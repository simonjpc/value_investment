import sys
import time
import numpy as np
import pandas as pd
from valuation.data_injection import Injector
from sqlalchemy import create_engine, exc
from sqlalchemy.pool import QueuePool
from valuation.constants import (
    GET_LAST_FINANCIAL_STMT_PER_SYMBOL_QUERY,
    GET_FINANCIAL_STMT_PER_SYMBOL_AND_PERIOD_QUERY,
    RATES_TO_USD,
    POTENTIAL_NCAV_CANDIDATES_IDX_NAME,
    POTENTIAL_NCAV_CANDIDATES_TABLE_NAME,
    POTENTIAL_NCAV_CANDIDATES_TICKER_COL_NAME,
    POTENTIAL_NCAV_CANDIDATES_DUMP_QUERY,
)
from valuation.liquidation import compute_ncavps
from valuation.utils import currency_to_usd, batch_tickers, compute_change_percentage
from valuation.extraction import get_current_price
import concurrent.futures
import logging

logging.basicConfig(stream=sys.stdout, level=logging.getLevelName("INFO"))
log = logging.getLogger(__name__)


injector = Injector()
engine = create_engine(
    injector.db_uri, poolclass=QueuePool, pool_size=10, max_overflow=20
)


def single_ticker_candidacy_pipeline(ticker: str):

    with engine.connect() as connection:
        df = pd.read_sql(
            GET_LAST_FINANCIAL_STMT_PER_SYMBOL_QUERY.format(ticker=ticker), connection
        )
    if len(df) == 0:
        return None
    currency = df.loc[0, "reportedCurrency_bs"]
    period = df.loc[0, "period_bs"]
    if period is None:
        return None

    with engine.connect() as connection:
        df = pd.read_sql(
            GET_FINANCIAL_STMT_PER_SYMBOL_AND_PERIOD_QUERY.format(
                ticker=ticker, period=period
            ),
            connection,
        )

    cols = list(df.columns)
    cols = [col.split("_")[0] for col in cols]
    df.columns = cols
    df = df[::-1]
    y = df.loc[
        ~pd.isna(df["weightedAverageShsOutDil"]), "weightedAverageShsOutDil"
    ].tail(10)

    slope_percentage = compute_change_percentage(y)
    if slope_percentage is None or slope_percentage > 0.2:
        return None
    y_5y = df.loc[
        ~pd.isna(df["weightedAverageShsOutDil"]), "weightedAverageShsOutDil"
    ].tail(5)

    slope_percentage_5y = compute_change_percentage(y_5y)
    if slope_percentage_5y is None or slope_percentage_5y > 0.2:
        return None

    # get ncav and liqv
    last_date_financials = df[df["fillingDate"] == max(df["fillingDate"])]
    ncavps = compute_ncavps(last_date_financials.to_dict("records")[0])
    if np.isnan(ncavps):
        return None
    ncavps = currency_to_usd(ncavps, currency, RATES_TO_USD)
    if ncavps is None:
        return None
    # get current price
    current_price = get_current_price(ticker)

    if current_price is None:
        return None

    # filter by value
    if current_price > ncavps:
        return None

    ncav_mos = round(100 * (ncavps - current_price) / ncavps, 2)
    if ncav_mos < 33 or ncav_mos > 95:
        return None
    candidate_info = pd.DataFrame(
        [[ticker, current_price, ncavps, ncav_mos, currency]],
        columns=["ticker", "current_price", "ncavps", "ncav_mos", "currency"],
    )
    injector.df_to_db(
        df=candidate_info,
        table_name=POTENTIAL_NCAV_CANDIDATES_TABLE_NAME,
        conn=engine,
    )
    return True


def filter_ncav_candidates():

    injector = Injector()

    connection = engine.connect()
    query = """select * from financial_stmts"""
    tickers_recent = pd.read_sql(query, connection)
    # tickers_recent = pd.read_sql(GET_ALL_LISTED_TICKERS_QUERY, connection)
    tickers = list(set(tickers_recent["symbol_bs"].tolist()))
    tickers = [ticker for ticker in tickers if ticker and "." not in ticker]
    # batches creation
    ticker_batches = batch_tickers(tickers=tickers, batch_size=290)
    try:
        # create table
        injector.execute_query(
            POTENTIAL_NCAV_CANDIDATES_DUMP_QUERY.format(
                table_name=POTENTIAL_NCAV_CANDIDATES_TABLE_NAME,
            ),
            connection,
        )
        # create index
        injector.execute_query(
            POTENTIAL_NCAV_CANDIDATES_DUMP_QUERY.format(
                index_name=POTENTIAL_NCAV_CANDIDATES_IDX_NAME,
                table_name=POTENTIAL_NCAV_CANDIDATES_TABLE_NAME,
                column_name=POTENTIAL_NCAV_CANDIDATES_TICKER_COL_NAME,
            ),
            connection,
        )

        # Multiprocessing
        # We execute this per batch considering the limit of the api
        for idx, batch in enumerate(ticker_batches):
            log.info(
                f"Starting batch {idx + 1}/{len(ticker_batches)} with {len(batch)} tickers..."
            )

            with concurrent.futures.ProcessPoolExecutor() as executor:
                dumping_futures = [
                    executor.submit(single_ticker_candidacy_pipeline, ticker)
                    for ticker in batch
                ]
                for future in concurrent.futures.as_completed(dumping_futures):
                    dumping_output = future.result()

            log.info(f"batch {idx + 1} executed")
            log.info(f"waiting 1 min...")
            time.sleep(61)

    except exc.SQLAlchemyError as e:
        print(f"An error occurred: {e}")

    finally:
        connection.close()
        engine.dispose()

    log.info("all batches executed")


if __name__ == "__main__":

    filter_ncav_candidates()
