def test_a07_overview_loads(client):
    response = client.get("/a07/")

    assert response.status_code == 200
    assert b"Authentication Failures" in response.data


def test_vulnerable_login_reveals_if_username_exists(client):
    unknown_user = client.post(
        "/a07/vulnerable",
        data={"username": "charlie", "password": "wrong"},
    )
    existing_user = client.post(
        "/a07/vulnerable",
        data={"username": "alice", "password": "wrong"},
    )

    assert unknown_user.status_code == 401
    assert existing_user.status_code == 401
    assert b"Username does not exist." in unknown_user.data
    assert b"Password is incorrect." in existing_user.data


def test_secure_login_uses_the_same_generic_error(client):
    unknown_user = client.post(
        "/a07/secure",
        data={"username": "charlie", "password": "wrong"},
    )
    existing_user = client.post(
        "/a07/secure",
        data={"username": "alice", "password": "wrong"},
    )

    assert unknown_user.status_code == 401
    assert existing_user.status_code == 401
    assert b"Invalid username or password." in unknown_user.data
    assert b"Invalid username or password." in existing_user.data
    assert b"Username does not exist." not in unknown_user.data
    assert b"Password is incorrect." not in existing_user.data


def test_secure_login_blocks_after_three_failures(client):
    for attempt_number in range(1, 4):
        response = client.post(
            "/a07/secure",
            data={"username": "alice", "password": "wrong"},
        )

        if attempt_number < 3:
            assert response.status_code == 401
        else:
            assert response.status_code == 429
            assert b"Too many failed attempts." in response.data


def test_secure_login_allows_valid_credentials(client):
    response = client.post(
        "/a07/secure",
        data={"username": "alice", "password": "Comp6841Demo!"},
    )

    assert response.status_code == 200
    assert b"Login successful." in response.data
