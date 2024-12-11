from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta

# Configure Celery to use Redis as the broker and result backend
app = Celery(
    "my_celery_app",
    broker="redis://localhost:6379/0",  # Replace with your Redis URL if needed
    backend="redis://localhost:6379/0",
    include=[
        "tasks.run_tasks",
    ],  # Add this line
)

# Load configuration options (optional)
app.conf.update(
    # result_expires=3600,  # Results will expire after an hour
    broker_connection_retry_on_startup=True,
)

monthly_workflow_start_time = datetime.now() + timedelta(seconds=5)
daily_workflow_start_time = datetime.now() + timedelta(seconds=12)

app.conf.beat_schedule = {
    # Schedule the workflow to run once a month
    "monthly_workflow": {
        "task": "tasks.run_tasks.run_workflow",
        "schedule": crontab(
            day_of_month=12,
            hour=0,
            minute=0,
            # minute="*/14"
        ),  # Runs on the 1st of every month at midnight
        "options": {"start_time": monthly_workflow_start_time},
    },
    # Schedule the daily task
    "daily_tickers_prices": {
        "task": "tasks.run_tasks.tickers_current_prices_wrapper",
        "schedule": crontab(hour=0, minute=15),  # Runs every day at midnight fifteen
        # "schedule": crontab(minute="*/5"),
        "options": {"start_time": daily_workflow_start_time},
    },
}
