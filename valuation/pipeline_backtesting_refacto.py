"""
This script is created with the intention of extracting information
of the yields of companies considered under a mos based on some valuation
method such as ncav/liqv or eps multiples
"""

import concurrent.futures
import logging
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, exc, text
from sqlalchemy.pool import QueuePool

from valuation.constants import (BACKTESTING_OUTPUT_QUERY,
                                 BACKTESTING_TABLE_NAME, CREATE_INDEX_QUERY,
                                 CURRENT_ASSETS_FACTORS)
from valuation.data_injection import Injector
from valuation.liquidation import compute_liqvps, compute_ncavps
from valuation.utils import batch_tickers

logging.basicConfig(
    stream=sys.stdout, level=logging.getLevelName("INFO")
)
log = logging.getLogger(__name__)

injector = Injector()
engine = create_engine(injector.db_uri, poolclass=QueuePool, pool_size=10, max_overflow=20)

ticker_type = "delisted" # listed or delisted

ticker_type_hashmap = {
    "listed": "company_tickers",
    "delisted": "delisted_company_tickers",
}


# Table with all info
output_df = pd.DataFrame(
    columns=[
        "ticker",
        "ref_report_date",
        "report_date",
        "ref_report_date_quarter",
        "report_date_quarter",
        "outs_shares1",
        "outs_shares2",
        "outs_shares3",
        "outs_shares4",
        "outs_shares5",
        "outs_shares6",
        "outs_shares7",
        "outs_shares8",
        "outs_shares9",
        "outs_shares10",
        "outs_shares_slope_pct_10y",
        "outs_shares_slope_pct_5y",
        "min_price_date",
        "min_price",
        "max_price_date",
        "max_price",
        "ncavps",
        "liqvps",
        "ncav_mos",
        "liqv_mos",
        "highest_return_delay",
        "doubling_price",
        "doubling_date",
        "doubling_return_delay",
        "highest_return",
        "min_price_modif",
        "max_price_modif",
        "ncav_mos_modif",
        "liqv_mos_modif",
        "doubling_price_modif",
        "highest_return_modif",
        "ticker_type",
    ]
)

MODIF_CONSTANT = 0.20 # 20% arbitrary return reduction

# --------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------

