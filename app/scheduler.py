import os
from apscheduler.schedulers.background import BackgroundScheduler

from app.extensions import db
from app.models import MonitoredService, StatusCheck
from app.services.monitor_service import check_website_status
from app.services.email_service import send_email_alert


scheduler = None


def send_status_change_alert(service, previous_status, current_result):
    """
    Sends alert only when service status changes.
    This avoids sending repeated emails every few minutes.
    """
    current_status = current_result["status"]

    if previous_status == current_status:
        return

    if current_status == "DOWN":
        subject = f"DOWN Alert: {service.name}"
        body = f"""
Service DOWN Alert

Service Name: {service.name}
URL: {service.url}
Current Status: {current_status}
Status Code: {current_result["status_code"]}
Response Time: {current_result["response_time_ms"]} ms
Message: {current_result["message"]}

The monitored service appears to be unavailable.
"""
        send_email_alert(subject, body)

    elif previous_status == "DOWN" and current_status == "UP":
        subject = f"RECOVERY Alert: {service.name}"
        body = f"""
Service Recovery Alert

Service Name: {service.name}
URL: {service.url}
Current Status: {current_status}
Status Code: {current_result["status_code"]}
Response Time: {current_result["response_time_ms"]} ms
Message: {current_result["message"]}

The monitored service is reachable again.
"""
        send_email_alert(subject, body)


def run_scheduled_checks(app):
    """
    Automatically checks all saved services and stores the latest result.
    """
    with app.app_context():
        services = MonitoredService.query.all()

        if not services:
            print("Scheduled monitor: no services found.")
            return

        print(f"Scheduled monitor: checking {len(services)} service(s).")

        for service in services:
            previous_check = (
                StatusCheck.query
                .filter_by(service_id=service.id)
                .order_by(StatusCheck.checked_at.desc())
                .first()
            )

            previous_status = previous_check.status if previous_check else None

            result = check_website_status(service.url)

            if result["status"] == "INVALID":
                continue

            status_check = StatusCheck(
                service_id=service.id,
                status=result["status"],
                status_code=result["status_code"],
                response_time_ms=result["response_time_ms"],
                message=result["message"]
            )

            db.session.add(status_check)

            if previous_status is not None:
                send_status_change_alert(service, previous_status, result)

        db.session.commit()
        print("Scheduled monitor: checks completed.")


def start_scheduler(app):
    """
    Starts the background scheduler only when enabled.
    """
    global scheduler

    scheduler_enabled = os.getenv("SCHEDULER_ENABLED", "false").lower() == "true"

    if not scheduler_enabled:
        print("Scheduled monitor: disabled.")
        return

    if app.config.get("TESTING"):
        print("Scheduled monitor: disabled during testing.")
        return

    if scheduler and scheduler.running:
        print("Scheduled monitor: already running.")
        return

    interval_minutes = int(os.getenv("CHECK_INTERVAL_MINUTES", "5"))

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        func=lambda: run_scheduled_checks(app),
        trigger="interval",
        minutes=interval_minutes,
        id="uptime_scheduled_checks",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()
    print(f"Scheduled monitor: running every {interval_minutes} minute(s).")