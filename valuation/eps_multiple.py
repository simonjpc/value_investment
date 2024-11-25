from valuation.constants import (
    PE_RATIO_CAP,
    ANNUAL_RETURN_RATE_CAP,
    QUARTERLY_RETURN_RATE_CAP,
    ANNUAL_GROWTH_RATE_CAP,
    QUARTERLY_GROWTH_RATE_CAP,
    EPS_KEY,
    TOTAL_ASSETS_KEY,
    GOODWILL_KEY,
    INTANGIBLE_ASSETS_KEY,
    TOTAL_LIAB_KEY,
    GOODWILL_AND_INTANGILE_ASSETS_KEY,
    SHARES_OUTS_KEY,
    NET_RECEIVABLES_KEY,
    INVENTORY_KEY,
    PPE_KEY,
    CURRENT_ASSETS_FACTORS,
    RECEIVABLES_FACTOR_KEY,
    INVENTORY_FACTOR_KEY,
    PPE_FACTOR_KEY,
    REPORTING_DATE_PRICE_COL,
    EXPECTED_OBLIGATIONS,
    STOCKHOLDERS_EQUITY_KEY,
    FILLING_DATE_KEY,
    DATE_KEY,
)

from typing import Dict, Any, Tuple, List
import numpy as np
import pandas as pd
from valuation.extraction import get_prices_in_range
from valuation.utils import compute_avg_value, get_key_from_iterator


class EPSMultiple:

    def __init__(self):
        pass


def compute_fp(
    eps: float,
    growth_value: float,
    future_pe: float,
    years: int = None,
    quarters: int = None,
) -> float:
    if eps is None:
        raise TypeError("all attributes must be numeric")
    if not all(isinstance(var, (int, float)) for var in [eps, growth_value, future_pe]):
        raise TypeError("all attributes must be numeric")
    if years is not None and years < 0:  # check for integer years var
        raise AttributeError("`years` attribute must be a positive integer")
    if quarters is not None and quarters < 0:  # check for integer years var
        raise AttributeError("`quarters` attribute must be a positive integer")
    if future_pe < 0:
        raise AttributeError("`future_pe` attribute must be positive")
    capped_growth_value = (
        min(ANNUAL_GROWTH_RATE_CAP, growth_value)
        if years is not None
        else min(QUARTERLY_GROWTH_RATE_CAP, growth_value)
    )
    capped_future_pe = min(PE_RATIO_CAP, future_pe)
    if years is not None:
        return eps * ((1 + capped_growth_value) ** years) * capped_future_pe
    return eps * ((1 + capped_growth_value) ** quarters) * capped_future_pe


def compute_pfv(
    fp: float, return_value: float, years: int, quarters: int = None
) -> float:
    if years is None and quarters is None:
        raise ValueError("either `years` or `quarters` must be different to None")
    if years is not None and quarters is not None:
        raise ValueError(
            "only one argument `years` or `quarters` can be different to None"
        )
    if not all([isinstance(var, (int, float)) for var in [fp, return_value]]):
        raise TypeError("all attributes must numerical")
    if return_value < 0:
        raise ValueError(
            "though numerically possible for negative values, the `return_value` attribute must be greater than or equal to zero"
        )
    if years is not None and years <= 0:
        raise ValueError("`years` attribute must be greater than zero")
    if quarters is not None and quarters <= 0:
        raise ValueError("`quarters` attribute must be greater than zero")
    capped_return_value = (
        min(ANNUAL_RETURN_RATE_CAP, return_value)
        if years is not None
        else min(QUARTERLY_RETURN_RATE_CAP, return_value)
    )
    if years is not None:
        return fp / ((1 + capped_return_value) ** years)
    return fp / ((1 + capped_return_value) ** quarters)


def compute_pex_value_handler(
    eps: float,
    growth_value: float,
    return_value: float,
    future_pe: float,
    years: int,
    quarters: int = None,
) -> float:
    if not all(
        [
            isinstance(var, (int, float))
            for var in [eps, growth_value, return_value, future_pe]
        ]
    ):
        raise TypeError("all attributes must be numerical")
    if not all([var >= 0 for var in [growth_value, return_value]]):
        raise ValueError(
            "thought numerically possible for negative values, `growth_value` and `return_value` must be greater or equal to zero"
        )
    if future_pe <= 0:
        raise ValueError(
            "thought numerically possible for other values, `future_pe` must be positive"
        )
    if years is None and quarters is None:
        raise ValueError("either `years` or `quarters` must be different to None")
    if years is not None and quarters is not None:
        raise ValueError(
            "only one argument `years` or `quarters` can be different to None"
        )
    if years is not None and years <= 0:
        raise ValueError("`years` attribute must be greater than zero")
    if quarters is not None and quarters <= 0:
        raise ValueError("`quarters` attribute must be greater than zero")

    fp = compute_fp(eps, growth_value, future_pe, years, quarters)
    pfv = compute_pfv(fp, return_value, years, quarters)
    return pfv


