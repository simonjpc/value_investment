from celery import Celery

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
