import os

from flask import Flask, app

from app.extensions import db
from app.scheduler import start_scheduler
from app.scheduler import start_scheduler


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///uptime.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from app import models
        db.create_all()

    from app.scheduler import start_scheduler
    start_scheduler(app)

    return app