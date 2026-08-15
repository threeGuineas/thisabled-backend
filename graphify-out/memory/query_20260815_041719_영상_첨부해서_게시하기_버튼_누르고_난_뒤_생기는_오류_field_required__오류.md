---
type: "query"
date: "2026-08-15T04:17:19.230309+00:00"
question: "영상 첨부해서 게시하기 버튼 누르고 난 뒤 생기는 오류 Field required (오류 코드: 422) 이거 머임?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["publish_post()", "PublishIn", "PostCategory", "VideoUploadOut"]
---

# Q: 영상 첨부해서 게시하기 버튼 누르고 난 뒤 생기는 오류 Field required (오류 코드: 422) 이거 머임?

## Answer

Expanded from graph vocabulary: [publish, video, post, request, category, title, content, caption, status]. Runtime logs show POST /api/v1/media/videos succeeded with 201, PATCH /api/v1/posts/{post_id} succeeded with 200, caption status reached done, and only POST /api/v1/posts/{post_id}/publish returned 422. PublishIn requires JSON fields title, category, and content; allow_no_caption is optional. The current draft has content length 61 but title and category are null, so the frontend is not preserving/sending the v2.3 metadata contract. Send all three required fields in the publish JSON and use one of daily, info, hobby, concern, meetup for category. The frontend currently displays only the generic Pydantic message and drops detail[].loc, which is why it says only Field required.

## Outcome

- Signal: useful

## Source Nodes

- publish_post()
- PublishIn
- PostCategory
- VideoUploadOut