from datetime import datetime
from typing import Any, Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from valuation.constants import (COLS_TO_PLOT_EPSX, COLS_TO_PLOT_NCAV,
                                 COLS_WITH_SAME_SCALE, DATE_FORMAT,
                                 DELISTED_COMPANY_NAME_KEY, FUNDS_STOPWORDS,
                                 SUBPLOT_NAMES)


def get_key_from_iterator(
    iterator: List[Dict[str, Any]], key: str,
) -> List[float]:
    if not isinstance(iterator, list):
        raise TypeError("`iterator` attribute must be a list of dictionaries")
    if not isinstance(key, str):
        raise TypeError("`key` attribute must be a string")
    return [element.get(key, None) for element in iterator]


def compute_rate_of_change(prev_value: float, current_value: float) -> float:
    """
    Computes the rate of change between two values.
    
    Args:
        prev_value (float): The previous value.
        current_value (float): The current value.

    Returns:
        float: The rate of change.
    """
    if not all([isinstance(var, (int, float)) for var in (prev_value, current_value)]):
        raise TypeError("both `prev_value` and `current_value` attributes must be numerical")
    return (current_value - prev_value) / (prev_value + 1e-6)

def compute_rates_of_change(iterator: List[float]) -> List[float]:
    """
    Computes the rates of change between all elements in the iterator.

    Args:
        iterator (List[float]): A list of numerical values.

    Returns:
        List[float]: A list of rates of change.
    """
    if not isinstance(iterator, (tuple, list)):
        raise TypeError("`iterator` attribute must be a list of a tuple")
    all_growth = [None]  # Initialize with zero for the first element
    for idx in range(1, len(iterator)):
        rate_change = compute_rate_of_change(iterator[idx], iterator[idx-1])
        all_growth.append(rate_change)
    return all_growth

def invert_iterator(iterator):
    if not isinstance(iterator, list):
        raise TypeError("`iterator` attribute must be a list")
    return iterator[::-1]

def drop_nulls(iterator: List[float]) -> List[float]:
    if not isinstance(iterator, list):
        raise TypeError("`iterator` attribute must be a list")
    iterator_wo_nans = np.array(iterator)
    iterator_wo_nans = [
        element for element in iterator_wo_nans if (element is not None) and (not pd.isna(element))
    ]
    return iterator_wo_nans

def compute_stat_bound(
    iterator: List[float], q_inf: float = 0.25, q_sup: float = 0.75, distance: int = 3
) -> Tuple[float, float]:
    if not isinstance(iterator, list):
        raise TypeError("`iterator` attribute must be a list")
    if not all([isinstance(attr, (int, float)) for attr in (q_inf, q_sup, distance)]):
        raise TypeError("all `q_inf`, `q_sup` and `distance` attributes must be a numerical")
    q1 = np.quantile(iterator, q_inf)
    q3 = np.quantile(iterator, q_sup)
    iqr = q3 - q1
    lower_bound = q1 - distance*iqr
    upper_bound = q3 + distance*iqr
    return lower_bound, upper_bound

def compute_avg_value(iterator: List[float]) -> float:
    if not isinstance(iterator, (tuple, list)):
        raise TypeError("`iterator` attribute must be a list or a tuple")
    try:
        average = np.mean(iterator)
        if np.isnan(average):
            raise ValueError("all elements of `iterator` attribute must be numerical")
    except:
        raise ValueError("all elements of `iterator` attribute must be numerical")
    return np.mean(iterator)

def get_date_from_dictionary(
    dictionary: Dict[str, Any], date_key: str
) -> pd.Timestamp:
    if not isinstance(dictionary, dict):
        raise TypeError("`dictionary` attribute must be a dictionary")
    value = dictionary.get(date_key, "")
    if value:
        return pd.to_datetime(value)
    else:
        raise ValueError(f"No '{date_key}' key found in the dictionary")

# ex handling_negative_pe function
def handling_negative_vals(iterator: List[float]) -> List[float]:
    if not isinstance(iterator, (tuple, list)):
        raise TypeError("`iterator` must be a list or tuple")
    try:
        positive_historical_pe = [max(val, 0) for val in iterator]
    except:
        raise TypeError("all elements in iterator must be numerical")
    return positive_historical_pe


def dict_to_df(fa_info: List[Dict[str, Any]]) -> pd.DataFrame:
    #print(fa_info)
    if not isinstance(fa_info, list):
        raise TypeError("`fa_info` must be a list")
    return pd.DataFrame(fa_info)


def list_to_single_col_df(fa_info:List[str], col_name:str) -> pd.DataFrame:
    if not isinstance(col_name, str):
        raise TypeError("`col_name` attribute must be a string")
    if not isinstance(fa_info, list):
        raise TypeError("`fa_info` attribute must be a list")
    df = pd.DataFrame(fa_info, columns=[col_name])
    return df

