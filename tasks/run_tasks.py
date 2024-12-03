from valuation.pipeline_current_prices import tickers_current_prices
from valuation.pipeline_drop_all_tables import drop_tables
from valuation.pipeline_prices_data import tickers_prices_data
from valuation.pipeline_stmts_data import tickers_financial_stmts_data
from valuation.pipeline_tickers import tickers_data
from valuation.pipeline_drop_db_connections import terminate_all_connections
from valuation.pipeline_potential_epsx_candidates import filter_epsx_candidates
from valuation.pipeline_potential_ncav_candidates import filter_ncav_candidates
from celery import shared_task
from datetime import datetime, timedelta
from django.core.cache import cache  # Or use a DB table for persistent state
from celery import chain

# Chain the tasks to run sequentially
workflow = chain(
    # terminate_all_connections.s()
    drop_tables.s(),
    tickers_data.s(),
    tickers_financial_stmts_data.s(),
    tickers_prices_data.s(),
    tickers_current_prices.s(),
    filter_ncav_candidates.s(),
    filter_epsx_candidates.s(),
)

# Start the workflow
workflow.apply_async()

WORKFLOW_RUNNING_KEY = "workflow_running"
LAST_WORKFLOW_RUN_KEY = "last_workflow_run"


@shared_task
def run_workflow():
    # Mark workflow as running
    cache.set(
        WORKFLOW_RUNNING_KEY, True, timeout=None
    )  # No timeout to track workflow running
    try:
        workflow = chain(
            drop_tables.s(),
            tickers_data.s(),
            tickers_financial_stmts_data.s(),
            tickers_prices_data.s(),
            tickers_current_prices.s(),
            filter_ncav_candidates.s(),
            filter_epsx_candidates.s(),
        )
        workflow.apply_async()
        # After completion, store the last run time
        cache.set(LAST_WORKFLOW_RUN_KEY, datetime.now(), timeout=None)
    except Exception as e:
        print(f"Workflow failed: {e}")
        raise
    finally:
        # Mark workflow as not running
        cache.delete(WORKFLOW_RUNNING_KEY)


@shared_task
def tickers_current_prices_wrapper():
    # Check if workflow is running
    if cache.get(WORKFLOW_RUNNING_KEY):
        print("Workflow is running. Delaying `tickers_current_prices`...")
        return  # Skip or reschedule based on requirement

    # Check if the last workflow was recent (e.g., within the last month)
    last_run = cache.get(LAST_WORKFLOW_RUN_KEY)
    if last_run and last_run > datetime.now() - timedelta(days=30):
        print("Workflow recently completed. Running `tickers_current_prices`...")
        tickers_current_prices.delay()  # Call the actual task
    else:
        print("Workflow hasn't completed recently. Waiting...")
