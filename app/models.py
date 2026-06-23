from datetime import datetime

from app.extensions import db


class MonitoredService(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(500), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    checks = db.relationship(
        "StatusCheck",
        backref="service",
        lazy=True,
        cascade="all, delete-orphan"
    )


class StatusCheck(db.Model):
    __tablename__ = "status_checks"

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=False
    )
    status = db.Column(db.String(20), nullable=False)
    status_code = db.Column(db.Integer, nullable=True)
    response_time_ms = db.Column(db.Float, nullable=True)
    message = db.Column(db.String(500), nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)