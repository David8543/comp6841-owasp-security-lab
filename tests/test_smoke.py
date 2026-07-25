from app import create_app


def test_home_page_loads():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"OWASP Top 10:2025 Security Lab" in response.data