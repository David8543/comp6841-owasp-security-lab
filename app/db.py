import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db():
    database = get_db()
    database.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        INSERT OR IGNORE INTO users (id, username)
        VALUES
            (1, 'alice'),
            (2, 'bob');

        INSERT OR IGNORE INTO notes (id, user_id, title, content)
        VALUES
            (1, 1, 'Alice private note', 'Alice exam preparation notes'),
            (2, 2, 'Bob private note', 'Bob confidential project idea');
        """
    )
    database.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
