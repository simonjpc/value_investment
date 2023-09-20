import pytest
import pandas as pd

@pytest.fixture
def fp_variables():
    """
    Input for function compute_fp
    """
    return {
        "eps": 1.5,
        "growth_value": 0.20,
        "years": 7,
        "future_pe": 9,
        "fp": 48.373,
    }

@pytest.fixture
def pfv_variables():
    """Input for function compute_pfv
    """
    return {
        "fp": 3.21, 
        "return_value": 0.15,
        "pfv": 1.387,
        "years": 6,
    }

@pytest.fixture
def pex_handler_variables():
    """
    Input for function compute_pex_value_handler
    """
    return {
        "eps": 1.5,
        "growth_value": 0.20,
        "return_value": 0.15,
        "future_pe": 9,
        "years": 6,
        "pfv": 17.427,
    }

@pytest.fixture
def pex_variables():
    """
    Input for function compute_pex_value
    """
    return {
        "deco": {"eps": -1.5},
        "growth_value": 0.20,
        "return_value": 0.15,
        "future_pe": 9,
        "years": 6,
        "pfv": -17.427,
    }

@pytest.fixture
def tangible_bv_variables():
    """
    Input for function compute_tangible_book_value
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "tangible_bv": 3432000,
    }

@pytest.fixture
def compute_tangible_bvps():
    """
    Input for function compute_tangible_book_value_ps
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "weightedAverageShsOutDil": 3150000,
        "tangible_bv": 3432000,
        "tangible_bvps": 1.089,
    }

@pytest.fixture
def dct_tangible_bv_variables():
    """
    Input for function compute_discounted_tangible_book_value
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "netReceivables": 400000,
        "inventory": 200000,
        "propertyPlantEquipmentNet": 300000,
        "dct_tangible_bv": 3173000,
    }
        

@pytest.fixture
def compute_dct_tangible_bvps():
    """
    Input for function compute_discounted_tangible_book_value_ps
    """
    return {
        "goodwill": 1340700,
        "intangibleAssets": 987300,
        "goodwillAndIntangibleAssets": 2328000,
        "totalAssets": 7650000,
        "totalLiabilities": 1890000,
        "netReceivables": 400000,
        "inventory": 200000,
        "propertyPlantEquipmentNet": 300000,
        "weightedAverageShsOutDil": 3150000,
        "dct_tangible_bv": -1,
        "dct_tangible_bvps": 1.007,
    }

@pytest.fixture
def pe_ratio_variables():
    return {
        "reporting_date_price": 6.28,
        "eps": 1.77,
        "pe_ratio": 3.548,
    }

@pytest.fixture
def de_ratio_variables():
    return {
        "totalLiabilities": 3702000,
        "totalCurrentLiabilities": 979000,
        "totalDebt": 614000,
        "totalStockholdersEquity": 7710000,
    }

@pytest.fixture
def date_range_variables():
    return {
        "date": pd.Timestamp("2022-09-19"),
        "window_start_offset": 30,
        "window_end_offset": 46,
    }

@pytest.fixture
def reporting_date_variables():
    return {
        "fillingDate": "2022-09-19",
        "date": "2022-08-10",
        "window": ("2022-09-19", "2022-09-22"),
    }

@pytest.fixture
def price_hist_variables():
    return {
        "symbol": "SYMB",
        "historical": [
            {
                "date": "2013-02-15",
                "open": 3.81,
                "high": 3.9434,
                "low": 3.81,
                "close": 3.92,
                "adjClose": 3.92,
                "volume": 17005,
                "unadjustedVolume": 17100,
                "change": 0.11,
                "changePercent": 2.89,
                "vwap": 3.86,
                "label": "February 15, 13",
                "changeOverTime": 0.0289,
            },
            {
                "date": "2013-02-14",
                "open": 3.94,
                "high": 3.94,
                "low": 3.8,
                "close": 3.81,
                "adjClose": 3.81,
                "volume": 14805,
                "unadjustedVolume": 14900,
                "change": -0.13,
                "changePercent": -3.3,
                "vwap": 3.81,
                "label": "February 14, 13",
                "changeOverTime": -0.033,
            },
            {
                "date": "2013-02-13",
                "open": 3.85,
                "high": 3.98,
                "low": 3.81,
                "close": 3.87,
                "adjClose": 3.87,
                "volume": 13884,
                "unadjustedVolume": 13900,
                "change": 0.02,
                "changePercent": 0.51948,
                "vwap": 3.89,
                "label": "February 13, 13",
                "changeOverTime": 0.0051948,
            },
            {
                "date": "2013-02-12",
                "open": 3.81,
                "high": 3.94,
                "low": 3.81,
                "close": 3.87,
                "adjClose": 3.87,
                "volume": 7997,
                "unadjustedVolume": 8000,
                "change": 0.06,
                "changePercent": 1.57,
                "vwap": 3.9,
                "label": "February 12, 13",
                "changeOverTime": 0.0157,
            },
            {
                "date": "2013-02-11",
                "open": 3.8,
                "high": 3.86,
                "low": 3.761,
                "close": 3.86,
                "adjClose": 3.86,
                "volume": 13106,
                "unadjustedVolume": 13200,
                "change": 0.06,
                "changePercent": 1.58,
                "vwap": 3.83,
                "label": "February 11, 13",
                "changeOverTime": 0.0158,
            }
        ]
    }

@pytest.fixture
def reporting_date_price_variables():
    return {
        "prices_content": [
            {
                "date": "2013-02-15",
                "open": 3.81,
                "high": 3.9434,
                "low": 3.81,
                "close": 3.92,
                "adjClose": 3.92,
                "volume": 17005,
                "unadjustedVolume": 17100,
                "change": 0.11,
                "changePercent": 2.89,
                "vwap": 3.86,
                "label": "February 15, 13",
                "changeOverTime": 0.0289,
            },
            {
                "date": "2013-02-14",
                "open": 3.94,
                "high": 3.94,
                "low": 3.8,
                "close": 3.81,
                "adjClose": 3.81,
                "volume": 14805,
                "unadjustedVolume": 14900,
                "change": -0.13,
                "changePercent": -3.3,
                "vwap": 3.81,
                "label": "February 14, 13",
                "changeOverTime": -0.033,
            },
            {
                "date": "2013-02-13",
                "open": 3.85,
                "high": 3.98,
                "low": 3.81,
                "close": 3.87,
                "adjClose": 3.87,
                "volume": 13884,
                "unadjustedVolume": 13900,
                "change": 0.02,
                "changePercent": 0.51948,
                "vwap": 3.89,
                "label": "February 13, 13",
                "changeOverTime": 0.0051948,
            },
            {
                "date": "2013-02-12",
                "open": 3.81,
                "high": 3.94,
                "low": 3.81,
                "close": 3.87,
                "adjClose": 3.87,
                "volume": 7997,
                "unadjustedVolume": 8000,
                "change": 0.06,
                "changePercent": 1.57,
                "vwap": 3.9,
                "label": "February 12, 13",
                "changeOverTime": 0.0157,
            },
            {
                "date": "2013-02-11",
                "open": 3.8,
                "high": 3.86,
                "low": 3.761,
                "close": 3.86,
                "adjClose": 3.86,
                "volume": 13106,
                "unadjustedVolume": 13200,
                "change": 0.06,
                "changePercent": 1.58,
                "vwap": 3.83,
                "label": "February 11, 13",
                "changeOverTime": 0.0158,
            }
        ],
        "low_prices_false": 3.798,
        "high_prices_false": 3.933,
        "low_prices_true": 3.805,
        "high_prices_true": 3.942,
    }
