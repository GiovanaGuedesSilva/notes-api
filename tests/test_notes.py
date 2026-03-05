import io


def test_create_note(client, auth_headers):
    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "# Hello\n\nThis is **bold**."},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "# Hello\n\nThis is **bold**."
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_notes_empty(client, auth_headers):
    response = client.get("/notes/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_list_notes(client, auth_headers):
    client.post(
        "/notes/",
        json={"title": "Note 1", "content": "Content 1"},
        headers=auth_headers,
    )
    client.post(
        "/notes/",
        json={"title": "Note 2", "content": "Content 2"},
        headers=auth_headers,
    )

    response = client.get("/notes/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_note(client, auth_headers):
    create_resp = client.post(
        "/notes/", json={"title": "My Note", "content": "Content"}, headers=auth_headers
    )
    note_id = create_resp.json()["id"]

    response = client.get(f"/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "My Note"


def test_get_note_not_found(client, auth_headers):
    response = client.get("/notes/999", headers=auth_headers)
    assert response.status_code == 404


def test_get_note_html(client, auth_headers):
    create_resp = client.post(
        "/notes/",
        json={"title": "HTML Note", "content": "# Hello\n\n**bold**"},
        headers=auth_headers,
    )
    note_id = create_resp.json()["id"]

    response = client.get(f"/notes/{note_id}/html", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "<h1" in data["html_content"]
    assert "<strong>" in data["html_content"]


def test_update_note(client, auth_headers):
    create_resp = client.post(
        "/notes/",
        json={"title": "Original", "content": "Old content"},
        headers=auth_headers,
    )
    note_id = create_resp.json()["id"]

    response = client.put(
        f"/notes/{note_id}",
        json={"title": "Updated Title"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["content"] == "Old content"


def test_update_note_not_found(client, auth_headers):
    response = client.put("/notes/999", json={"title": "X"}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_note(client, auth_headers):
    create_resp = client.post(
        "/notes/", json={"title": "To Delete", "content": "Bye"}, headers=auth_headers
    )
    note_id = create_resp.json()["id"]

    response = client.delete(f"/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 204

    get_response = client.get(f"/notes/{note_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_note_not_found(client, auth_headers):
    response = client.delete("/notes/999", headers=auth_headers)
    assert response.status_code == 404


def test_upload_note(client, auth_headers):
    md_content = b"# Uploaded\n\nThis is uploaded content."
    response = client.post(
        "/notes/upload",
        files={"file": ("mynote.md", io.BytesIO(md_content), "text/markdown")},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "mynote"
    assert "# Uploaded" in data["content"]


def test_upload_non_md_file(client, auth_headers):
    response = client.post(
        "/notes/upload",
        files={"file": ("note.txt", io.BytesIO(b"content"), "text/plain")},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_note_ownership_isolation(client):
    # Register two users
    client.post(
        "/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "pass123"},
    )
    client.post(
        "/auth/register",
        json={"username": "bob", "email": "bob@example.com", "password": "pass123"},
    )

    # Get tokens
    alice_token = client.post(
        "/auth/token", data={"username": "alice", "password": "pass123"}
    ).json()["access_token"]
    bob_token = client.post(
        "/auth/token", data={"username": "bob", "password": "pass123"}
    ).json()["access_token"]

    alice_headers = {"Authorization": f"Bearer {alice_token}"}
    bob_headers = {"Authorization": f"Bearer {bob_token}"}

    # Alice creates a note
    create_resp = client.post(
        "/notes/",
        json={"title": "Alice's Secret Note", "content": "Private content"},
        headers=alice_headers,
    )
    note_id = create_resp.json()["id"]

    # Bob should see an empty list (not Alice's notes)
    bob_notes = client.get("/notes/", headers=bob_headers).json()
    assert len(bob_notes) == 0

    # Bob should get 404 when trying to access Alice's note by ID
    response = client.get(f"/notes/{note_id}", headers=bob_headers)
    assert response.status_code == 404


def test_unauthenticated_access(client):
    response = client.get("/notes/")
    assert response.status_code == 401
