from unittest.mock import MagicMock, patch


def test_grammar_check_with_errors(client, auth_headers):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "matches": [
            {
                "message": "Possible spelling mistake found.",
                "offset": 10,
                "length": 7,
                "replacements": [{"value": "sentence"}, {"value": "sentences"}],
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch(
        "app.services.grammar_service.requests.post", return_value=mock_response
    ):
        response = client.post(
            "/grammar/check",
            json={"text": "This is a sentnce with errors."},
            headers=auth_headers,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["error_count"] == 1
    assert data["errors"][0]["message"] == "Possible spelling mistake found."
    assert "sentence" in data["errors"][0]["replacements"]


def test_grammar_check_no_errors(client, auth_headers):
    mock_response = MagicMock()
    mock_response.json.return_value = {"matches": []}
    mock_response.raise_for_status = MagicMock()

    with patch(
        "app.services.grammar_service.requests.post", return_value=mock_response
    ):
        response = client.post(
            "/grammar/check",
            json={"text": "This is a correct sentence."},
            headers=auth_headers,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["error_count"] == 0
    assert data["errors"] == []


def test_grammar_check_service_failure(client, auth_headers):
    with patch(
        "app.services.grammar_service.requests.post",
        side_effect=Exception("Connection error"),
    ):
        response = client.post(
            "/grammar/check",
            json={"text": "Some text."},
            headers=auth_headers,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["error_count"] == 0
    assert data["warning"] is not None
    assert "Grammar check failed" in data["warning"]


def test_grammar_check_unauthenticated(client):
    response = client.post("/grammar/check", json={"text": "Hello."})
    assert response.status_code == 401
