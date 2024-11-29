from valuation.pipeline_current_prices import tickers_current_prices
from valuation.pipeline_drop_all_tables import drop_tables
from valuation.pipeline_prices_data import tickers_prices_data
from valuation.pipeline_stmts_data import tickers_financial_stmts_data
from valuation.pipeline_tickers import tickers_data
from valuation.pipeline_drop_db_connections import terminate_all_connections
from valuation.pipeline_potential_epsx_candidates import filter_epsx_candidates
from valuation.pipeline_potential_ncav_candidates import filter_ncav_candidates
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

# # Send the task
# result = drop_tables.delay()

# # Monitor its execution
# print(f"Task ID: {result.id}")
