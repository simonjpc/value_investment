from celery import Celery
from celery.schedules import crontab

# Configure Celery to use Redis as the broker and result backend
app = Celery(
    "my_celery_app",
    broker="redis://localhost:6379/0",  # Replace with your Redis URL if needed
    backend="redis://localhost:6379/0",
    include=[
        "valuation.pipeline_current_prices",
        "valuation.pipeline_drop_all_tables",
        "valuation.pipeline_prices_data",
        "valuation.pipeline_stmts_data",
        "valuation.pipeline_tickers",
        "valuation.pipeline_drop_db_connections",
        "valuation.pipeline_potential_epsx_candidates",
        "valuation.pipeline_potential_ncav_candidates",
    ],  # Add this line
)

# Load configuration options (optional)
app.conf.update(
    # result_expires=3600,  # Results will expire after an hour
    broker_connection_retry_on_startup=True,
)

app.conf.beat_schedule = {
    # Schedule the workflow to run once a month
    "monthly_workflow": {
        "task": "tasks.run_tasks.run_workflow",
        "schedule": crontab(
            day_of_month=1, hour=0, minute=0
        ),  # Runs on the 1st of every month at midnight
    },
    # Schedule the daily task
    "daily_tickers_prices": {
        "task": "tasks.run_tasks.tickers_current_prices_wrapper",
        "schedule": crontab(hour=0, minute=0),  # Runs every day at midnight
    },
}