def df_to_list(df: pd.DataFrame) -> List[Tuple[Any]]:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("`df` attribute must be a dataframe")
    return df.values.tolist()

def weekday_from_date(date: Union[str, pd.Timestamp]) -> str:
    """
    0 = Monday
    6 = Sunday
    """
    #if not isinstance(date, (str, pd.Timestamp)):
    #    raise TypeError("`date` attribute must be a string of a timestamp")
    if isinstance(date, str):
        date = datetime.strptime(date, DATE_FORMAT)
    return date.weekday()
    
def compute_offset_date(
    date: Union[str, pd.Timestamp], offset: int = 730,
) -> pd.Timestamp:
    if not isinstance(date, (str, pd.Timestamp)):
        raise TypeError("`date` attribute must be a string of a timestamp")
    if isinstance(date, str):
        date = pd.to_datetime(date)
    offset_date = (date + pd.DateOffset(days=offset)).date()
    return offset_date


def plot_indicators_epsx(df: pd.DataFrame) -> None:
    num_cols = df.shape[1]
    num_plots = min(num_cols, 13)  # Limit to 13 subplots or the number of columns
    _, ax = plt.subplots(1, num_plots, figsize=(26, 2.5))

    for i in range(num_plots):
        col_name = COLS_TO_PLOT_EPSX[i]
        df[col_name].plot.bar(ax=ax[i], title=SUBPLOT_NAMES[col_name])
        for cols in COLS_WITH_SAME_SCALE:
            if col_name in cols:#["totalAssets", "totalLiabilities", "de_ratio1", "de_ratio2", "de_ratio3"]:
                #min_ylim, max_ylim = df[col_name].min(), df[col_name].max()
                min_ylim = df[cols].min().min() #min([df[col].min() for col in cols])
                max_ylim = df[cols].max().max() #max([df[col].max() for col in cols])
                ax[i].set_ylim([min_ylim, max_ylim])
                break

    plt.tight_layout()
    plt.show()

def plot_indicators_ncav(df: pd.DataFrame) -> None:
    num_cols = df.shape[1]
    num_plots = min(num_cols, 11)  # Limit to 11 subplots or the number of columns
    _, ax = plt.subplots(1, num_plots, figsize=(26, 3))

    for i in range(num_plots):
        col_name = COLS_TO_PLOT_NCAV[i]
        df[col_name].plot.bar(ax=ax[i], title=SUBPLOT_NAMES[col_name])
        for cols in COLS_WITH_SAME_SCALE:
            if col_name in cols:#["totalAssets", "totalLiabilities", "de_ratio1", "de_ratio2", "de_ratio3"]:
                #min_ylim, max_ylim = df[col_name].min(), df[col_name].max()
                min_ylim = df[cols].min().min() #min([df[col].min() for col in cols])
                max_ylim = df[cols].max().max() #max([df[col].max() for col in cols])
                ax[i].set_ylim([min_ylim, max_ylim])
                break

    plt.tight_layout()
    plt.show()

def drop_df_cols(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    df = df.drop(columns=cols, axis=1)
    return df


def add_suffix_to_cols(df: pd.DataFrame, suffix: str) -> pd.DataFrame:
    df.columns = [col+suffix for col in df.columns]
    return df

def batch_tickers(tickers: List[Any], batch_size: int = 300) -> List[List[str]]:
    if not isinstance(tickers, list):
        raise TypeError("`tickers` attribute must of a list of strings")
    if not isinstance(batch_size, int):
        raise TypeError("`batch_size` attribute must of an integer")
    ticker_batches = []
    cnt = 0
    while True:
        start = cnt * batch_size
        end = (cnt + 1) * batch_size
        single_batch = tickers[start:end]
        #if not all([isinstance(tk, str) for tk in single_batch]):
        #    raise ValueError("`tickers` attribute must of a list of strings")
        ticker_batches.append(single_batch)
        if start >= len(tickers) or end >= len(tickers):
            break
        cnt += 1
    return ticker_batches

# TO TEST
def filter_out_funds(delisted_objects: Dict[str, Any]) -> Dict[str, Any]:
    filtered_objects = [
        delisted
        for delisted in delisted_objects if not any(
            [
                stopword in delisted[DELISTED_COMPANY_NAME_KEY].lower()
                for stopword in FUNDS_STOPWORDS
            ]
        )
    ]
    return filtered_objects

def usd_to_currency(
    price: float, currency: str, exchanger: Dict[str, float]
) -> float:
    if currency not in exchanger or currency is None:
        return None
    return exchanger[currency] * price

def currency_to_usd(
    price: float, currency: str, exchanger: Dict[str, float]
) -> float:
    if currency not in exchanger or currency is None:
        return None
    return price / exchanger[currency]
