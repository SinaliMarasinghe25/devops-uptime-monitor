import os
from apscheduler.schedulers.background import BackgroundScheduler

from app.extensions import db
from app.models import MonitoredService, StatusCheck
from app.services.monitor_service import check_website_status


scheduler = None


def run_scheduled_checks(app):
    """
    Automatically checks all saved services and stores the latest result.
    This runs in the background using APScheduler.
    """
    with app.app_context():
        services = MonitoredService.query.all()

        if not services:
            print("Scheduled monitor: no services found.")
            return

        print(f"Scheduled monitor: checking {len(services)} service(s).")

        for service in services:
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

        db.session.commit()
        print("Scheduled monitor: checks completed.")


def start_scheduler(app):
    """
    Starts the background scheduler only when enabled.
    This prevents tests from accidentally starting background jobs.
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