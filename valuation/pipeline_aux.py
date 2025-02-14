from celery_app import app
from valuation.pipeline_tickers import tickers_data
from valuation.pipeline_drop_all_tables import drop_tables
from valuation.pipeline_prices_data import tickers_prices_data
from valuation.pipeline_current_prices import tickers_current_prices
from valuation.pipeline_stmts_data import tickers_financial_stmts_data
from valuation.pipeline_drop_db_connections import terminate_all_connections
from valuation.pipeline_potential_epsx_candidates import filter_epsx_candidates
from valuation.pipeline_potential_ncav_candidates import filter_ncav_candidates


@app.task
def workflow():
    try:
        terminate_all_connections()
        drop_tables()
        tickers_data()
        tickers_financial_stmts_data()
        tickers_prices_data()
        tickers_current_prices()
        filter_ncav_candidates()
        filter_epsx_candidates()
    except Exception as e:
        print(f"failed auxiliar workflow with error: {e}")


@app.task
def candidates_selection_workflow():
    try:
        tickers_current_prices()
        filter_ncav_candidates()
        filter_epsx_candidates()
    except Exception as e:
        print(f"failed auxiliar candidates selection workflow with error: {e}")