def compute_pex_value(
    deco: Dict[str, Any],
    growth_value: float,
    return_value: float,
    future_pe: float,
    years: int,
    quarters: int = None,
) -> float:
    if not isinstance(deco, (dict, pd.Series)):
        raise ValueError("`deco` attribute must be a dictionary")
    if EPS_KEY not in deco:
        raise ValueError("`eps` key is expected in `deco`")
    if not all(
        [
            isinstance(var, (int, float))
            for var in [growth_value, return_value, future_pe]
        ]
    ):
        print(growth_value, return_value, future_pe)
        raise ValueError(
            "attributes `growth_value`, `return_value` and `future_pe` must all be numeric"
        )
    eps = deco.get(EPS_KEY, 0)
    pfv = compute_pex_value_handler(
        eps, growth_value, return_value, future_pe, years, quarters
    )
    return pfv


def compute_tangible_book_value(deco: Dict[str, Any]) -> float:
    if not isinstance(deco, (dict, pd.Series)):
        raise AttributeError("`deco` attribute must be a dictionary")
    intangible_assets = deco.get(
        GOODWILL_AND_INTANGILE_ASSETS_KEY,
        deco.get(GOODWILL_KEY, 0) + deco.get(INTANGIBLE_ASSETS_KEY, 0),
    )
    total_assets = deco.get(TOTAL_ASSETS_KEY, 0)
    total_liab = deco.get(TOTAL_LIAB_KEY, 0)
    tangible_assets = total_assets - intangible_assets
    tangible_book_value = tangible_assets - total_liab
    return tangible_book_value


def compute_tangible_book_value_ps(deco: Dict[str, Any]) -> float:
    tangible_book_value = compute_tangible_book_value(deco)
    nb_outs_shares = deco.get(SHARES_OUTS_KEY, np.Inf)
    nb_outs_shares = max(nb_outs_shares, 1e-6)
    return tangible_book_value / nb_outs_shares


def compute_discounted_tangible_book_value(deco: Dict[str, Any]) -> float:
    if not isinstance(deco, dict):
        raise AttributeError("`deco` attribute must be a dictionary")
    intangible_assets = deco.get(
        GOODWILL_AND_INTANGILE_ASSETS_KEY,
        deco.get(GOODWILL_KEY, 0) + deco.get(INTANGIBLE_ASSETS_KEY, 0),
    )
    total_assets = deco.get(TOTAL_ASSETS_KEY, 0)
    total_liab = deco.get(TOTAL_LIAB_KEY, 0)

    discount = sum(
        (1 - CURRENT_ASSETS_FACTORS[factor_key]) * deco.get(current_asset_key, 0)
        for factor_key, current_asset_key in [
            (RECEIVABLES_FACTOR_KEY, NET_RECEIVABLES_KEY),
            (INVENTORY_FACTOR_KEY, INVENTORY_KEY),
            (PPE_FACTOR_KEY, PPE_KEY),
        ]
    )

    discounted_tangible_assets = total_assets - intangible_assets - discount
    discounted_tangible_book_value = discounted_tangible_assets - total_liab
    return discounted_tangible_book_value


def compute_discounted_tangible_book_value_ps(deco: Dict[str, Any]) -> float:
    tangible_book_value = compute_discounted_tangible_book_value(deco)
    nb_outs_shares = deco.get(SHARES_OUTS_KEY, np.Inf)
    return tangible_book_value / nb_outs_shares


def compute_pe_ratio(deco: Dict[str, Any]) -> float:
    if not isinstance(deco, (dict, pd.Series)):
        raise AttributeError("`deco` attribute must be a dictionary")
    pps = deco.get(REPORTING_DATE_PRICE_COL, 0)
    eps = deco.get(EPS_KEY, 0)
    if eps == 0:
        eps = 1e-6
    return pps / eps


def compute_de_ratio1(deco: Dict[str, Any]) -> float:
    return deco.get("totalLiabilities", 1e6) / deco.get("totalStockholdersEquity", 1e-6)


def compute_de_ratio2(deco) -> float:
    return deco.get("totalCurrentLiabilities", 1e6) / deco.get(
        "totalStockholdersEquity", 1e-6
    )


def compute_de_ratio3(deco) -> float:
    return deco.get("totalDebt", 1e6) / deco.get("totalStockholdersEquity", 1e-6)


def compute_de_ratio(deco: Dict[str, Any], obligation_type: str) -> float:
    if not isinstance(deco, (dict, pd.Series)):
        raise AttributeError("`deco` attribute must be a dictionary")
    if not isinstance(obligation_type, str):
        raise AttributeError("`obligation_type` attribute must be a string")
    if obligation_type not in EXPECTED_OBLIGATIONS:
        raise AttributeError(
            f"`obligation_type` attribute must be one of the following: {EXPECTED_OBLIGATIONS}"
        )
    return deco.get(obligation_type, 1e6) / max(
        1e-6, deco.get(STOCKHOLDERS_EQUITY_KEY, 1e-6)
    )


