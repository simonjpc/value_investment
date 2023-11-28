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
