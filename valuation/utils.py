import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
from valuation.constants import COLS_TO_PLOT_EPSX, COLS_TO_PLOT_NCAV, COLS_WITH_SAME_SCALE, SUBPLOT_NAMES

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
