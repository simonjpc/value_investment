import pytest
import pandas as pd
import numpy as np
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

@pytest.fixture
def balance_sheet_response_mock():
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
            "cashAndCashEquivalents": 6794000,
            "shortTermInvestments": 0,
            "cashAndShortTermInvestments": 6794000,
            "netReceivables": 6385000,
            "inventory": 1748000,
            "otherCurrentAssets": 1888000,
            "totalCurrentAssets": 16815000,
            "propertyPlantEquipmentNet": 9404000,
            "goodwill": 0,
            "intangibleAssets": 1201000,
            "goodwillAndIntangibleAssets": 1201000,
            "longTermInvestments": 0,
            "taxAssets": 0,
            "otherNonCurrentAssets": 523000,
            "totalNonCurrentAssets": 11128000,
            "otherAssets": 0,
            "totalAssets": 27943000,
            "accountPayables": 1347000,
            "shortTermDebt": 392000,
            "taxPayables": 2600000,
            "deferredRevenue": 519000,
            "otherCurrentLiabilities": 5433000,
            "totalCurrentLiabilities": 7691000,
            "longTermDebt": 871000,
            "deferredRevenueNonCurrent": 0,
            "deferredTaxLiabilitiesNonCurrent": 69000,
            "otherNonCurrentLiabilities": 192000,
            "totalNonCurrentLiabilities": 1132000,
            "otherLiabilities": 0,
            "capitalLeaseObligations": 1209000,
            "totalLiabilities": 8823000,
            "preferredStock": 0,
            "commonStock": 3478000,
            "retainedEarnings": 4800000,
            "accumulatedOtherComprehensiveIncomeLoss": 106000,
            "othertotalStockholdersEquity": 10736000,
            "totalStockholdersEquity": 19120000,
            "totalEquity": 19120000,
            "totalLiabilitiesAndStockholdersEquity": 27943000,
            "minorityInterest": 0,
            "totalLiabilitiesAndTotalEquity": 27943000,
            "totalInvestments": 0,
            "totalDebt": 1263000,
            "netDebt": -5531000,
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
            "cashAndCashEquivalents": 9962000,
            "shortTermInvestments": 0,
            "cashAndShortTermInvestments": 9962000,
            "netReceivables": 7775000,
            "inventory": 1890000,
            "otherCurrentAssets": 2314000,
            "totalCurrentAssets": 21941000,
            "propertyPlantEquipmentNet": 7805000,
            "goodwill": 0,
            "intangibleAssets": 1227000,
            "goodwillAndIntangibleAssets": 1227000,
            "longTermInvestments": 0,
            "taxAssets": 0,
            "otherNonCurrentAssets": 591000,
            "totalNonCurrentAssets": 9623000,
            "otherAssets": 0,
            "totalAssets": 31564000,
            "accountPayables": 1096000,
            "shortTermDebt": 3412000,
            "taxPayables": 1966000,
            "deferredRevenue": 437000,
            "otherCurrentLiabilities": 4720000,
            "totalCurrentLiabilities": 9665000,
            "longTermDebt": 927000,
            "deferredRevenueNonCurrent": 0,
            "deferredTaxLiabilitiesNonCurrent": 0,
            "otherNonCurrentLiabilities": 162000,
            "totalNonCurrentLiabilities": 1089000,
            "otherLiabilities": 0,
            "capitalLeaseObligations": 1278000,
            "totalLiabilities": 10754000,
            "preferredStock": 0,
            "commonStock": 3463000,
            "retainedEarnings": 6809000,
            "accumulatedOtherComprehensiveIncomeLoss": -162000,
            "othertotalStockholdersEquity": 10700000,
            "totalStockholdersEquity": 20810000,
            "totalEquity": 20810000,
            "totalLiabilitiesAndStockholdersEquity": 31564000,
            "minorityInterest": 0,
            "totalLiabilitiesAndTotalEquity": 31564000,
            "totalInvestments": 0,
            "totalDebt": 4339000,
            "netDebt": -5623000,
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
            "cashAndCashEquivalents": 11184000,
            "shortTermInvestments": 0,
            "cashAndShortTermInvestments": 11184000,
            "netReceivables": 4315000,
            "inventory": 1866000,
            "otherCurrentAssets": 2558000,
            "totalCurrentAssets": 19923000,
            "propertyPlantEquipmentNet": 6294000,
            "goodwill": 0,
            "intangibleAssets": 1254000,
            "goodwillAndIntangibleAssets": 1254000,
            "longTermInvestments": 0,
            "taxAssets": 0,
            "otherNonCurrentAssets": 500000,
            "totalNonCurrentAssets": 8048000,
            "otherAssets": 0,
            "totalAssets": 27971000,
            "accountPayables": 872000,
            "shortTermDebt": 1766000,
            "taxPayables": 1411000,
            "deferredRevenue": 4532000,
            "otherCurrentLiabilities": 4246000,
            "totalCurrentLiabilities": 11416000,
            "longTermDebt": 2564000,
            "deferredRevenueNonCurrent": 0,
            "deferredTaxLiabilitiesNonCurrent": 0,
            "otherNonCurrentLiabilities": 248000,
            "totalNonCurrentLiabilities": 2812000,
            "otherLiabilities": 0,
            "capitalLeaseObligations": 972000,
            "totalLiabilities": 14228000,
            "preferredStock": 0,
            "commonStock": 3450000,
            "retainedEarnings": -82000,
            "accumulatedOtherComprehensiveIncomeLoss": -339000,
            "othertotalStockholdersEquity": 10714000,
            "totalStockholdersEquity": 13743000,
            "totalEquity": 13743000,
            "totalLiabilitiesAndStockholdersEquity": 27971000,
            "minorityInterest": 0,
            "totalLiabilitiesAndTotalEquity": 27971000,
            "totalInvestments": 0,
            "totalDebt": 4330000,
            "netDebt": -6854000,
            "link": "https://www.sec.gov/Archives/edgar/data/96793/000156459020044839/0001564590-20-044839-index.htm",
            "finalLink": "https://www.sec.gov/Archives/edgar/data/96793/000156459020044839/ssy-10k_20200630.htm",
        }
    ]

