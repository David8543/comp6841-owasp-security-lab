def test_vulnerable_route_exposes_another_users_note(client):
    response = client.get("/a01/vulnerable/notes/2")

    assert response.status_code == 200
    assert b"Bob confidential project idea" in response.data


def test_secure_route_blocks_another_users_note(client):
    response = client.get("/a01/secure/notes/2")

    assert response.status_code == 403
    assert b"Bob confidential project idea" not in response.data


def test_secure_route_allows_own_note(client):
    response = client.get("/a01/secure/notes/1")

    assert response.status_code == 200
    assert b"Alice exam preparation notes" in response.data