def single_ticker_backtest(test_symbol):
    query = f"""
    SELECT "fillingDate_bs", period_bs
    FROM financial_stmts
    WHERE symbol_bs = '{test_symbol}'
    """

    offset_3y = None # no date for 3y offset in the beginning
    doubled = True # doubled return flag as True by default
    return_time_days = None #

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    df = df.sort_values(by="fillingDate_bs", ascending=True)

    dates = df["fillingDate_bs"].tolist()
    periods = df["period_bs"].tolist()
    single_ticker_df = pd.DataFrame()

    for i, date in enumerate(dates):
        if offset_3y is not None and not doubled:
            if date.date() < offset_3y:
                continue
            doubled = True
            offset_3y = None

        if return_time_days is not None:
            if date.date() < highest_date:
                continue
            return_time_days = None
        # get stmts from oldest until oldest + 10 years from the same quarter
        if len(df) == 0:
            continue
        #oldest_date, oldest_period = df.loc[0, "fillingDate_bs"], df.loc[0, "period_bs"]

        # ----------------------------------------------------------------
        oldest_date, oldest_period = date, periods[i]
        if oldest_date is None:
            continue
        # ----------------------------------------------------------------

        offset = 10*365 # 10 years
        offset_date = (oldest_date + pd.DateOffset(days=offset)).date()
        if offset_date > datetime.today().date():
            offset_date = datetime.today().date()
        oldest_date = oldest_date.date()
        
        query = f"""
        select *
        from financial_stmts
        where symbol_bs = '{test_symbol}' and
            period_bs = '{oldest_period}' and
            "fillingDate_bs" >= '{oldest_date}' and
            "fillingDate_bs" <= '{offset_date}'
        """

        with engine.connect() as connection:
            same_period_hist_df = pd.read_sql(query, connection)
        # this could have no output if the filling period is not the same throughtout the 10 years
        same_period_hist_df = same_period_hist_df.sort_values("date")

        # Compute valuation with info from fillingDate_bs of oldest + 10 years
        # (most recent row of `same_period_hist_df`)
        cols = list(same_period_hist_df.columns)
        cols = [col.split("_")[0] for col in cols]
        same_period_hist_df.columns = cols

        offset_date_financials = same_period_hist_df[
            same_period_hist_df["fillingDate"] == max(same_period_hist_df["fillingDate"])
        ]
        #print(test_symbol)
        #print()
        ncavps = compute_ncavps(offset_date_financials.to_dict("records")[0])
        liqvps = compute_liqvps(
            offset_date_financials.to_dict("records")[0],
            factors=CURRENT_ASSETS_FACTORS
        )

        # Get prices from the least oldest stmt til the day before the following stmt
        offset_date_financials = offset_date_financials.reset_index(drop=True)
        least_oldest_date = offset_date_financials.loc[0, "date"]

        query = f"""
        SELECT date, "fillingDate_bs", period_bs
        FROM financial_stmts
        WHERE date > '{least_oldest_date}' and symbol_bs = '{test_symbol}'
        ORDER BY date
        LIMIT 1;
        """
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)

        if len(df) == 0:
            continue

        next_filling_date = df.loc[0, "fillingDate_bs"].date()
        plateau_date = (next_filling_date - pd.DateOffset(days=1)).date()
        next_filling_date, plateau_date

        query = f"""
        select *
        from prices_history
        where symbol = '{test_symbol}' and date >= '{least_oldest_date}' and date <= '{plateau_date}'
        """
        with engine.connect() as connection:
            prices_df = pd.read_sql(query, connection)

        if len(prices_df) == 0:
            continue

        fct = 1 # should be more like 0.5 when implemented in the script
        prices_df[prices_df["low"] < ncavps * fct]

        # Compute slope in percentage values of shares outstanding during the last 10 years (same quarter)
        same_period_hist_df = same_period_hist_df[::-1]
        y = same_period_hist_df.loc[~pd.isna(same_period_hist_df["weightedAverageShsOutDil"]), "weightedAverageShsOutDil"]
        x = range(len(y))
        if len(y) < 2:
            continue
        slope, y_intercept = np.polyfit(
            x, y, 1,
        )
        #y_5y = same_period_hist_df.tail(5).loc[~pd.isna(same_period_hist_df.tail(5)["weightedAverageShsOutDil"]), "weightedAverageShsOutDil"]
        y_5y = same_period_hist_df.head(5).loc[~pd.isna(same_period_hist_df.head(5)["weightedAverageShsOutDil"]), "weightedAverageShsOutDil"]

        x_5y = range(len(y_5y))
        if len(y_5y) < 2:
            continue
        slope_5y, y_intercept_5y = np.polyfit(
            x_5y,
            y_5y,
            1,
        )
        start, end = (slope * x + y_intercept)[0], (slope * x + y_intercept)[-1]
        start_5y, end_5y = (slope_5y * x_5y + y_intercept_5y)[0], (slope_5y * x_5y + y_intercept_5y)[-1]

        slope_percentage = (end - start) / start
        #slope_percentage = (y.iloc[0] - y.iloc[-1]) / y.iloc[-1]
        slope_percentage_5y = (end_5y - start_5y) / start_5y
        #slope_percentage_5y = (y_5y.iloc[0] - y_5y.iloc[-1]) / y_5y.iloc[-1]

        print(f"slope_percentage for {test_symbol}")
        print(slope_percentage)
        print(f"slope_percentage_5y for {test_symbol}")
        print(slope_percentage_5y)
        print("same_period_hist_df")
        print(same_period_hist_df.head())
        print("y")
        print(y)
        print()
        print("y_5y")
        print(y_5y)
        print()
        quit()
        # Check if price in the future goes up after buying time
        oldest_lowest_date, oldest_lowest_price = (
            prices_df.loc[prices_df["low"] == min(prices_df["low"]), "date"].iloc[-1],
            prices_df.loc[prices_df["low"] == min(prices_df["low"]), "low"].iloc[-1]
        )
        offset_3y = (oldest_lowest_date + pd.DateOffset(days=3*365)).date()

        # if lowest price above ncav, it's overpriced
        if oldest_lowest_price > ncavps:
            continue

        query = f"""
        select *
        from prices_history
        where date >= '{oldest_lowest_date}' and date <= '{offset_3y}' and symbol = '{test_symbol}'
        """

        with engine.connect() as connection:
            maybe_up_df = pd.read_sql(query, connection)
        
        highest_date, highest_price = (
            maybe_up_df.loc[maybe_up_df["high"] == max(maybe_up_df["high"]), "date"].iloc[0],
            maybe_up_df.loc[maybe_up_df["high"] == max(maybe_up_df["high"]), "high"].iloc[0],
        )

        # Percentage of return
        return_percentage = (highest_price - oldest_lowest_price) / oldest_lowest_price

        # Date of return
        return_time_days = (highest_date - oldest_lowest_date).days
        return_time_months = round(return_time_days / 30, 2)
        return_time_years = round(return_time_days / 365, 2)

        # Time to realize 100% of return
        expected_return = oldest_lowest_price * 2

        query = f"""
        SELECT *
        FROM prices_history
        WHERE high > {expected_return} and symbol = '{test_symbol}' and date >= '{oldest_lowest_date}' and date <= '{offset_3y}'
        ORDER BY high
        LIMIT 1;
        """
        with engine.connect() as connection:
            doubled_return_df = pd.read_sql(query, connection)

        connection.close()
        engine.dispose()
        if len(doubled_return_df) > 0:
            doubled_return_date = doubled_return_df.loc[0, "date"]
            doubled_return_days = (doubled_return_date - oldest_lowest_date).days
            doubled_return_months = round(doubled_return_days / 30, 2)
            doubled_return_years = round(doubled_return_days / 365, 2)
        else:
            doubled_return_date = None
            doubled_return_years = None
            doubled = False
        tmp_df = pd.DataFrame(
            data=[
                [
                    test_symbol,
                    oldest_date,#df.loc[0, "fillingDate_bs"]
                    offset_date_financials.loc[0, "fillingDate"],
                    oldest_period,#df.loc[0, "period_bs"]
                    offset_date_financials.loc[0, "period"],
                    same_period_hist_df.reset_index().loc[0, "weightedAverageShsOutDil"] if same_period_hist_df.reset_index().loc[0, "weightedAverageShsOutDil"] else None,
                    same_period_hist_df.reset_index().loc[1, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 2 else None,
                    same_period_hist_df.reset_index().loc[2, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 3 else None,
                    same_period_hist_df.reset_index().loc[3, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 4 else None,
                    same_period_hist_df.reset_index().loc[4, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 5 else None,
                    same_period_hist_df.reset_index().loc[5, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 6 else None,
                    same_period_hist_df.reset_index().loc[6, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 7 else None,
                    same_period_hist_df.reset_index().loc[7, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 8 else None,
                    same_period_hist_df.reset_index().loc[8, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 9 else None,
                    same_period_hist_df.reset_index().loc[9, "weightedAverageShsOutDil"] if len(same_period_hist_df) >= 10 else None,
                    round(slope_percentage * 100, 2),
                    round(slope_percentage_5y * 100, 2),
                    oldest_lowest_date,
                    oldest_lowest_price,
                    highest_date,
                    highest_price,
                    ncavps,
                    liqvps,
                    round(100 * (ncavps - oldest_lowest_price) / ncavps, 2),
                    round(100 * (liqvps - oldest_lowest_price) / liqvps, 2),
                    return_time_years, #round(return_time_days / 365, 2),
                    oldest_lowest_price * 2,
                    doubled_return_date, #doubled_return_df.loc[0, "date"] if len(doubled_return_df) > 0 else None,
                    doubled_return_years, #round(doubled_return_days / 365, 2) if doubled_return_days is not None else None,
                    round(return_percentage * 100, 2),
                    oldest_lowest_price * (1 + MODIF_CONSTANT),
                    highest_price * (1 - MODIF_CONSTANT),
                    round(100 * (ncavps - oldest_lowest_price * (1 + MODIF_CONSTANT)) / ncavps, 2),
                    round(100 * (liqvps - oldest_lowest_price * (1 + MODIF_CONSTANT)) / liqvps, 2),
                    oldest_lowest_price * (1 + MODIF_CONSTANT),
                    round((highest_price * (1 - MODIF_CONSTANT) - oldest_lowest_price * (1 + MODIF_CONSTANT)) * 100 / oldest_lowest_price * (1 + MODIF_CONSTANT), 2),
                    ticker_type,
                ]
            ],
            columns=[
                "ticker",
                "ref_report_date",
                "report_date",
                "ref_report_date_quarter",
                "report_date_quarter",
                "outs_shares1",
                "outs_shares2",
                "outs_shares3",
                "outs_shares4",
                "outs_shares5",
                "outs_shares6",
                "outs_shares7",
                "outs_shares8",
                "outs_shares9",
                "outs_shares10",
                "outs_shares_slope_pct_10y",
                "outs_shares_slope_pct_5y",
                "min_price_date",
                "min_price",
                "max_price_date",
                "max_price",
                "ncavps",
                "liqvps",
                "ncav_mos",
                "liqv_mos",
                "highest_return_delay",
                "doubling_price",
                "doubling_date",
                "doubling_return_delay",
                "highest_return",
                "min_price_modif",
                "max_price_modif",
                "ncav_mos_modif",
                "liqv_mos_modif",
                "doubling_price_modif",
                "highest_return_modif",
                "ticker_type",
            ]
        )

        single_ticker_df = pd.concat([single_ticker_df, tmp_df], axis=0)
    return single_ticker_df

if __name__ == "__main__":
    query = f"""
    select *
    from {ticker_type_hashmap[ticker_type]}
    """

    with engine.connect() as connection:
        tickers_df = pd.read_sql(query, connection)

    tickers_list = tickers_df["ticker"].tolist()

    """filtered_tickers = [
        ticker for ticker in tickers_list if (
            "." not in ticker and
            "-" not in ticker and
            "+" not in ticker and
            "^" not in ticker and
            "~" not in ticker
        )
    ]"""

    filtered_tickers = [ticker for ticker in tickers_list]

    batches = batch_tickers(tickers=filtered_tickers, batch_size=60)

    """try:
        drop_query = "DROP TABLE backtesting_output;"
        with engine.connect() as connection:
            connection.execute(text(drop_query))
            connection.commit()
    except:
        pass"""

    connection = engine.connect()

    try:
        injector.execute_query(
            BACKTESTING_OUTPUT_QUERY.format(
                table_name=BACKTESTING_TABLE_NAME,
            ),
            connection,
        )

        injector.execute_query(
            query=CREATE_INDEX_QUERY.format(
                index_name="ticker_symbol_index",
                table_name=BACKTESTING_TABLE_NAME,
                column_name="ticker",
            ),
            connection=connection,
        )
        #connection.close()
        for idx, batch in enumerate(batches):
            log.info(f"Starting batch {idx + 1}/{len(batches)} with {len(batch)} tickers...")
            batch_df = pd.DataFrame()
            with concurrent.futures.ProcessPoolExecutor() as executor:
                dumping_futures = [
                    executor.submit(
                        single_ticker_backtest,
                        ticker,
                    ) for ticker in batch[:500]
                ]
                for future in concurrent.futures.as_completed(dumping_futures):
                    single_ticker_df = future.result()
                    batch_df = pd.concat([batch_df, single_ticker_df], axis=0)
            output_df = pd.concat([output_df, batch_df], axis=0)
            log.info(f"batch {idx + 1} executed")
            #time.sleep(61)

        output_df = output_df.reset_index(drop=True)

        #with engine.connect() as connection:
        injector.df_to_db(
            df=output_df,
            table_name=BACKTESTING_TABLE_NAME,
            conn=connection,
        )

        #engine.dispose()

    except exc.SQLAlchemyError as e:
        print(f"An error occurred: {e}")

    finally:
        connection.close()
        engine.dispose()
        
    log.info("all batches successfully executed.")
