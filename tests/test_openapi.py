"""프론트엔드 계약 문서가 라우트 변경 뒤에도 빠지거나 퇴행하지 않도록 검증."""

from app.main import app
from app.openapi import OPERATION_GUIDES


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _schema():
    # 다른 테스트가 캐시를 만들었더라도 같은 정본을 검사한다.
    return app.openapi()


def test_every_http_operation_has_a_detailed_guide():
    schema = _schema()
    actual = {
        (method, path)
        for path, path_item in schema["paths"].items()
        for method in path_item
        if method in HTTP_METHODS
    }

    assert actual == set(OPERATION_GUIDES)
    for method, path in actual:
        operation = schema["paths"][path][method]
        assert len(operation["summary"]) >= 4
        assert len(operation["description"]) >= 100
        assert "프론트 공통 처리" in operation["description"]
        for response in operation["responses"].values():
            assert response["description"] != "Successful Response"


def test_json_request_bodies_have_copyable_examples():
    schema = _schema()
    for path, path_item in schema["paths"].items():
        for method, operation in path_item.items():
            if method not in HTTP_METHODS:
                continue
            json_body = operation.get("requestBody", {}).get("content", {}).get(
                "application/json"
            )
            if json_body is not None:
                assert "example" in json_body, f"missing request example: {method} {path}"


def test_protected_operations_document_unauthorized_response():
    schema = _schema()
    for path, path_item in schema["paths"].items():
        for method, operation in path_item.items():
            if method in HTTP_METHODS and operation.get("security"):
                assert "401" in operation["responses"], f"missing 401: {method} {path}"


def test_frontend_critical_contracts_are_explicit():
    schema = _schema()
    info = schema["info"]
    assert info["version"] == "0.3.0"
    assert "finally에서 로딩 상태를 해제" in info["description"]
    assert "WebSocket (OpenAPI 비지원 영역)" in info["description"]
    assert "422" in info["description"] and "배열" in info["description"]

    callback = schema["paths"]["/api/v1/auth/{provider}/callback"]["get"]
    assert "302" in callback["responses"]
    assert "200" not in callback["responses"]

    refresh = schema["paths"]["/api/v1/auth/refresh"]["post"]
    assert refresh["security"] == [{"RefreshCookie": []}]
    assert schema["components"]["securitySchemes"]["RefreshCookie"]["in"] == "cookie"

    recommendation = schema["paths"]["/api/v1/recommendations"]["get"]
    assert "항상 로딩을 끝내고" in recommendation["description"]
    examples = recommendation["responses"]["200"]["content"]["application/json"][
        "examples"
    ]
    assert set(examples) == {"success", "insufficient", "temporary"}
    assert examples["temporary"]["value"]["items"] == []
    assert examples["temporary"]["value"]["message"]

    simplify = schema["paths"]["/api/v1/comm/simplify"]["post"]
    assert "일반 텍스트" in simplify["description"]

    retry_caption = schema["paths"]["/api/v1/posts/{post_id}/caption/retry"]["post"]
    assert retry_caption["responses"]["202"]
    assert "503" in retry_caption["responses"]
    assert "processing" in retry_caption["description"]

    video_upload = schema["paths"]["/api/v1/media/videos"]["post"]
    assert "실제" in video_upload["description"]
    assert "STT_DAILY_BUDGET_EXCEEDED" in video_upload["responses"]["503"]["description"]


def test_parameters_explain_opaque_ids_and_cursors():
    schema = _schema()
    feed = schema["paths"]["/api/v1/feed"]["get"]
    parameters = {parameter["name"]: parameter for parameter in feed["parameters"]}
    assert "next_cursor" in parameters["cursor"]["description"]
    assert parameters["limit"]["description"]
    assert "daily" in parameters["category"]["description"]
    assert "제목" in parameters["q"]["description"]

    detail = schema["paths"]["/api/v1/posts/{post_id}"]["get"]
    post_id = next(parameter for parameter in detail["parameters"] if parameter["name"] == "post_id")
    assert post_id["description"]
    assert post_id["example"]


def test_post_contract_documents_title_category_and_video_publish_metadata():
    schema = _schema()
    create_example = schema["paths"]["/api/v1/posts"]["post"]["requestBody"]["content"][
        "application/json"
    ]["example"]
    assert create_example["title"]
    assert create_example["category"] == "daily"

    publish_example = schema["paths"]["/api/v1/posts/{post_id}/publish"]["post"][
        "requestBody"
    ]["content"]["application/json"]["example"]
    assert {"title", "category", "content", "allow_no_caption"} <= publish_example.keys()
