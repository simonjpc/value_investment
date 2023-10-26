import pandas as pd
from typing import List, Tuple, Dict, Any

# get unique tickers from financial_stmts table
def get_unique_tickers_from_db() -> List[str]:
    pass
# compute starting and ending day of week (from monday to friday)
def week_starting_and_ending() -> Tuple[str, str]:
    # think about how the define the input
    pass

# for each ticker get daily values per week
def get_prices_in_range():
    # this function is already implemented 
    pass

# transform data from week to have only 6 values per week
def aggregate_weekly_prices(price_info: Dict[str, Any]) -> Tuple[float]:
    pass

# dump data into database
def dump_prices_info(all_df: pd.DataFrame) -> None:
    pass