def get_date_range(
    date: pd.Timestamp, window_start_offset: int = 30, window_end_offset: int = 46
) -> Tuple[str, str]:
    if not isinstance(date, pd.Timestamp):
        raise AttributeError("`date` attribute must be a pandas timestamp")
    if not all(
        [
            isinstance(var, (int, float))
            for var in (window_start_offset, window_end_offset)
        ]
    ):
        raise AttributeError(
            "both `window_start_offset` & `window_end_offset` must be positive integers"
        )
    if not all([var >= 0 for var in (window_start_offset, window_end_offset)]):
        raise AttributeError(
            "both `window_start_offset` & `window_end_offset` must be positive integers"
        )
    if window_end_offset < window_start_offset:
        raise ValueError(
            "`window_end_offset` must be greater than or equal to `window_start_offset`"
        )
    window_start = (date + pd.DateOffset(days=window_start_offset)).date()
    window_end = (date + pd.DateOffset(days=window_end_offset)).date()
    return str(window_start), str(window_end)


def get_reporting_window(deco):
    if not isinstance(deco, (dict, pd.Series)):
        raise AttributeError("`deco attribute must be a dictionary`")
    filling_date = deco.get(FILLING_DATE_KEY, None)

    if filling_date is None:
        date = deco.get(DATE_KEY, None)
        if date is not None:
            date = pd.Timestamp(date)
            reporting_start, reporting_end = get_date_range(date)
        else:
            return None, None, filling_date is not None
    else:
        reporting_start = filling_date
        reporting_datetime = pd.to_datetime(filling_date) + pd.DateOffset(days=3)
        reporting_end = str(reporting_datetime.date())
    return reporting_start, reporting_end, filling_date is not None


# def compute_avg_price(data_prices: Dict[str, Any]) -> float:
#    historical_prices = data_prices.get("historical", {})


def get_price_history(deco: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not isinstance(deco, dict):
        raise AttributeError("`deco` attribute must be a dictionary")
    return deco.get("historical", [])


# def get_reporting_prices(iterator: List[Dict[str, Any]], price_key: str = "low") -> List[float]:
#    prices = get_key_from_iterator(iterator, price_key)
#    return prices


def compute_price_at_reporting_date(
    prices: List[str],
    filling_date_flag: bool,
    key: str = "low",
) -> float:
    if not isinstance(prices, list):
        raise AttributeError("`prices` attribute must be a list")
    if not isinstance(filling_date_flag, (bool, np.bool_)):
        raise AttributeError("`filling_date_flag` attribute must be boolean")
    if not isinstance(key, str):
        raise AttributeError("`key` attribute must be a string")
    if filling_date_flag is False:
        range_price_lows = get_key_from_iterator(prices, key)
    else:
        range_price_lows = get_key_from_iterator(prices[:2], key)
    if range_price_lows:
        avg_price_at_report = compute_avg_value(range_price_lows)
    else:
        avg_price_at_report = np.Inf
    return avg_price_at_report


def growth_function(current: float, previous: float, nb_periods: int) -> float:
    if not all(
        [isinstance(var, (int, float)) for var in (current, previous, nb_periods)]
    ):
        raise TypeError("all attributes must be numerical")
    if not all([var > 0 for var in (current, previous, nb_periods)]):
        raise ValueError("all attributes must be positive")
    growth_value = round((current / previous) ** (1 / nb_periods) - 1, 4)
    return growth_value


def compute_growth(current: float, previous: float, nb_periods: int) -> float:
    if not all(
        [isinstance(var, (int, float)) for var in (current, previous, nb_periods)]
    ):
        raise TypeError("all attributes must be numerical")
    if current == 0:
        current = 1e-6
    if previous == 0:
        previous = 1e-6
    if current > 0 and previous < 0:
        gap = 2 * abs(previous)
        # gap = current - previous
        current += gap
        previous += gap
    elif current < 0 and previous > 0:
        gap = previous - current
        current += gap
        previous += gap
    elif current < 0 and previous < 0:
        previous, current = current, previous
        previous = abs(previous)
        current = abs(current)
    growth = growth_function(current, previous, nb_periods)
    return growth


# DEPRICATED
def compute_price_at_reporting_date_OLD(deco, ticker):
    print(deco)
    filling_date = deco.get(FILLING_DATE_KEY, None)

    if filling_date is None:
        reporting_start, reporting_end = get_date_range(filling_date)
    else:
        reporting_start = filling_date
        reporting_datetime = pd.to_datetime(filling_date) + pd.DateOffset(days=3)
        reporting_end = str(reporting_datetime.date())

    try:
        data_prices = get_prices_in_range(ticker, reporting_start, reporting_end)

        historical_prices = data_prices.get("historical", [])
        if filling_date is None:
            range_price_lows = get_key_from_iterator(historical_prices, "low")
        else:
            range_price_lows = get_key_from_iterator(historical_prices[:2], "low")

        if range_price_lows:
            avg_price_at_report = compute_avg_value(range_price_lows)
        else:
            avg_price_at_report = np.Inf
    except Exception as e:
        print(f"Error fetching price data: {e}")
        avg_price_at_report = np.Inf

    return avg_price_at_report
