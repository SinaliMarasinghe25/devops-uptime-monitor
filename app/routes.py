from flask import Blueprint, jsonify, render_template, request

from app.services.monitor_service import check_website_status

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def dashboard():
    result = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        result = check_website_status(url)

    return render_template("dashboard.html", result=result)


@main.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "DevOps Uptime Monitor"
    }), 200