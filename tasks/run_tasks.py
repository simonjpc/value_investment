from valuation.pipeline_current_prices import tickers_current_prices_workflow
from valuation.pipeline_drop_all_tables import drop_tables
from valuation.pipeline_prices_data import tickers_prices_data
from valuation.pipeline_stmts_data import tickers_financial_stmts_data
from valuation.pipeline_tickers import tickers_data
from valuation.pipeline_drop_db_connections import terminate_all_connections
from valuation.pipeline_potential_epsx_candidates import filter_epsx_candidates
from valuation.pipeline_potential_ncav_candidates import filter_ncav_candidates
from valuation.pipeline_aux import workflow
from celery import shared_task
from datetime import datetime, timedelta
import redis
import time
from celery import chain

# Chain the tasks to run sequentially
# workflow = chain(
#     # terminate_all_connections.s(),
#     drop_tables.s(),
#     tickers_data.s(),
#     tickers_financial_stmts_data.s(),
#     tickers_prices_data.s(),
#     tickers_current_prices.s(),
#     filter_ncav_candidates.s(),
#     filter_epsx_candidates.s(),
# )

# # Start the workflow
# workflow.apply_async()

redis_client = redis.Redis(host="localhost", port=6379, db=1)
WORKFLOW_RUNNING_KEY = "workflow_running"
CURRENT_PRICE_RUNNING_KEY = "current_price_running"
LAST_WORKFLOW_RUN_KEY = "last_workflow_run"


@shared_task
def run_workflow():
    # Mark workflow as running
    if redis_client.get(CURRENT_PRICE_RUNNING_KEY):
        print("Current price flow is running. Delaying `run_workflow`...")
        return

    redis_client.set(
        WORKFLOW_RUNNING_KEY,
        "1",
    )  # No timeout to track workflow running
    time.sleep(61)
    try:
        # workflow = chain(
        #     # terminate_all_connections.s(),
        #     drop_tables.s(),
        #     tickers_data.s(),
        #     tickers_financial_stmts_data.s(),
        #     tickers_prices_data.s(),
        #     tickers_current_prices.s(),
        #     filter_ncav_candidates.s(),
        #     filter_epsx_candidates.s(),
        # )
        # workflow.apply()
        workflow.delay()
        # After completion, store the last run time
        redis_client.set(LAST_WORKFLOW_RUN_KEY, str(datetime.now()))
    except Exception as e:
        print(f"Workflow failed: {e}")
        raise
    finally:
        # Mark workflow as not running
        redis_client.delete(WORKFLOW_RUNNING_KEY)


@shared_task
def tickers_current_prices_wrapper():
    # Check if workflow is running
    if redis_client.get(WORKFLOW_RUNNING_KEY):
        print("Workflow is running. Delaying `tickers_current_prices`...")
        return  # Skip or reschedule based on requirement
    try:
        redis_client.set(
            CURRENT_PRICE_RUNNING_KEY, "1"
        )  # only because we have an api rate limit
        # Check if the last workflow was recent (e.g., within the last month)
        time.sleep(61)
        last_run = redis_client.get(LAST_WORKFLOW_RUN_KEY)
        if last_run:
            last_run = datetime.fromisoformat(last_run.decode())
            if last_run > datetime.now() - timedelta(days=30):
                print(
                    "Workflow recently completed. Running `tickers_current_prices`..."
                )
                tickers_current_prices_workflow.delay()  # Call the actual task
        else:
            print("Workflow hasn't completed recently. Waiting...")
    finally:
        redis_client.delete(CURRENT_PRICE_RUNNING_KEY)
