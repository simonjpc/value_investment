import concurrent.futures
import logging
import multiprocessing
import sys
import time
from typing import List

import pandas as pd
from sqlalchemy import create_engine, exc
from sqlalchemy.pool import QueuePool

from valuation.constants import (
    CREATE_INDEX_QUERY,
    FINANCIAL_STMT_DUMP_QUERY,
    FINANCIAL_STMT_TABLE_NAME,
    GET_ALL_DELISTED_TICKERS_QUERY,
    GET_ALL_LISTED_TICKERS_QUERY,
    INCOME_STMT_COLS_TO_DROP,
    TICKER_COL_NAME,
    TICKER_IDX_NAME,
    TICKERS_PATH_ANCIENT,
    TICKERS_PATH_RECENT,
)
from valuation.data_injection import Injector
from valuation.data_loading import DataLoader
from valuation.extraction import get_balance_sheet_info, get_income_stmt_info
from valuation.utils import add_suffix_to_cols, batch_tickers, dict_to_df, drop_df_cols
from celery_app import app

logging.basicConfig(stream=sys.stdout, level=logging.getLevelName("INFO"))
log = logging.getLogger(__name__)

injector = Injector()
engine = create_engine(
    injector.db_uri,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)


def single_ticker_pipeline(ticker: str):
    failed_ticker = None
    income_stmt = get_income_stmt_info(
        ticker=ticker,
        period="quarter",
        limit=120,
    )
    balance_sheet = get_balance_sheet_info(
        ticker=ticker,
        period="quarter",
        limit=120,
    )
    log.info("balance sheet & income stmt data loaded.")

    if not all([len(history) for history in (income_stmt, balance_sheet)]):
        return False, failed_ticker

    income_stmt_df = dict_to_df(fa_info=income_stmt)
    balance_sheet_df = dict_to_df(fa_info=balance_sheet)
    log.info("balance sheet & income stmt dicts transformed into df.")

    try:
        income_stmt_df = income_stmt_df.set_index("date")
        balance_sheet_df = balance_sheet_df.set_index("date")
    except:
        print(ticker)
    log.info("`date` col added as index.")

    income_stmt_df = drop_df_cols(
        income_stmt_df,
        cols=INCOME_STMT_COLS_TO_DROP,
    )
    log.info("repeated cols dropped from income statement source.")

    income_stmt_df = income_stmt_df[~income_stmt_df.index.duplicated(keep="first")]
    balance_sheet_df = balance_sheet_df[
        ~balance_sheet_df.index.duplicated(keep="first")
    ]
    log.info("rows with same index (date) dropped and only first kept.")

    income_stmt_df = add_suffix_to_cols(df=income_stmt_df, suffix="_is")
    balance_sheet_df = add_suffix_to_cols(df=balance_sheet_df, suffix="_bs")
    log.info("balance sheet & income stmt df cols modified with suffixes.")

    financial_info = pd.concat([balance_sheet_df, income_stmt_df], axis=1)
    financial_info = financial_info.reset_index()
    log.info("concatenation succeeded.")

    try:
        injector.df_dump(df=financial_info, engine=engine)
    except:
        failed_ticker = ticker
        # print("ticker: ", ticker)
        # raise("data dump failed")
        log.info(f"data dump failed for {ticker}.")
    log.info(f"data dump successful for {ticker}.")
    engine.dispose()
    return True, failed_ticker


# @app.task()
def tickers_financial_stmts_data():

    log.info("starting...")
    dataloader = DataLoader()
    injector = Injector()

    connection = engine.connect()

    # data loading
    tickers_recent = pd.read_sql(GET_ALL_LISTED_TICKERS_QUERY, connection)
    tickers_recent = tickers_recent["ticker"].tolist()
    tickers_ancient = pd.read_sql(GET_ALL_DELISTED_TICKERS_QUERY, connection)
    tickers_ancient = tickers_ancient["ticker"].tolist()
    tickers = list(set(tickers_recent + tickers_ancient))

    # batches creation
    ticker_batches = batch_tickers(tickers=tickers, batch_size=90)
    log.info("tickers loaded and batches created")

    try:
        # create table
        injector.execute_query(
            FINANCIAL_STMT_DUMP_QUERY.format(
                table_name=FINANCIAL_STMT_TABLE_NAME,
            ),
            connection,
        )
        # create index
        injector.execute_query(
            CREATE_INDEX_QUERY.format(
                index_name=TICKER_IDX_NAME,
                table_name=FINANCIAL_STMT_TABLE_NAME,
                column_name=TICKER_COL_NAME,
            ),
            connection,
        )

        # Multiprocessing
        # We execute this per batch considering the limit of the api
        dfc = []
        for idx, batch in enumerate(ticker_batches):
            log.info(
                f"Starting batch {idx + 1}/{len(ticker_batches)} with {len(batch)} tickers..."
            )

            with concurrent.futures.ThreadPoolExecutor() as executor:
                dumping_futures = [
                    executor.submit(single_ticker_pipeline, ticker) for ticker in batch
                ]
                for future in concurrent.futures.as_completed(dumping_futures):
                    dumping_output = future.result()
                    dumping_flag = dumping_output[0]
                    failed_ticker = dumping_output[1]
                    if failed_ticker is not None:
                        dfc.append(failed_ticker)

            log.info(f"batch {idx + 1} executed")
            log.info(f"waiting 1 min...")
            time.sleep(61)

    except exc.SQLAlchemyError as e:
        print(f"An error occurred: {e}")

    finally:
        connection.close()
        engine.dispose()
    print()
    print(f"Ticker with failed DB dump: {dfc}")


if __name__ == "__main__":
    # create table if it does not exist
    tickers_financial_stmts_data()
