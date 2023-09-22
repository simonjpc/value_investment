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

@pytest.fixture
def income_stmt_response_mock():
    return [
        {
            "date": "2022-06-30",
            "symbol": "SSY",
            "reportedCurrency": "USD",
            "cik": "0000096793",
            "fillingDate": "2022-09-28",
            "acceptedDate": "2022-09-28 14:55:21",
            "calendarYear": "2022",
            "period": "FY",
            "revenue": 41344000,
            "costOfRevenue": 21238000,
            "grossProfit": 20106000,
            "grossProfitRatio": 0.4863099845,
            "researchAndDevelopmentExpenses": 0,
            "generalAndAdministrativeExpenses": 19558000,
            "sellingAndMarketingExpenses": 0,
            "sellingGeneralAndAdministrativeExpenses": 19558000,
            "otherExpenses": 5888000,
            "operatingExpenses": 25446000,
            "costAndExpenses": 46684000,
            "interestIncome": 0,
            "interestExpense": -15000,
            "depreciationAndAmortization": -1477000,
            "ebitda": -6817000,
            "ebitdaratio": -0.1648848684,
            "operatingIncome": -5340000,
            "operatingIncomeRatio": -0.1291602167,
            "totalOtherIncomeExpensesNet": 3725000,
            "incomeBeforeTax": -1615000,
            "incomeBeforeTaxRatio": -0.0390625,
            "incomeTaxExpense": 107000,
            "netIncome": -1722000,
            "netIncomeRatio": -0.0416505418,
            "eps": -0.25,
            "epsdiluted": -0.25,
            "weightedAverageShsOut": 6945000,
            "weightedAverageShsOutDil": 6945000,
            "link": "https://www.sec.gov/Archives/edgar/data/96793/000156459022032555/0001564590-22-032555-index.htm",
            "finalLink": "https://www.sec.gov/Archives/edgar/data/96793/000156459022032555/ssy-10k_20220630.htm",
        },
        {
            "date": "2021-06-30",
            "symbol": "SSY",
            "reportedCurrency": "USD",
            "cik": "0000096793",
            "fillingDate": "2021-09-27",
            "acceptedDate": "2021-09-27 16:27:32",
            "calendarYear": "2021",
            "period": "FY",
            "revenue": 40685000,
            "costOfRevenue": 19074000,
            "grossProfit": 21611000,
            "grossProfitRatio": 0.531178567,
            "researchAndDevelopmentExpenses": 0,
            "generalAndAdministrativeExpenses": 14350000,
            "sellingAndMarketingExpenses": 0,
            "sellingGeneralAndAdministrativeExpenses": 14350000,
            "otherExpenses": 5390000,
            "operatingExpenses": 19740000,
            "costAndExpenses": 38814000,
            "interestIncome": 0,
            "interestExpense": 0,
            "depreciationAndAmortization": 1084000,
            "ebitda": 2955000,
            "ebitdaratio": 0.0726311909,
            "operatingIncome": 1871000,
            "operatingIncomeRatio": 0.0459874647,
            "totalOtherIncomeExpensesNet": 5129000,
            "incomeBeforeTax": 7000000,
            "incomeBeforeTaxRatio": 0.1720535824,
            "incomeTaxExpense": 63000,
            "netIncome": 6890000,
            "netIncomeRatio": 0.1693498832,
            "eps": 1,
            "epsdiluted": 0.99,
            "weightedAverageShsOut": 6907000,
            "weightedAverageShsOutDil": 6989000,
            "link": "https://www.sec.gov/Archives/edgar/data/96793/000156459021049055/0001564590-21-049055-index.htm",
            "finalLink": "https://www.sec.gov/Archives/edgar/data/96793/000156459021049055/ssy-10k_20210630.htm",
        },
        {
            "date": "2020-06-30",
            "symbol": "SSY",
            "reportedCurrency": "USD",
            "cik": "0000096793",
            "fillingDate": "2020-09-29",
            "acceptedDate": "2020-09-28 17:45:55",
            "calendarYear": "2020",
            "period": "FY",
            "revenue": 47813000,
            "costOfRevenue": 23162000,
            "grossProfit": 24651000,
            "grossProfitRatio": 0.515571079,
            "researchAndDevelopmentExpenses": 0,
            "generalAndAdministrativeExpenses": 20164000,
            "sellingAndMarketingExpenses": 0,
            "sellingGeneralAndAdministrativeExpenses": 20164000,
            "otherExpenses": 4816000,
            "operatingExpenses": 24980000,
            "costAndExpenses": 48142000,
            "interestIncome": 0,
            "interestExpense": 29000,
            "depreciationAndAmortization": 1450000,
            "ebitda": 1175000,
            "ebitdaratio": 0.0245749064,
            "operatingIncome": -275000,
            "operatingIncomeRatio": -0.0057515738,
            "totalOtherIncomeExpensesNet": -15000,
            "incomeBeforeTax": -290000,
            "incomeBeforeTaxRatio": -0.006065296,
            "incomeTaxExpense": 296000,
            "netIncome": -586000,
            "netIncomeRatio": -0.012256081,
            "eps": -0.0842,
            "epsdiluted": -0.0842,
            "weightedAverageShsOut": 6957000,
            "weightedAverageShsOutDil": 6957000,
            "link": "https://www.sec.gov/Archives/edgar/data/96793/000156459020044839/0001564590-20-044839-index.htm",
            "finalLink": "https://www.sec.gov/Archives/edgar/data/96793/000156459020044839/ssy-10k_20200630.htm",
        }
    ]
