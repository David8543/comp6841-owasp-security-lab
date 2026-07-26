def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"OWASP Top 10:2025 Security Lab" in response.data