@pytest.fixture
def prices_in_range_mock():
    return {
        "symbol": "SSY",
        "historical": [
            {
                "date": "2020-02-06",
                "open": 1.19,
                "high": 1.1912,
                "low": 1.14,
                "close": 1.1912,
                "adjClose": 1.19,
                "volume": 15926,
                "unadjustedVolume": 15900,
                "change": 0.0012,
                "changePercent": 0.10084,
                "vwap": 1.18,
                "label": "February 06, 20",
                "changeOverTime": 0.0010084,
            },
            {
                "date": "2020-02-05",
                "open": 1.18,
                "high": 1.2248,
                "low": 1.18,
                "close": 1.2001,
                "adjClose": 1.2,
                "volume": 16993,
                "unadjustedVolume": 17000,
                "change": 0.0201,
                "changePercent": 1.7,
                "vwap": 1.2,
                "label": "February 05, 20",
                "changeOverTime": 0.017,
            },
            {
                "date": "2020-02-04",
                "open": 1.1589,
                "high": 1.414,
                "low": 1.1588,
                "close": 1.25,
                "adjClose": 1.25,
                "volume": 159982,
                "unadjustedVolume": 159700,
                "change": 0.0911,
                "changePercent": 7.86,
                "vwap": 1.26,
                "label": "February 04, 20",
                "changeOverTime": 0.0786,
            },
            {
                "date": "2020-02-03",
                "open": 1.1532,
                "high": 1.2045,
                "low": 1.12,
                "close": 1.14,
                "adjClose": 1.14,
                "volume": 11695,
                "unadjustedVolume": 11700,
                "change": -0.0132,
                "changePercent": -1.14,
                "vwap": 1.14,
                "label": "February 03, 20",
                "changeOverTime": -0.0114,
            }
        ]
    }

@pytest.fixture
def get_current_price_mock():
    return [
        {
            "symbol": "SSY",
            "name": "SunLink Health Systems, Inc.",
            "price": 0.8949,
            "changesPercentage": 2.8621,
            "change": 0.0249,
            "dayLow": 0.8701,
            "dayHigh": 0.8949,
            "yearHigh": 1.47,
            "yearLow": 0.53,
            "marketCap": 6292579,
            "priceAvg50": 0.9296,
            "priceAvg200": 0.94395,
            "exchange": "AMEX",
            "volume": 1250,
            "avgVolume": 7685,
            "open": 0.87,
            "previousClose": 0.87,
            "eps": -0.37,
            "pe": -2.42,
            "earningsAnnouncement": "2023-09-27T14:02:00.000+0000",
            "sharesOutstanding": 7031600,
            "timestamp": 1695656746,
        }
    ]

