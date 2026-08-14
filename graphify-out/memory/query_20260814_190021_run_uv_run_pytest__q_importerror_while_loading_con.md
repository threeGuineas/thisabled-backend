---
type: "query"
date: "2026-08-14T19:00:21.326072+00:00"
question: "Run uv run pytest -q\nImportError while loading conftest /home/runner/work/thisabled-backend/thisabled-backend/tests/conftest.py.\ntests/conftest.py:22: in <module>\n    from app.main import app\napp/main.py:180: in <module>\n    app.mount(\"/uploads\", StaticFiles(directory=settings.UPLOAD_DIR), name=\"uploads\")\n.venv/lib/python3.11/site-packages/starlette/staticfiles.py:56: in __init__\n    raise RuntimeError(f\"Directory {directory} does not exist\")\nE   RuntimeError: Directory /app/uploads does not exist"
contributor: "graphify"
outcome: "useful"
source_nodes: ["main.py", "Settings", "storage.py", "conftest.py"]
---

# Q: Run uv run pytest -q
ImportError while loading conftest /home/runner/work/thisabled-backend/thisabled-backend/tests/conftest.py.
tests/conftest.py:22: in <module>
    from app.main import app
app/main.py:180: in <module>
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
.venv/lib/python3.11/site-packages/starlette/staticfiles.py:56: in __init__
    raise RuntimeError(f"Directory {directory} does not exist")
E   RuntimeError: Directory /app/uploads does not exist

## Answer

Expanded from original query via graph vocab: [main, settings, storage, path, upload, uploads, runtime, pytest, test, config]. PR #11 GitHub Actions run 31830575119 fails before test collection because app.main mounts StaticFiles at import time with check_dir=True, while settings.UPLOAD_DIR defaults to /app/uploads and that Docker-only directory does not exist on the native GitHub runner. The lifespan already creates the directory, but lifespan runs after import, so it is too late. Docker hides the defect because its image/volume pre-creates /app/uploads. Focused fix: mount StaticFiles with check_dir=False so import is side-effect-free, retain lifespan and storage mkdir as runtime guarantees, add a fresh-process import regression test with a nonexistent UPLOAD_DIR, then run uv run pytest -q and push to PR #11.

## Outcome

- Signal: useful

## Source Nodes

- main.py
- Settings
- storage.py
- conftest.py