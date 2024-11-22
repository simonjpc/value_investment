import sys
import time
import numpy as np
import pandas as pd
from valuation.data_injection import Injector
from valuation.extraction import get_current_price
from valuation.utils import batch_tickers, handling_negative_vals
from sqlalchemy import create_engine, exc
from sqlalchemy.pool import QueuePool
import concurrent.futures
import logging
from valuation.constants import (
    GET_N_LAST_FINANCIAL_STMT_PER_SYMBOL_QUERY,
    POTENTIAL_PFV_CANDIDATES_DUMP_QUERY,
    POTENTIAL_PFV_CANDIDATES_TABLE_NAME,
    POTENTIAL_PFV_CANDIDATES_IDX_NAME,
    POTENTIAL_PFV_CANDIDATES_TICKER_COL_NAME,
    GET_LAST_FINANCIAL_STMT_PER_SYMBOL_QUERY,
)
from valuation.eps_multiple import (
    compute_growth,
    get_reporting_window,
    compute_avg_value,
    compute_pex_value,
)

logging.basicConfig(stream=sys.stdout, level=logging.getLevelName("INFO"))
log = logging.getLogger(__name__)


injector = Injector()
engine = create_engine(
    injector.db_uri, poolclass=QueuePool, pool_size=10, max_overflow=20
)


def single_ticker_candidacy_pipeline(
    ticker: str, return_value: float = 0.2, years: int = 10
):
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
            GET_N_LAST_FINANCIAL_STMT_PER_SYMBOL_QUERY.format(ticker=ticker, limit=10),
            connection,
        )
        df = df.rename(columns={"eps_is": "eps"})
    if len(df) < 5:
        return None
    all_equity = df["totalStockholdersEquity_bs"].tolist()

    growths = []
    for nb_years in range(5, len(all_equity) + 1):  # 6, 7, 8, 9]:
        single_growth = compute_growth(
            all_equity[0], all_equity[nb_years - 1], nb_years - 1
        )
        growths.append(single_growth)
    growth_value = np.median(growths)
    if np.isnan(growth_value) or growth_value == np.nan or growth_value < 0:
        return None

    # compute future pe ratio
    all_prices = []
    for _, single_income_stmt in df.iterrows():
        reporting_start, reporting_end, filling_date_flag = get_reporting_window(
            single_income_stmt
        )

        prices_hist_query = f"select * from prices_history where symbol = '{ticker}'"
        with engine.connect() as connection:
            prices_hist_df = pd.read_sql(prices_hist_query, connection)

        try:
            range_price_lows = prices_hist_df["low"].tolist()
            avg_price_at_report = compute_avg_value(range_price_lows)
        except:
            avg_price_at_report = 0
        all_prices.append(avg_price_at_report)

    all_eps = df["eps"].tolist()
    all_eps = [val if val != 0 and not np.isnan(val) else 1e-6 for val in all_eps]
    historical_pe = list(np.array(all_prices) / np.array(all_eps))
    historical_pe = handling_negative_vals(historical_pe)
    future_pe = compute_avg_value(historical_pe)
    if future_pe <= 0:
        return None
    pfvps = compute_pex_value(df.iloc[0], growth_value, return_value, future_pe, years)

    current_price = get_current_price(ticker)

    if current_price is None:
        return None

    # filter by value
    if current_price > pfvps:
        return None

    pfv_mos = round(100 * (pfvps - current_price) / pfvps, 2)
    if pfv_mos < 33 or pfv_mos > 95:
        return None

    candidate_info = pd.DataFrame(
        [[ticker, current_price, pfvps, pfv_mos, currency]],
        columns=["ticker", "current_price", "pfvps", "pfv_mos", "currency"],
    )
    injector.df_to_db(
        df=candidate_info,
        table_name=POTENTIAL_PFV_CANDIDATES_TABLE_NAME,
        conn=engine,
    )
    return True


if __name__ == "__main__":

    injector = Injector()

    connection = engine.connect()
    query = """select * from financial_stmts"""
    tickers_recent = pd.read_sql(query, connection)
    # tickers_recent = pd.read_sql(GET_ALL_LISTED_TICKERS_QUERY, connection)
    tickers = list(set(tickers_recent["symbol_bs"].tolist()))
    tickers = [ticker for ticker in tickers if ticker and "." not in ticker]
    ticker_batches = batch_tickers(tickers=tickers, batch_size=290)

    try:
        # create table
        injector.execute_query(
            POTENTIAL_PFV_CANDIDATES_DUMP_QUERY.format(
                table_name=POTENTIAL_PFV_CANDIDATES_TABLE_NAME,
            ),
            connection,
        )
        # create index
        injector.execute_query(
            POTENTIAL_PFV_CANDIDATES_DUMP_QUERY.format(
                index_name=POTENTIAL_PFV_CANDIDATES_IDX_NAME,
                table_name=POTENTIAL_PFV_CANDIDATES_TABLE_NAME,
                column_name=POTENTIAL_PFV_CANDIDATES_TICKER_COL_NAME,
            ),
            connection,
        )
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
