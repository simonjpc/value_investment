import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from typing import List, Tuple, Dict, Any
from valuation.constants import OLDEST_FILLING_DATE_PER_SYMBOL_QUERY
from valuation.data_injection import Injector
from valuation.extraction import get_prices_in_range
from valuation.utils import compute_avg_value, dict_to_df

# get oldest record per symbol.
# This should go somewhere else where reads from queries are made
def all_symbols_oldest_and_newest_dates(
    query: str, connection: sqlalchemy.engine,
) -> pd.DataFrame:
    df = pd.read_sql(query, con=connection)
    return df

# probably part of tools.py
def compute_offset_date(
    date: Any[str, pd.Timestamp], offset: int = 730,
) -> np.Timestamp:
    if not isinstance(date, (str, pd.Timestamp)):
        raise TypeError("`date` attribute must be a string of a timestamp")
    if isinstance(date, str):
        date = pd.to_datetime(date)
    offset_date = (date + pd.DateOffset(days=offset)).date()
    return offset_date

# probably part of tools.py
def weekday_from_date(date: Any[str, pd.Timestamp]) -> str:
    """
    0 = Monday
    6 = Sunday
    """
    if not isinstance(date, (str, pd.Timestamp)):
        raise TypeError("`date` attribute must be a string of a timestamp")
    if isinstance(date, str):
        date = pd.to_datetime(date)
    return date.weekday()

# Already implemented
# def get_prices_in_range(ticker: str, window_start: str, window_end: str) -> Dict[str, Any]:

# to improve
def get_pertinent_keys(prices_structure: Dict[str, Any]) -> List[str]:
    all_price_info = []
    historical_prices = prices_structure.get("historical", None)
    if historical_prices is None:
        return
    for element in prices_structure:
        low_price, high_price, open_price, close_price, volume = (
            element.get("low", None),
            element.get("high", None),
            element.get("open", None),
            element.get("close", None),
            element.get("volume", None),
        )
        all_price_info.append(
            (
                low_price, high_price, open_price, close_price, volume
            )
        )
    return all_price_info

# compute price average. Already implemented
# compute_avg_value()

# convert data into df. Already implemented
df =  dict_to_df()

# dump into database
injector = Injector()
injector.df_dump(df, engine) # <- better understand the engine and how connections are created
