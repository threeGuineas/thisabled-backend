# Chat Read Status Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-recipient unread badges and a sender-visible receipt on exactly the recipient's last-read message.

**Architecture:** Persist one read cursor for each `(room_id, user_id)` in `chat_read_states`. Room-list queries count visible incoming messages after that cursor; a cursor-less message-list request advances it and publishes a content-free `chat.read` event. Message serialization compares the counterpart cursor, so only the matching sent message is marked read.

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy async, PostgreSQL 15, Alembic, Redis pub/sub, pytest.

## Global Constraints

- Keep PKs and FKs UUID-based.
- Exclude SAFE `pending` messages from visibility, read advancement, and unread counts.
- Advance read state only when the latest message page is requested without `cursor`.
- Never include message content in WebSocket events.
- Run tests with `DATABASE_URL` rewritten from `thisabled` to `thisabled_test`.
- Commit implementation and tests as one `feat(chat)` change after the full suite passes.

---

## File Structure

- `app/models/chat.py` owns `ChatReadState`; `app/models/__init__.py` exports it.
- `app/services/chat.py` owns cursor comparison, unread counting, and cursor advancement.
- `app/schemas/chat.py` and `app/api/v1/chat.py` expose the API and event.
- `alembic/versions/f7b9114a3c2e_chat_read_states.py` creates the new table.
- `tests/test_chat.py` and `tests/test_ws.py` cover REST and event behavior.
- `docs/erd.dbml` and `docs/api.md` document the contract.

### Task 1: Write failing behavior tests

**Files:**
- Modify: `tests/test_chat.py`
- Modify: `tests/test_ws.py`

**Interfaces:**
- Produces: `RoomOut.unread_count: int`, `RoomListOut.unread_total: int`, `MessageOut.is_read: bool`, and `chat.read`.

- [ ] **Step 1: Add the unread badge and receipt test**

```python
async def test_opening_latest_messages_marks_unread_and_receipt(client, safety):
    a = await register(client, "읽음발신")
    b = await register(client, "읽음수신")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room_id = (await _room(client, ha, b["user_id"])).json()["id"]
    await _send(client, ha, room_id, "첫 메시지")
    await _send(client, ha, room_id, "두 번째 메시지")

    inbox = (await client.get("/api/v1/chat/rooms", headers=hb)).json()
    assert inbox["unread_total"] == 2
    assert inbox["items"][0]["unread_count"] == 2
    before = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=ha)).json()
    assert [item["is_read"] for item in before["items"]] == [False, False]

    await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)
    after = (await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=ha)).json()
    assert (await client.get("/api/v1/chat/rooms", headers=hb)).json()["unread_total"] == 0
    assert [item["is_read"] for item in after["items"]] == [True, False]
```

- [ ] **Step 2: Verify the test is red**

Run: `docker compose exec -T app pytest tests/test_chat.py::test_opening_latest_messages_marks_unread_and_receipt -q`

Expected: FAIL because the response fields do not exist.

- [ ] **Step 3: Add the event test and verify it is red**

```python
async def test_opening_messages_publishes_read_event(client, test_redis, safety):
    a = await register(client, "이벤트읽음발신")
    b = await register(client, "이벤트읽음수신")
    ha, hb = auth_header(a["access_token"]), auth_header(b["access_token"])
    await make_friends(client, ha, hb, b["user_id"])
    room_id = (await _room(client, ha, b["user_id"])).json()["id"]
    sent = (await _send(client, ha, room_id, "읽음 이벤트")).json()
    pubsub = test_redis.pubsub()
    await pubsub.subscribe(user_channel(a["user_id"]))
    try:
        await client.get(f"/api/v1/chat/rooms/{room_id}/messages", headers=hb)
        event = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        assert json.loads(event["data"]) == {
            "type": "chat.read",
            "payload": {"room_id": room_id, "message_id": sent["id"]},
        }
    finally:
        await pubsub.unsubscribe(user_channel(a["user_id"]))
        await pubsub.aclose()
```

Run: `docker compose exec -T app pytest tests/test_ws.py::test_opening_messages_publishes_read_event -q`

Expected: FAIL because no `chat.read` publication exists.

### Task 2: Persist and calculate the cursor

**Files:**
- Modify: `app/models/chat.py`
- Modify: `app/models/__init__.py`
- Modify: `app/services/chat.py`
- Create: `alembic/versions/f7b9114a3c2e_chat_read_states.py`

**Interfaces:**
- Produces: `unread_count(db, room_id, user_id) -> int`, `counterpart_read_message_id(db, room, user_id) -> UUID | None`, and `advance_read_cursor(db, room, user_id) -> UUID | None`.

- [ ] **Step 1: Add the ORM model and matching migration**

