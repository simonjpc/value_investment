import sys
import pandas as pd
import concurrent.futures
import time
from sqlalchemy import create_engine, exc
from sqlalchemy.pool import QueuePool
from valuation.constants import (
    CURRENT_PRICES_TABLE_QUERY,
    CREATE_INDEX_QUERY,
    CURRENT_PRICES_TABLE_NAME,
)
from valuation.extraction import get_current_price
from valuation.data_injection import Injector
from valuation.utils import batch_tickers
import logging
from valuation.constants import (
    ALL_TICKERS_QUERY,
    TICKERS_FROM_FINANCIAL_STMTS_QUERY,
)
from tasks.celery_app import app

logging.basicConfig(stream=sys.stdout, level=logging.getLevelName("INFO"))
log = logging.getLogger(__name__)

injector = Injector()
engine = create_engine(
    injector.db_uri,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)


def current_ticker_price_df(ticker: str, table_name: str) -> pd.DataFrame:
    current_price = get_current_price(ticker)
    if current_price is None:
        single_ticker_current_price_df = pd.DataFrame(
            {"ticker": [ticker], "price": [None]}
        )
    else:
        single_ticker_current_price_df = pd.DataFrame(
            {"ticker": [ticker], "price": [current_price]}
        )
    injector.df_to_db(
        df=single_ticker_current_price_df,
        table_name=table_name,
        conn=engine,
    )
    return True


@app.task()
def tickers_current_prices(
    self,
):
    with engine.connect() as connection:
        df = pd.read_sql(TICKERS_FROM_FINANCIAL_STMTS_QUERY, connection)

    connection = engine.connect()
    logging.info("all tickers fetched")
    all_tickers = df["symbol_bs"].tolist()
    all_tickers = [ticker for ticker in all_tickers if ticker is not None]
    logging.info("tickers list created")

    batches = batch_tickers(tickers=all_tickers, batch_size=300)
    logging.info("batches created")

    try:
        injector.execute_query(
            CURRENT_PRICES_TABLE_QUERY.format(table_name=CURRENT_PRICES_TABLE_NAME),
            connection=connection,
        )

        injector.execute_query(
            CREATE_INDEX_QUERY.format(
                index_name="ticker_idx",
                table_name=CURRENT_PRICES_TABLE_NAME,
                column_name="ticker",
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
                        current_ticker_price_df,
                        ticker,
                        CURRENT_PRICES_TABLE_NAME,
                    )
                    for ticker in batch
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

    tickers_current_prices()