@pytest.fixture
def balance_sheet_data():
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
            "cashAndCashEquivalents": 6794000,
            "shortTermInvestments": 0,
            "cashAndShortTermInvestments": 6794000,
            "netReceivables": 6385000,
            "inventory": 1748000,
            "otherCurrentAssets": 1888000,
            "totalCurrentAssets": 16815000,
            "propertyPlantEquipmentNet": 9404000,
            "goodwill": 0,
            "intangibleAssets": 1201000,
            "goodwillAndIntangibleAssets": 1201000,
            "longTermInvestments": 0,
            "taxAssets": 0,
            "otherNonCurrentAssets": 523000,
            "totalNonCurrentAssets": 11128000,
            "otherAssets": 0,
            "totalAssets": 27943000,
            "accountPayables": 1347000,
            "shortTermDebt": 392000,
            "taxPayables": 2600000,
            "deferredRevenue": 519000,
            "otherCurrentLiabilities": 5433000,
            "totalCurrentLiabilities": 7691000,
            "longTermDebt": 871000,
            "deferredRevenueNonCurrent": 0,
            "deferredTaxLiabilitiesNonCurrent": 69000,
            "otherNonCurrentLiabilities": 192000,
            "totalNonCurrentLiabilities": 1132000,
            "otherLiabilities": 0,
            "capitalLeaseObligations": 1209000,
            "totalLiabilities": 8823000,
            "preferredStock": 0,
            "commonStock": 3478000,
            "retainedEarnings": 4800000,
            "accumulatedOtherComprehensiveIncomeLoss": 106000,
            "othertotalStockholdersEquity": 10736000,
            "totalStockholdersEquity": 19120000,
            "totalEquity": 19120000,
            "totalLiabilitiesAndStockholdersEquity": 27943000,
            "minorityInterest": 0,
            "totalLiabilitiesAndTotalEquity": 27943000,
            "totalInvestments": 0,
            "totalDebt": 1263000,
            "netDebt": -5531000,
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
            "cashAndCashEquivalents": 9962000,
            "shortTermInvestments": 0,
            "cashAndShortTermInvestments": 9962000,
            "netReceivables": 7775000,
            "inventory": 1890000,
            "otherCurrentAssets": 2314000,
            "totalCurrentAssets": 21941000,
            "propertyPlantEquipmentNet": 7805000,
            "goodwill": 0,
            "intangibleAssets": 1227000,
            "goodwillAndIntangibleAssets": 1227000,
            "longTermInvestments": 0,
            "taxAssets": 0,
            "otherNonCurrentAssets": 591000,
            "totalNonCurrentAssets": 9623000,
            "otherAssets": 0,
            "totalAssets": 31564000,
            "accountPayables": 1096000,
            "shortTermDebt": 3412000,
            "taxPayables": 1966000,
            "deferredRevenue": 437000,
            "otherCurrentLiabilities": 4720000,
            "totalCurrentLiabilities": 9665000,
            "longTermDebt": 927000,
            "deferredRevenueNonCurrent": 0,
            "deferredTaxLiabilitiesNonCurrent": 0,
            "otherNonCurrentLiabilities": 162000,
            "totalNonCurrentLiabilities": 1089000,
            "otherLiabilities": 0,
            "capitalLeaseObligations": 1278000,
            "totalLiabilities": 10754000,
            "preferredStock": 0,
            "commonStock": 3463000,
            "retainedEarnings": 6809000,
            "accumulatedOtherComprehensiveIncomeLoss": -162000,
            "othertotalStockholdersEquity": 10700000,
            "totalStockholdersEquity": 20810000,
            "totalEquity": 20810000,
            "totalLiabilitiesAndStockholdersEquity": 31564000,
            "minorityInterest": 0,
            "totalLiabilitiesAndTotalEquity": 31564000,
            "totalInvestments": 0,
            "totalDebt": 4339000,
            "netDebt": -5623000,
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
            "cashAndCashEquivalents": 11184000,
            "shortTermInvestments": 0,
            "cashAndShortTermInvestments": 11184000,
            "netReceivables": 4315000,
            "inventory": 1866000,
            "otherCurrentAssets": 2558000,
            "totalCurrentAssets": 19923000,
            "propertyPlantEquipmentNet": 6294000,
            "goodwill": 0,
            "intangibleAssets": 1254000,
            "goodwillAndIntangibleAssets": 1254000,
            "longTermInvestments": 0,
            "taxAssets": 0,
            "otherNonCurrentAssets": 500000,
            "totalNonCurrentAssets": 8048000,
            "otherAssets": 0,
            "totalAssets": 27971000,
            "accountPayables": 872000,
            "shortTermDebt": 1766000,
            "taxPayables": 1411000,
            "deferredRevenue": 4532000,
            "otherCurrentLiabilities": 4246000,
            "totalCurrentLiabilities": 11416000,
            "longTermDebt": 2564000,
            "deferredRevenueNonCurrent": 0,
            "deferredTaxLiabilitiesNonCurrent": 0,
            "otherNonCurrentLiabilities": 248000,
            "totalNonCurrentLiabilities": 2812000,
            "otherLiabilities": 0,
            "capitalLeaseObligations": 972000,
            "totalLiabilities": 14228000,
            "preferredStock": 0,
            "commonStock": 3450000,
            "retainedEarnings": -82000,
            "accumulatedOtherComprehensiveIncomeLoss": -339000,
            "othertotalStockholdersEquity": 10714000,
            "totalStockholdersEquity": 13743000,
            "totalEquity": 13743000,
            "totalLiabilitiesAndStockholdersEquity": 27971000,
            "minorityInterest": 0,
            "totalLiabilitiesAndTotalEquity": 27971000,
            "totalInvestments": 0,
            "totalDebt": 4330000,
            "netDebt": -6854000,
            "link": "https://www.sec.gov/Archives/edgar/data/96793/000156459020044839/0001564590-20-044839-index.htm",
            "finalLink": "https://www.sec.gov/Archives/edgar/data/96793/000156459020044839/ssy-10k_20200630.htm",
        }
    ]

