from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from valuation.constants import CURRENT_ASSETS_FACTORS
from valuation.data_injection import Injector
from valuation.liquidation import compute_liqvps, compute_ncavps

injector = Injector()
engine = create_engine(injector.db_uri, poolclass=QueuePool, pool_size=10, max_overflow=20)

query = f"""
select *
from company_tickers
"""

with engine.connect() as connection:
    tickers_df = pd.read_sql(query, connection)

tickers_list = len(tickers_df["ticker"].tolist())

filtered_tickers = [
    ticker for ticker in tickers_list if (
        "." not in ticker and
        "-" not in ticker and
        "+" not in ticker and
        "^" not in ticker and
        "~" not in ticker
    )
]

# iterate on all symbols
for test_symbol in filtered_tickers:

    # get oldest stmt
    query = f"""
    WITH min_filling_date AS (
        SELECT MIN("fillingDate_bs") as filling_date_oldest
        FROM financial_stmts
        WHERE symbol_bs = '{test_symbol}'
    )
    SELECT "fillingDate_bs", period_bs
    FROM financial_stmts
    WHERE "fillingDate_bs" = (
        SELECT filling_date_oldest FROM min_filling_date
        )
        AND symbol_bs = '{test_symbol}';
    """

    with engine.connec() as connection:
        df = pd.read_sql(query, connection)

    # get stmts from oldest until oldest + 10 years from the same quarter

    oldest_date, oldest_period = df.loc[0, "fillingDate_bs"], df.loc[0, "period_bs"]
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

    # Compute valuation with info from fillingDate_bs of oldest + 10 years
    # (most recent row of `same_period_hist_df`)

    cols = list(same_period_hist_df.columns)
    cols = [col.split("_")[0] for col in cols]
    same_period_hist_df.columns = cols

    offset_date_financials = same_period_hist_df[
        same_period_hist_df["fillingDate"] == max(same_period_hist_df["fillingDate"])
    ]
    ncavps = compute_ncavps(offset_date_financials.to_dict("records")[0])
    liqvps = compute_liqvps(
        offset_date_financials.to_dict("records")[0],
        factors=CURRENT_ASSETS_FACTORS
    )

    # Get prices from the least oldest stmt til the day before the following stmt
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

    fct = 1 # should be more like 0.5 when implemented in the script
    prices_df[prices_df["low"] < ncavps * fct]

    # Compute slope in percentage values of shares outstanding during the last 10 years (same quarter)
    same_period_hist_df = same_period_hist_df[::-1]
    x = range(len(same_period_hist_df[~pd.isna(same_period_hist_df["weightedAverageShsOutDil"])]))
    slope, y_intercept = np.polyfit(
        x,
        same_period_hist_df.loc[~pd.isna(same_period_hist_df["weightedAverageShsOutDil"]), "weightedAverageShsOutDil"],
        1,
    )
    x_5y = range(5)
    slope_5y, y_intercept_5y = np.polyfit(
        x_5y,
        same_period_hist_df.tail(5).loc[~pd.isna(same_period_hist_df.tail(5)["weightedAverageShsOutDil"]), "weightedAverageShsOutDil"],
        1,
    )

    start, end = (slope * x + y_intercept)[0], (slope * x + y_intercept)[-1]
    start_5y, end_5y = (slope_5y * x_5y + y_intercept_5y)[0], (slope_5y * x_5y + y_intercept_5y)[-1]

    slope_percentage = (end - start) / start
    slope_percentage_5y = (end_5y - start_5y) / start_5y

    # Check if price in the future goes up after buying time

    oldest_lowest_date, oldest_lowest_price = (
        prices_df.loc[prices_df["low"] == min(prices_df["low"]), "date"].iloc[-1],
        prices_df.loc[prices_df["low"] == min(prices_df["low"]), "low"].iloc[-1]
    )
    offset_3y = (oldest_lowest_date + pd.DateOffset(days=3*365)).date()

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

    doubled_return_date = doubled_return_df.loc[0, "date"]

    doubled_return_days = (doubled_return_date - oldest_lowest_date).days
    doubled_return_months = round(doubled_return_days / 30, 2)
    doubled_return_years = round(doubled_return_days / 365, 2)

    