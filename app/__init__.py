import os

from flask import Flask, render_template

from . import db
from .a01 import bp as a01_bp
from .a05 import bp as a05_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="local-lab-only",
        DATABASE=os.path.join(app.instance_path, "security-lab.sqlite3"),
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    app.register_blueprint(a01_bp)
    app.register_blueprint(a05_bp)

    with app.app_context():
        db.init_db()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    return app
