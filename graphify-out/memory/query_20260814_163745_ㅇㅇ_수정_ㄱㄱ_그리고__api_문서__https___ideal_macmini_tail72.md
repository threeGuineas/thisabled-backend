---
type: "query"
date: "2026-08-14T16:37:45.637337+00:00"
question: "ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록"
contributor: "graphify"
outcome: "useful"
source_nodes: ["recommendations()", "user_features()", "UiMode", "main.py", "FastAPI", "Response"]
---

# Q: ㅇㅇ 수정 ㄱㄱ 그리고 [api 문서](https://ideal-macmini.tail72b898.ts.net/docs) 자세하게, 결함 없게 구체적으로 아주 친절하게 패치해줘 프론트엔드가 곤란하지 않도록

## Answer

Expanded from original query via graph vocab: [api, auth, docs, schema, response, error, example, recommendations, recommendation, match, model, default]. Fixed the live MATCH failure by serializing domain UiMode.default as the model server's neutral empty ui_mode value in user_features(); added a route-level regression test and reproduced the real endpoint against match-input-v2 with HTTP 200, 7 items, and no error message. Added install_openapi() and complete OPERATION_GUIDES coverage for all 57 HTTP operations: Korean summaries and detailed frontend instructions, JSON request examples, actual success/error descriptions, bearer and refresh-cookie security, parameter guidance, recommendation success/insufficient/temporary examples, plain-text COMM guidance, pagination/media/loading rules, and WebSocket event documentation. Added typed HealthOut, BlockedOut, ReadOut, and RestrictionReleaseOut response models. Public Swagger now reports v0.3.0 with 46 paths and 66 schemas. Validation: 113 pytest tests passed; browser rendering and public openapi.json verified.

## Outcome

- Signal: useful

## Source Nodes

- recommendations()
- user_features()
- UiMode
- main.py
- FastAPI
- Response