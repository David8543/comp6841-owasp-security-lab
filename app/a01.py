from flask import Blueprint, abort, render_template

from .db import get_db


bp = Blueprint("a01", __name__, url_prefix="/a01")
CURRENT_USER_ID = 1


def get_note(note_id):
    return get_db().execute(
        """
        SELECT notes.id, notes.user_id, notes.title, notes.content,
               users.username
        FROM notes
        JOIN users ON users.id = notes.user_id
        WHERE notes.id = ?
        """,
        (note_id,),
    ).fetchone()


@bp.get("/")
def overview():
    return render_template("a01/index.html")


@bp.get("/vulnerable/notes/<int:note_id>")
def vulnerable_note(note_id):
    note = get_note(note_id)
    if note is None:
        abort(404)
    return render_template("a01/note.html", note=note, mode="Vulnerable")


@bp.get("/secure/notes/<int:note_id>")
def secure_note(note_id):
    note = get_note(note_id)
    if note is None:
        abort(404)
    if note["user_id"] != CURRENT_USER_ID:
        abort(403)
    return render_template("a01/note.html", note=note, mode="Secure")
