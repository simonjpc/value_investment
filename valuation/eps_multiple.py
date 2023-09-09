from valuation.constants import (
    GROWTH_RATE_CAP,
    PE_RATIO_CAP,
    RETURN_RATE_CAP,
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
)

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from valuation.extractor import get_prices_in_range
from valuation.utils import compute_avg_value, get_key_from_iterator

class EPSMultiple():

    def __init__(self):
        pass


def compute_fp(
    eps: float,
    growth_value: float,
    years: int,
    future_pe: float,
) -> float:
    capped_growth_value = min(GROWTH_RATE_CAP, growth_value)
    capped_future_pe = min(PE_RATIO_CAP, future_pe)
    return eps * ((1 + capped_growth_value) ** years) * capped_future_pe

def compute_pfv(fp: float, return_value: float, years: int) -> float:
    capped_return_value = min(RETURN_RATE_CAP, return_value)
    return fp / ((1 + capped_return_value) ** years)

def compute_pex_value_handler(
    eps: float,
    growth_value: float,
    return_value: float,
    future_pe: float,
    years: int,
) -> float:
    fp = compute_fp(eps, growth_value, years, future_pe)
    pfv = compute_pfv(fp, return_value, years)
    return pfv

def compute_pex_value(
    deco: Dict[str, Any],
    growth_value: float,
    return_value: float,
    future_pe: float,
    years: int,
)  -> float:
    eps = deco.get(EPS_KEY, 0)
    pfv = compute_pex_value_handler(
        eps, growth_value, return_value, future_pe, years
    )
    return pfv

def compute_tangible_book_value(deco: Dict[str, Any]) -> float:
    intangible_assets = deco.get(
        GOODWILL_AND_INTANGILE_ASSETS_KEY,
        deco.get(GOODWILL_KEY, 0) + deco.get(INTANGIBLE_ASSETS_KEY, 0)
    )
    total_assets = deco.get(TOTAL_ASSETS_KEY, 0)
    total_liab = deco.get(TOTAL_LIAB_KEY, 0)
    tangible_assets = total_assets - intangible_assets
    tangible_book_value = tangible_assets - total_liab
    return tangible_book_value

def compute_tangible_book_value_ps(deco: Dict[str, Any]) -> float:
    tangible_book_value = compute_tangible_book_value(deco)
    nb_outs_shares = deco.get(SHARES_OUTS_KEY, np.Inf)
    return tangible_book_value / nb_outs_shares


def compute_discounted_tangible_book_value(deco: Dict[str, Any]) -> float:
    intangible_assets = deco.get(
        GOODWILL_AND_INTANGILE_ASSETS_KEY,
        deco.get(GOODWILL_KEY, 0) + deco.get(INTANGIBLE_ASSETS_KEY, 0)
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

def compute_discounted_tangible_book_value_ps(
    deco: Dict[str, Any],
    factors_deco: Dict[str, Any],
) -> float:
    tangible_book_value = compute_discounted_tangible_book_value(deco, factors_deco)
    nb_outs_shares = deco.get(SHARES_OUTS_KEY, np.Inf)
    return tangible_book_value / nb_outs_shares

def compute_pe_ratio(deco: Dict[str, Any]) -> float:
    eps = deco.get(EPS_KEY, 0)
    pps = deco.get(REPORTING_DATE_PRICE_COL, 1e-5)
    return eps/pps

def compute_de_ratio1(deco: Dict[str, Any]) -> float:
    return deco.get("totalLiabilities", 1e6) / deco.get("totalStockholdersEquity", 1e-6)

def compute_de_ratio2(deco) -> float:
    return deco.get("totalCurrentLiabilities", 1e6) / deco.get("totalStockholdersEquity", 1e-6)

def compute_de_ratio3(deco) -> float:
    return deco.get("totalDebt", 1e6) / deco.get("totalStockholdersEquity", 1e-6)

def compute_de_ratio(deco: Dict[str, Any], obligation_type: str) -> float:
    if obligation_type not in EXPECTED_OBLIGATIONS:
        raise AttributeError(
            f"invalid `obligation_type` attribute. The accepted values are {EXPECTED_OBLIGATIONS}"
        )
    return deco.get(obligation_type, 1e6) / deco.get(STOCKHOLDERS_EQUITY_KEY, 1e-6)

def get_date_window(
    date: pd.Timestamp, window_start_offset: int = 30, window_end_offset: int = 46
) -> Tuple[str, str]:
    window_start = (date + pd.DateOffset(days=window_start_offset)).date()
    window_end = (date + pd.DateOffset(days=window_end_offset)).date()
    return str(window_start), str(window_end)

def compute_price_at_reporting_date(deco, ticker):
    filling_date = deco.get(FILLING_DATE_KEY, None)
    
    if filling_date is None:
        reporting_start, reporting_end = get_date_window(filling_date)
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
