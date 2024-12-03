import sys
import time
import numpy as np
import pandas as pd
import sqlalchemy
import concurrent.futures
from sqlalchemy import create_engine, exc
from sqlalchemy.pool import QueuePool
from typing import List, Dict, Any
from datetime import datetime
from valuation.constants import (
    CREATE_INDEX_QUERY,
    OLDEST_AND_NEWEST_FILLING_DATES_PER_SYMBOL_QUERY,
    PRICES_INFO_COLUMNS,
    PRICES_HISTORY_TABLE_NAME,
    DAILY_PRICES_HISTORY_DUMP_QUERY,
    HIST_PRICES_DATE_COL,
)
from valuation.data_injection import Injector
from valuation.extraction import get_prices_in_range
from valuation.utils import (
    compute_offset_date,
    df_to_list,
    weekday_from_date,
    batch_tickers,
)
from tasks.celery_app import app
import logging

logging.basicConfig(stream=sys.stdout, level=logging.getLevelName("INFO"))
log = logging.getLogger(__name__)

injector = Injector()
engine = create_engine(
    injector.db_uri,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)


def all_symbols_oldest_and_newest_dates(
    query: str,
    connection: sqlalchemy.engine,
) -> pd.DataFrame:
    df = pd.read_sql(query, con=connection)
    return df


def single_ticker_prices_history_pipeline(
    ticker: str,
    oldest_report_date: str,
    newest_report_date: str,
) -> None:
    # compute offset of newest date -> this is not really necessary
    offset_date = compute_offset_date(newest_report_date)
    oldest_report_date = str(oldest_report_date.date())
    offset_date = str(offset_date)
    # get prices data
    prices_history = get_prices_in_range(
        ticker,
        oldest_report_date,
        offset_date,
    )
    # preprocess prices data (formatting, new computations, etc)
    preprocessed_prices = preprocess_raw_prices(prices_history)
    # dump data into table
    injector.df_to_db(
        df=preprocessed_prices,
        table_name=PRICES_HISTORY_TABLE_NAME,
        conn=engine,
    )
    return True


def drop_rows_with_empty_vals_in(
    df: pd.DataFrame,
    cols: List[str],
) -> pd.DataFrame:
    return df.dropna(subset=cols)


def preprocess_raw_prices(prices_structure: Dict[str, Any]) -> pd.DataFrame:
    prices = get_pertinent_keys(prices_structure=prices_structure)
    prices_df = pd.DataFrame(prices, columns=PRICES_INFO_COLUMNS)
    return prices_df


def get_pertinent_keys(prices_structure: Dict[str, Any]) -> List[str]:
    all_price_info = []
    historical_prices = prices_structure.get("historical", None)
    if historical_prices is None:
        return
    for element in historical_prices:
        (
            date,
            low_price,
            high_price,
            open_price,
            close_price,
            volume,
            symbol,
        ) = (
            element.get("date", None),
            element.get("low", None),
            element.get("high", None),
            element.get("open", None),
            element.get("close", None),
            element.get("volume", None),
            prices_structure.get("symbol", None),
        )
        weekday = weekday_from_date(date)  # cheating
        all_price_info.append(
            [
                date,
                weekday,
                symbol,
                low_price,
                high_price,
                open_price,
                close_price,
                volume,
            ]
        )
    return all_price_info


@app.task()
def tickers_prices_data(
    self,
):

    connection = engine.connect()
    oldest_and_newest_date = all_symbols_oldest_and_newest_dates(
        query=OLDEST_AND_NEWEST_FILLING_DATES_PER_SYMBOL_QUERY,
        connection=connection,
    )
    oldest_and_newest_date = drop_rows_with_empty_vals_in(
        df=oldest_and_newest_date,
        cols=["symbol_bs", "fillingdate_oldest"],
    )
    oldest_and_newest_date.loc[
        pd.isna(oldest_and_newest_date["fillingdate_newest"]),
        "fillingdate_newest",
    ] = str(datetime.today().date())

    dates_per_ticker_iter = df_to_list(oldest_and_newest_date)
    batches = batch_tickers(tickers=dates_per_ticker_iter, batch_size=90)
    # create table
    try:
        injector.execute_query(
            DAILY_PRICES_HISTORY_DUMP_QUERY.format(
                table_name=PRICES_HISTORY_TABLE_NAME
            ),
            connection=connection,
        )

        injector.execute_query(
            CREATE_INDEX_QUERY.format(
                index_name="ticker_in_price_hist_idx",
                table_name=PRICES_HISTORY_TABLE_NAME,
                column_name="symbol",
            ),
            connection=connection,
        )
        for idx, batch in enumerate(batches):
            log.info(
                f"Starting batch {idx + 1}/{len(batches)} with {len(batch)} tickers..."
            )
            with concurrent.futures.ThreadPoolExecutor() as executor:
                dumping_futures = [
                    executor.submit(
                        single_ticker_prices_history_pipeline,
                        element[0],
                        element[1],
                        element[2],
                    )
                    for element in batch
                ]
                for future in concurrent.futures.as_completed(dumping_futures):
                    dumping_flag = future.result()
            log.info(f"batch {idx + 1} executed")
            log.info(f"waiting 1 min...")
            time.sleep(61)

    except exc.SQLAlchemyError as e:
        print(f"An error occurred: {e}")

    finally:
        connection.close()
        engine.dispose()


if __name__ == "__main__":

    tickers_prices_data()