@pytest.fixture
def rate_of_change_variables():
    return {
        "prev_value": 7.34,
        "current_value": 8.11,
        "rate_of_change": 0.105,
    }

@pytest.fixture
def rates_of_change_variables():
    return {
        "iterator": [59557767, 55689016, 41435577, 45719024],
        "rates_of_change": [None, 0.069, 0.344, -0.094],
    }

@pytest.fixture
def inversion_variables():
    return {
        "iterator": [59557767, 55689016, 41435577, 45719024],
        "inverted_iterator" : [45719024, 41435577, 55689016, 59557767],
    }

@pytest.fixture
def drop_nulls_variables():
    return {
        "iterator": [None, np.nan, 55689016, 41435577, 45719024],
        "iterator_wo_null" : [55689016, 41435577, 45719024],
    }

@pytest.fixture
def bounds_variables():
    return {
        "iterator" : [-200, 100, 101, 102, 103, 108, 180, 500],
        "bounds" : (25.0, 201.75),
    }

@pytest.fixture
def avg_variables():
    return {
        "iterator": [59557767, 55689016, 41435577, 45719023],
        "avg" : 50600345.75,
    }

@pytest.fixture
def get_date_variables():
    return {
        "date_key": "2020-06-30",
    }

@pytest.fixture
def negative_vals_variables():
    return {
        "iter_w_negative_vals": [-1, 1, 2],
        "iter_wo_negative_vals": [0, 1, 2],
    }

@pytest.fixture
def growth_function_variables():
    return {
        "pos_pos1": {
            "previous": 20000,
            "current": 60000,
            "nb_years": 5,
            "growth": 0.246,
        },
        "pos_pos2": {
            "previous": 60000,
            "current": 20000,
            "nb_years": 5,
            "growth": -0.197,
        },
        "pos_neg1": {
            "previous": 20000,
            "current": -60000,
            "nb_years": 5,
            "growth": -0.275,
        },
        "pos_neg2": {
            "previous": 60000,
            "current": -20000,
            "nb_years": 5,
            "growth": -0.156,
        },
        "neg_pos1": {
            "previous": -20000,
            "current": 60000,
            "nb_years": 5,
            "growth": 0.379,
        },
        "neg_pos2": {
            "previous": -60000,
            "current": 20000,
            "nb_years": 5,
            "growth": 0.185,
        },
        "neg_neg1": {
            "previous": -20000,
            "current": -60000,
            "nb_years": 5,
            "growth": -0.197,
        },
        "neg_neg2": {
            "previous": -60000,
            "current": -20000,
            "nb_years": 5,
            "growth": 0.246,
        },
    }
