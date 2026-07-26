from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


bp = Blueprint("a07", __name__, url_prefix="/a07")
MAX_FAILED_ATTEMPTS = 3
DUMMY_PASSWORD_HASH = generate_password_hash("not-a-real-password")


def get_user(username):
    return get_db().execute(
        """
        SELECT id, username, password_hash
        FROM auth_users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()


def get_failed_count(identifier):
    row = get_db().execute(
        """
        SELECT failed_count
        FROM login_attempts
        WHERE identifier = ?
        """,
        (identifier,),
    ).fetchone()
    return row["failed_count"] if row else 0


def set_failed_count(identifier, failed_count):
    database = get_db()
    database.execute(
        """
        INSERT INTO login_attempts (identifier, failed_count)
        VALUES (?, ?)
        ON CONFLICT(identifier)
        DO UPDATE SET failed_count = excluded.failed_count
        """,
        (identifier, failed_count),
    )
    database.commit()


def clear_failed_count(identifier):
    database = get_db()
    database.execute(
        "DELETE FROM login_attempts WHERE identifier = ?",
        (identifier,),
    )
    database.commit()


@bp.get("/")
def overview():
    return render_template("a07/index.html")


@bp.route("/vulnerable", methods=("GET", "POST"))
def vulnerable_login():
    message = None
    success = False
    status_code = 200

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = get_user(username)

        if user is None:
            message = "Username does not exist."
            status_code = 401
        elif not check_password_hash(user["password_hash"], password):
            message = "Password is incorrect."
            status_code = 401
        else:
            message = "Login successful."
            success = True

    return (
        render_template(
            "a07/login.html",
            mode="Vulnerable",
            vulnerable=True,
            message=message,
            success=success,
            username=request.form.get("username", ""),
        ),
        status_code,
    )


@bp.route("/secure", methods=("GET", "POST"))
def secure_login():
    message = None
    success = False
    status_code = 200
    failed_count = 0

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        client_address = request.remote_addr or "local"
        identifier = f"{client_address}:{username}"
        failed_count = get_failed_count(identifier)

        if failed_count >= MAX_FAILED_ATTEMPTS:
            message = "Too many failed attempts. Try again later."
            status_code = 429
        else:
            user = get_user(username)
            password_hash = (
                user["password_hash"] if user is not None else DUMMY_PASSWORD_HASH
            )
            password_matches = check_password_hash(password_hash, password)

            if user is None or not password_matches:
                failed_count += 1
                set_failed_count(identifier, failed_count)

                if failed_count >= MAX_FAILED_ATTEMPTS:
                    message = "Too many failed attempts. Try again later."
                    status_code = 429
                else:
                    message = "Invalid username or password."
                    status_code = 401
            else:
                clear_failed_count(identifier)
                failed_count = 0
                message = "Login successful."
                success = True

    return (
        render_template(
            "a07/login.html",
            mode="Secure",
            vulnerable=False,
            message=message,
            success=success,
            username=request.form.get("username", ""),
            failed_count=failed_count,
            max_attempts=MAX_FAILED_ATTEMPTS,
            status_code=status_code,
        ),
        status_code,
    )


@bp.post("/reset")
def reset_attempts():
    database = get_db()
    database.execute("DELETE FROM login_attempts")
    database.commit()
    return redirect(url_for("a07.overview"))
