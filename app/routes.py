from urllib.parse import urlparse

from flask import Blueprint, jsonify, render_template, request

from app.extensions import db
from app.models import MonitoredService, StatusCheck
from app.services.monitor_service import check_website_status

main = Blueprint("main", __name__)


def get_service_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc or url


@main.route("/", methods=["GET", "POST"])
def dashboard():
    result = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        result = check_website_status(url)

        if result["status"] != "INVALID":
            service = MonitoredService.query.filter_by(url=url).first()

            if service is None:
                service = MonitoredService(
                    name=get_service_name(url),
                    url=url
                )
                db.session.add(service)
                db.session.flush()

            status_check = StatusCheck(
                service_id=service.id,
                status=result["status"],
                status_code=result["status_code"],
                response_time_ms=result["response_time_ms"],
                message=result["message"]
            )

            db.session.add(status_check)
            db.session.commit()

    recent_checks = (
        StatusCheck.query
        .order_by(StatusCheck.checked_at.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html",
        result=result,
        recent_checks=recent_checks
    )


@main.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "DevOps Uptime Monitor"
    }), 200