```python
class ChatReadState(Base):
    __tablename__ = "chat_read_states"
    __table_args__ = (
        UniqueConstraint("room_id", "user_id"),
        Index("ix_chat_read_states_user_room", "user_id", "room_id"),
    )
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    last_read_message_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    last_read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

The migration uses revision `f7b9114a3c2e`, `down_revision = "84e58e0eefae"`, the same columns, two cascading FKs, a unique `(room_id, user_id)`, and `ix_chat_read_states_user_room`.

- [ ] **Step 2: Implement cursor helpers**

```python
async def advance_read_cursor(db: AsyncSession, room: ChatRoom, user_id: uuid.UUID) -> uuid.UUID | None:
    latest = (await db.execute(
        select(ChatMessage).where(
            ChatMessage.room_id == room.id,
            ChatMessage.sender_id.is_distinct_from(user_id),
            ChatMessage.safety_status != SafetyStatus.pending.value,
        ).order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc()).limit(1)
    )).scalar_one_or_none()
    if latest is None:
        return None
    state = await _read_state(db, room.id, user_id)
    if state is not None and not _is_after(latest, state):
        return None
    if state is None:
        db.add(ChatReadState(room_id=room.id, user_id=user_id,
                             last_read_message_id=latest.id, last_read_at=latest.created_at))
    else:
        state.last_read_message_id, state.last_read_at = latest.id, latest.created_at
    await db.commit()
    return latest.id
```

Implement `_is_after` and the unread predicate using the same lexicographic `(created_at, id)` position.

- [ ] **Step 3: Upgrade isolated schema and verify green**

Run: `docker compose exec -T app sh -lc 'DATABASE_URL=$(echo "$DATABASE_URL" | sed "s@/thisabled$@/thisabled_test@"); alembic upgrade head; pytest tests/test_chat.py::test_opening_latest_messages_marks_unread_and_receipt -q'`

Expected: PASS.

### Task 3: Expose, document, verify, and commit

**Files:**
- Modify: `app/schemas/chat.py`
- Modify: `app/api/v1/chat.py`
- Modify: `docs/erd.dbml`
- Modify: `docs/api.md`
- Modify: `tests/test_chat.py`
- Modify: `tests/test_ws.py`

**Interfaces:**
- Consumes: Task 2 helpers and `publish_to_user`.
- Produces: fields plus `{"type":"chat.read","payload":{"room_id":"…","message_id":"…"}}`.

- [ ] **Step 1: Add response fields**

```python
class RoomOut(BaseModel):
    unread_count: int = 0

class RoomListOut(BaseModel):
    items: list[RoomOut]
    unread_total: int = 0

class MessageOut(BaseModel):
    is_read: bool = False
```

- [ ] **Step 2: Wire first-page advancement and receipt serialization**

```python
if cursor is None:
    read_message_id = await advance_read_cursor(db, room, user.id)
    if read_message_id is not None and (other_id := counterpart_id(room, user.id)) is not None:
        await publish_to_user(
            redis, other_id,
            {"type": "chat.read", "payload": {
                "room_id": str(room.id), "message_id": str(read_message_id)
            }},
        )
counterpart_read_id = await counterpart_read_message_id(db, room, user.id)
```

Pass `counterpart_read_id` into `_message_out`; it marks only a caller-owned matching message. Compute each room's `unread_count`, sum `unread_total`, and add the Redis dependency to `list_messages`.

- [ ] **Step 3: Update ERD and API documentation**

Document the new table, response fields, newest-page behavior, and content-free event.

- [ ] **Step 4: Verify focused and full suites**

Run: `docker compose exec -T app sh -lc 'DATABASE_URL=$(echo "$DATABASE_URL" | sed "s@/thisabled$@/thisabled_test@"); pytest tests/test_chat.py tests/test_ws.py -q'`

Expected: PASS.

Run: `docker compose exec -T app sh -lc 'DATABASE_URL=$(echo "$DATABASE_URL" | sed "s@/thisabled$@/thisabled_test@"); pytest -q'`

Expected: all tests pass.

- [ ] **Step 5: Update graph and commit**

Run: `graphify update .`

Run:
```bash
git add app/models/chat.py app/models/__init__.py app/services/chat.py app/api/v1/chat.py app/schemas/chat.py alembic/versions/f7b9114a3c2e_chat_read_states.py docs/erd.dbml docs/api.md tests/test_chat.py tests/test_ws.py graphify-out
git commit -m "feat(chat): 읽음 상태와 미읽음 수 추가"
```

## Plan Self-Review

- The plan covers persistence, badges, the single sender receipt, first-page timing, SAFE exclusion, real-time updates, documentation, and regression testing.
- Names and types in Tasks 2 and 3 match the declared interfaces.
- Each implementation task has concrete test code, commands, and expected results.
