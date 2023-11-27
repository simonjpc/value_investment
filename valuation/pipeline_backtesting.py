import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from datetime import datetime
from valuation.liquidation import compute_ncavps, compute_liqvps
from valuation.constants import CURRENT_ASSETS_FACTORS
from valuation.data_injection import Injector

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

for ticker in filtered_tickers:
    query = f"""
    WITH min_filling_date AS (
        SELECT MIN("fillingDate_bs") as filling_date_oldest
        FROM financial_stmts
        WHERE symbol_bs = '{test_symbol}'
    )
    SELECT "fillingDate_bs", period_bs
    FROM financial_stmts
    WHERE "fillingDate_bs" = (SELECT filling_date_oldest FROM min_filling_date)
        AND symbol_bs = '{test_symbol}';
    """

    with engine.connec() as connection:
        df = pd.read_sql(query, connection)

    