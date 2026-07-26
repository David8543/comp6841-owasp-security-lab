from flask import Blueprint, redirect, render_template, request, url_for

from .db import get_db


bp = Blueprint("a05", __name__, url_prefix="/a05")


def get_comments():
    return get_db().execute(
        "SELECT id, body FROM comments ORDER BY id"
    ).fetchall()


def store_comment(body):
    database = get_db()
    database.execute(
        "INSERT INTO comments (body) VALUES (?)",
        (body,),
    )
    database.commit()


@bp.get("/")
def overview():
    return render_template("a05/index.html")


@bp.route("/vulnerable", methods=("GET", "POST"))
def vulnerable_comments():
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            store_comment(body)
        return redirect(url_for("a05.vulnerable_comments"))

    return render_template(
        "a05/comments.html",
        comments=get_comments(),
        mode="Vulnerable",
        vulnerable=True,
    )


@bp.route("/secure", methods=("GET", "POST"))
def secure_comments():
    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if body:
            store_comment(body)
        return redirect(url_for("a05.secure_comments"))

    return render_template(
        "a05/comments.html",
        comments=get_comments(),
        mode="Secure",
        vulnerable=False,
    )


@bp.post("/reset")
def reset_comments():
    database = get_db()
    database.execute("DELETE FROM comments")
    database.execute(
        "INSERT INTO comments (body) VALUES (?)",
        ("Welcome to the local comments board.",),
    )
    database.commit()
    return redirect(url_for("a05.overview"))
