PAYLOAD = "<script>alert('Stored XSS executed')</script>"


def test_a05_overview_loads(client):
    response = client.get("/a05/")

    assert response.status_code == 200
    assert b"Stored XSS" in response.data


def test_vulnerable_page_renders_stored_script_as_html(client):
    response = client.post(
        "/a05/vulnerable",
        data={"body": PAYLOAD},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert PAYLOAD.encode() in response.data


def test_secure_page_escapes_the_same_stored_script(client):
    client.post(
        "/a05/vulnerable",
        data={"body": PAYLOAD},
    )
    response = client.get("/a05/secure")

    assert response.status_code == 200
    assert PAYLOAD.encode() not in response.data
    assert b"&lt;script&gt;" in response.data
