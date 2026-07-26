import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.sqlite3"
    return create_app(
        {
            "TESTING": True,
            "DATABASE": str(database_path),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()
