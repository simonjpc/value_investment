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

tickers_list = tickers_df["ticker"].tolist()

filtered_tickers = [
    ticker for ticker in tickers_list if (
        "." not in ticker and
        "-" not in ticker and
        "+" not in ticker and
        "^" not in ticker and
        "~" not in ticker
    )
]

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
    ]
)

MODIF_CONSTANT = 0.20 # 20% arbitrary return reduction

# iterate on all symbols
for idx, test_symbol in enumerate(filtered_tickers):
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

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    # get stmts from oldest until oldest + 10 years from the same quarter
    if len(df) == 0:
        continue
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

    output_df.loc[idx, "ticker"] = test_symbol
    output_df.loc[idx, "ref_report_date"] = df.loc[0, "fillingDate_bs"]
    output_df.loc[idx, "report_date"] = offset_date_financials.loc[0, "fillingDate"]
    output_df.loc[idx, "ref_report_date_quarter"] = df.loc[0, "period_bs"]
    output_df.loc[idx, "report_date_quarter"] = offset_date_financials.loc[0, "period"]
    output_df.loc[idx, "outs_shares1"] = same_period_hist_df.reset_index().loc[0, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares2"] = same_period_hist_df.reset_index().loc[1, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares3"] = same_period_hist_df.reset_index().loc[2, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares4"] = same_period_hist_df.reset_index().loc[3, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares5"] = same_period_hist_df.reset_index().loc[4, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares6"] = same_period_hist_df.reset_index().loc[5, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares7"] = same_period_hist_df.reset_index().loc[6, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares8"] = same_period_hist_df.reset_index().loc[7, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares9"] = same_period_hist_df.reset_index().loc[8, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares10"] = same_period_hist_df.reset_index().loc[9, "weightedAverageShsOutDil"]
    output_df.loc[idx, "outs_shares_slope_pct_10y"] = round(slope_percentage * 100, 2)
    output_df.loc[idx, "outs_shares_slope_pct_5y"] = round(slope_percentage_5y * 100, 2)
    output_df.loc[idx, "min_price_date"] = oldest_lowest_date
    output_df.loc[idx, "min_price"] = oldest_lowest_price
    output_df.loc[idx, "max_price_date"] = highest_date
    output_df.loc[idx, "max_price"] = highest_price
    output_df.loc[idx, "ncavps"] = ncavps
    output_df.loc[idx, "liqvps"] = liqvps
    output_df.loc[idx, "ncav_mos"] = round(oldest_lowest_price / ncavps, 2)
    output_df.loc[idx, "liqv_mos"] = round(oldest_lowest_price / liqvps, 2)
    output_df.loc[idx, "highest_return_delay"] = round(return_time_days / 365, 2)
    output_df.loc[idx, "doubling_price"] = oldest_lowest_price * 2
    output_df.loc[idx, "doubling_date"] = doubled_return_df.loc[0, "date"] if len(doubled_return_df) > 0 else None
    output_df.loc[idx, "doubling_return_delay"] = round(doubled_return_days / 365, 2) if doubled_return_days is not None else None
    output_df.loc[idx, "highest_return"] = round(return_percentage * 100, 2)

    output_df.loc[idx, "min_price_modif"] = oldest_lowest_price * (1 + MODIF_CONSTANT)
    output_df.loc[idx, "max_price_modif"] = highest_price * (1 - MODIF_CONSTANT)
    output_df.loc[idx, "ncav_mos_modif"] = round(output_df.loc[idx, "min_price_modif"] / ncavps, 2)
    output_df.loc[idx, "liqv_mos_modif"] = round(output_df.loc[idx, "min_price_modif"] / liqvps, 2)
    output_df.loc[idx, "doubling_price_modif"] = output_df.loc[idx, "min_price_modif"] * 2
    output_df.loc[idx, "highest_return_modif"] = round((output_df.loc[idx, "max_price_modif"] - output_df.loc[idx, "min_price_modif"]) * 100 / output_df.loc[idx, "min_price_modif"], 2)

    break

#output_df = output_df.reset_index(drop=True)
print("output_df")
print(output_df.head())
