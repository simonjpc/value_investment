# Financial stmts constants
EPS_KEY = "eps"
TOTAL_ASSETS_KEY = "totalAssets"
GOODWILL_KEY = "goodwill"
INTANGIBLE_ASSETS_KEY = "intangibleAssets"
TOTAL_LIAB_KEY = "totalLiabilities"
GOODWILL_AND_INTANGILE_ASSETS_KEY = "goodwillAndIntangibleAssets"
SHARES_OUTS_KEY = "weightedAverageShsOutDil"
CASH_AND_EQUIV_KEY = "cashAndCashEquivalents"
NET_RECEIVABLES_KEY = "netReceivables"
INVENTORY_KEY = "inventory"
PPE_KEY = "propertyPlantEquipmentNet"
TOTAL_CURR_ASSETS_KEY = "totalCurrentAssets"
TOTAL_CURR_LIAB_KEY = "totalCurrentLiabilities"
STOCKHOLDERS_EQUITY_KEY = "totalStockholdersEquity"
TOTAL_DEBT_KEY = "totalDebt"
EXPECTED_OBLIGATIONS = (TOTAL_CURR_LIAB_KEY, TOTAL_LIAB_KEY, TOTAL_DEBT_KEY)
DATE_KEY = "date"
FILLING_DATE_KEY = "fillingDate"
HIST_PRICES_KEY = "historical"
PRICE_KEY = "price"

# Present faire value constants
GROWTH_RATE_CAP = 0.40
PE_RATIO_CAP = 20
RETURN_RATE_CAP = 0.20

# API constants
VERSION = "v3"
API_BASE_PATH = f"https://financialmodelingprep.com/api/{VERSION}"

# Current Assets elements constants
RECEIVABLES_FACTOR_KEY = "receivables_factor"
INVENTORY_FACTOR_KEY = "inventory_factor"
PPE_FACTOR_KEY = "ppe_factor"
CURRENT_ASSETS_FACTORS = {
    RECEIVABLES_FACTOR_KEY: 0.8,
    INVENTORY_FACTOR_KEY: 0.6,
    PPE_FACTOR_KEY: 0.67,
}

# Columns constants
REPORTING_DATE_PRICE_COL = "reporting_date_price"
COLS_TO_PLOT_EPSX = [
    "pfvps",
    "pe_ratio",
    "revenue",
    "netIncome",
    "eps",
    "totalAssets",
    "totalLiabilities",
    "totalEquity",
    "tangible_book_value_ps",
    "weightedAverageShsOutDil",
    "de_ratio1",
    "de_ratio2",
    "de_ratio3",
]
COLS_TO_PLOT_NCAV = [
    "ncavps",
    "liqvps",
    "totalCurrentAssets",
    "totalCurrentLiabilities",
    "current_ratio",
    "totalAssets",
    "totalLiabilities",
    "weightedAverageShsOutDil",
    "de_ratio1",
    "de_ratio2",
    "de_ratio3",
]
COLS_WITH_SAME_SCALE = [
    ["totalCurrentAssets", "totalCurrentLiabilities"],
    ["totalAssets", "totalLiabilities"],
    ["de_ratio1", "de_ratio2", "de_ratio3"],
]
PRICES_INFO_COLUMNS = [
    "date",
    "weekday",
    "symbol",
    "low",
    "high",
    "open",
    "close",
    "volume",
]
HIST_PRICES_DATE_COL = PRICES_INFO_COLUMNS[0]
WEEKDAY_COL = "weekday"
SUBPLOT_NAMES = {
    "ncavps": "ncavps",
    "liqvps": "liqvps",
    "pfvps": "pfvps",
    "totalCurrentAssets": "current assets",
    "totalCurrentLiabilities": "current liab",
    "current_ratio": "current ratio",
    "pe_ratio": "pe_ratio",
    "revenue": "revenue",
    "netIncome": "net income",
    "eps": "eps",
    "totalAssets": "total assets",
    "totalLiabilities": "total liab",
    "totalEquity": "total equity",
    "tangible_book_value_ps": "tangible bv",
    "weightedAverageShsOutDil": "outs shares",
    "de_ratio1": "total liab / tot equity",
    "de_ratio2": "curr liab / tot equity",
    "de_ratio3": "net debt / tot equity",
}

# TABLES
FINANCIAL_STMT_DUMP_QUERY = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        date date,
        symbol_bs varchar,
        "reportedCurrency_bs" varchar,
        cik_bs varchar,
        "fillingDate_bs" timestamp,
        "acceptedDate_bs" timestamp,
        "calendarYear_bs" integer,
        period_bs character(2),
        "cashAndCashEquivalents_bs" numeric, -- previous bigint til dump crash
        "shortTermInvestments_bs" numeric, -- previous bigint til dump crash
        "cashAndShortTermInvestments_bs" numeric, -- previous bigint til dump crash
        "netReceivables_bs" numeric, -- previous bigint til dump crash
        inventory_bs numeric, -- previous bigint til dump crash
        "otherCurrentAssets_bs" numeric, -- previous bigint til dump crash
        "totalCurrentAssets_bs" numeric, -- previous bigint til dump crash
        "propertyPlantEquipmentNet_bs" numeric, -- previous bigint til dump crash
        goodwill_bs numeric, -- previous bigint til dump crash
        "intangibleAssets_bs" numeric, -- previous bigint til dump crash
        "goodwillAndIntangibleAssets_bs" numeric, -- previous bigint til dump crash
        "longTermInvestments_bs" numeric, -- previous bigint til dump crash
        "taxAssets_bs" numeric, -- previous bigint til dump crash
        "otherNonCurrentAssets_bs" numeric, -- previous bigint til dump crash
        "totalNonCurrentAssets_bs" numeric, -- previous bigint til dump crash
        "otherAssets_bs" numeric, -- previous bigint til dump crash
        "totalAssets_bs" numeric, -- previous bigint til dump crash
        "accountPayables_bs" numeric, -- previous bigint til dump crash
        "shortTermDebt_bs" numeric, -- previous bigint til dump crash
        "taxPayables_bs" numeric, -- previous bigint til dump crash
        "deferredRevenue_bs" numeric, -- previous bigint til dump crash
        "otherCurrentLiabilities_bs" numeric, -- previous bigint til dump crash
        "totalCurrentLiabilities_bs" numeric, -- previous bigint til dump crash
        "longTermDebt_bs" numeric, -- previous bigint til dump crash
        "deferredRevenueNonCurrent_bs" numeric, -- previous bigint til dump crash
        "deferredTaxLiabilitiesNonCurrent_bs" numeric, -- previous bigint til dump crash
        "otherNonCurrentLiabilities_bs" numeric, -- previous bigint til dump crash
        "totalNonCurrentLiabilities_bs" numeric, -- previous bigint til dump crash
        "otherLiabilities_bs" numeric, -- previous bigint til dump crash
        "capitalLeaseObligations_bs" numeric, -- previous bigint til dump crash
        "totalLiabilities_bs" numeric, -- previous bigint til dump crash
        "preferredStock_bs" numeric, -- previous bigint til dump crash
        "commonStock_bs" numeric, -- previous bigint til dump crash
        "retainedEarnings_bs" numeric, -- previous bigint til dump crash
        "accumulatedOtherComprehensiveIncomeLoss_bs" numeric, -- previous bigint til dump crash
        "othertotalStockholdersEquity_bs" numeric, -- previous bigint til dump crash
        "totalStockholdersEquity_bs" numeric, -- previous bigint til dump crash
        "totalEquity_bs" numeric, -- previous bigint til dump crash
        "totalLiabilitiesAndStockholdersEquity_bs" numeric, -- previous bigint til dump crash
        "minorityInterest_bs" numeric, -- previous bigint til dump crash
        "totalLiabilitiesAndTotalEquity_bs" numeric, -- previous bigint til dump crash
        "totalInvestments_bs" numeric, -- previous bigint til dump crash
        "totalDebt_bs" numeric, -- previous bigint til dump crash
        "netDebt_bs" numeric, -- previous bigint til dump crash
        link_bs varchar,
        "finalLink_bs" varchar,
        revenue_is numeric, -- previous bigint til dump crash
        "costOfRevenue_is" numeric, -- previous bigint til dump crash
        "grossProfit_is" numeric, -- previous bigint til dump crash
        "grossProfitRatio_is" numeric, -- previous integer til dump crash
        "researchAndDevelopmentExpenses_is" numeric, -- previous bigint til dump crash
        "generalAndAdministrativeExpenses_is" numeric, -- previous bigint til dump crash
        "sellingAndMarketingExpenses_is" numeric, -- previous bigint til dump crash
        "sellingGeneralAndAdministrativeExpenses_is" numeric, -- previous bigint til dump crash
        "otherExpenses_is" numeric, -- previous bigint til dump crash
        "operatingExpenses_is" numeric, -- previous bigint til dump crash
        "costAndExpenses_is" numeric, -- previous bigint til dump crash
        "interestIncome_is" numeric, -- previous bigint til dump crash
        "interestExpense_is" numeric, -- previous bigint til dump crash
        "depreciationAndAmortization_is" numeric, -- previous bigint til dump crash
        ebitda_is numeric, -- previous bigint til dump crash
        ebitdaratio_is numeric,
        "operatingIncome_is" numeric, -- previous bigint til dump crash
        "operatingIncomeRatio_is" numeric,
        "totalOtherIncomeExpensesNet_is" numeric, -- previous bigint til dump crash
        "incomeBeforeTax_is" numeric, -- previous bigint til dump crash
        "incomeBeforeTaxRatio_is" numeric,
        "incomeTaxExpense_is" numeric, -- previous bigint til dump crash
        "netIncome_is" numeric, -- previous bigint til dump crash
        "netIncomeRatio_is" numeric,
        eps_is numeric, -- previous integer til dump crash
        epsdiluted_is numeric, -- previous integer til dump crash
        "weightedAverageShsOut_is" numeric, -- previous bigint til dump crash
        "weightedAverageShsOutDil_is" numeric -- previous bigint til dump crash
    )
"""


CREATE_INDEX_QUERY = """
    CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name})
"""

DAILY_PRICES_HISTORY_DUMP_QUERY = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        date date,
        weekday integer,
        symbol varchar,
        low numeric,
        high numeric,
        open numeric,
        close numeric,
        volume numeric
    )
"""

ALL_TICKERS_DUMP_QUERY = """
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    ticker varchar
)
"""

BACKTESTING_OUTPUT_QUERY = """
CREATE TABLE IF NOT EXISTS {table_name} (
    ticker varchar,
    ref_report_date timestamp,
    report_date timestamp,
    ref_report_date_quarter varchar,
    report_date_quarter varchar,
    outs_shares1 numeric,
    outs_shares2 numeric,
    outs_shares3 numeric,
    outs_shares4 numeric,
    outs_shares5 numeric,
    outs_shares6 numeric,
    outs_shares7 numeric,
    outs_shares8 numeric,
    outs_shares9 numeric,
    outs_shares10 numeric,
    outs_shares_slope_pct_10y numeric,
    outs_shares_slope_pct_5y numeric,
    min_price_date timestamp,
    min_price numeric,
    max_price_date timestamp,
    max_price numeric,
    ncavps numeric,
    liqvps numeric,
    ncav_mos numeric,
    liqv_mos numeric,
    highest_return_delay numeric,
    doubling_price numeric,
    doubling_date timestamp,
    doubling_return_delay numeric,
    highest_return numeric,
    min_price_modif numeric,
    max_price_modif numeric,
    ncav_mos_modif numeric,
    liqv_mos_modif numeric,
    doubling_price_modif numeric,
    highest_return_modif numeric,
    ticker_type varchar
)
"""

ALL_TICKERS_QUERY = """
    SELECT ticker
    FROM company_tickers
"""

LAST_TICKER_FINANCIAL_STMT_QUERY = """
    SELECT *
    FROM financial_stmts
    WHERE symbol_bs = '{ticker}'
    ORDER BY date DESC
    LIMIT 1;
"""

TICKER_FINANCIAL_STMTS_IN_RANGE_QUERY = """
    SELECT *
    FROM financial_stmts
    WHERE symbol_bs = '{ticker}' and period_bs = '{period}'
"""

BACKTESTING_COL_NAMES = [
    "ticker",
    "ref_report_date",
    "report_date",
    "ref_report_date_quarter",
    "report_date_quarter",
    "outs_shares1",
    "outs_shares2",
    "outs_shares3",
    "outs_shares4",
    "outs_shares5",
    "outs_shares6",
    "outs_shares7",
    "outs_shares8",
    "outs_shares9",
    "outs_shares10",
    "outs_shares_slope_pct_10y",
    "outs_shares_slope_pct_5y",
    "min_price_date",
    "min_price",
    "max_price_date",
    "max_price",
    "ncavps",
    "liqvps",
    "ncav_mos",
    "liqv_mos",
    "highest_return_delay",
    "doubling_price",
    "doubling_date",
    "doubling_return_delay",
    "highest_return",
    "min_price_modif",
    "max_price_modif",
    "ncav_mos_modif",
    "liqv_mos_modif",
    "doubling_price_modif",
    "highest_return_modif",
    "ticker_type",
]

INSERT_ELEMENT_IN_COL_QUERY = """
INSERT INTO {table_name} ({col_name}) VALUES ('{element}')
"""

GET_ALL_LISTED_TICKERS_QUERY = """
SELECT ticker
FROM company_tickers
"""

GET_ALL_DELISTED_TICKERS_QUERY = """
SELECT ticker
FROM delisted_company_tickers
"""

OLDEST_AND_NEWEST_FILLING_DATES_PER_SYMBOL_QUERY = """
    SELECT 
        symbol_bs,
        MIN("fillingDate_bs") AS fillingdate_oldest,
        MAX("fillingDate_bs") AS fillingdate_newest
    FROM
        financial_stmts
    GROUP BY
        symbol_bs;
"""
FINANCIAL_STMT_TABLE_NAME = "financial_stmts"
PRICES_HISTORY_TABLE_NAME = "prices_history"
ALL_TICKERS_TABLE_NAME = "company_tickers"
ALL_DELISTED_TICKERS_TABLE_NAME = "delisted_company_tickers"
BACKTESTING_TABLE_NAME = "backtesting_output"
SQLALCHEMY_DB_PATH = "postgresql://{user}:{password}@{host}:{port}/{db}"
INCOME_STMT_COLS_TO_DROP = [
    "symbol",
    "reportedCurrency",
    "cik",
    "fillingDate",
    "acceptedDate",
    "calendarYear",
    "period",
    "finalLink",
    "link",
]
TICKER_IDX_NAME = "symbol_index"
TICKER_COL_NAME = "symbol_bs"

# Paths constants
TICKERS_PATH_RECENT = "./tickers_list_03092023.txt"
TICKERS_PATH_ANCIENT = "./tickers_list_28062023.txt"

# Formats
DATE_FORMAT = "%Y-%m-%d"

# Delisted objects
FUNDS_STOPWORDS = ["fund", "etf", "proshares"]
DELISTED_COMPANY_NAME_KEY = "companyName"

# Exchange rates to USD
BASE_CURRENCY = "USD"
RATES_TO_USD = {
    "AED": 3.672799,
    "ARS": 814.376084,
    "AUD": 1.496603,
    "BDT": 109.702905,
    "BGN": 1.791634,
    "BRL": 4.897503,
    "CAD": 1.339525,
    "CHF": 0.852625,
    "CLP": 919.929947,
    "CNY": 7.1118,
    "COP": 3944,
    "CZK": 22.493403,
    "DKK": 6.8256,
    "EGP": 30.897791,
    "EUR": 0.915345,
    "GBP": 0.787603,
    "GEL": 2.685038,
    "GHS": 11.910749,
    "HKD": 7.81585,
    "HUF": 346.759582,
    "IDR": 15543.75,
    "ILS": 3.73325,
    "INR": 83.11485,
    "ISK": 137.579912,
    "JPY": 144.61303,
    "KES": 158.249861,
    "KRW": 1320.880304,
    "KWD": 0.307497,
    "KYD": 0.833067,
    "KZT": 454.528828,
    "LBP": 15024.461616,
    "MAD": 9.952906,
    "MOP": 8.046637,
    "MXN": 16.95184,
    "MYR": 4.643498,
    "NGN": 914.502147,
    "NOK": 10.35816,
    "NZD": 1.60471,
    "PEN": 3.696036,
    "PGK": 3.732797,
    "PHP": 56.126502,
    "PLN": 3.97565,
    "QAR": 3.641501,
    "RON": 4.550961,
    "RSD": 107.307017,
    "RUB": 90.902679,
    "SAR": 3.750137,
    "SEK": 10.264785,
    "SGD": 1.331585,
    "THB": 35.005965,
    "TRY": 29.92213,
    "TWD": 31.093499,
    "USD": 1,
    "VND": 24370,
    "XAF": 599.8418,
    "ZAR": 18.68205,
    "ZMW": 25.965891,
}

# queries
DATE_PERIOD_CURRENCY_PER_SYMBOL = """
    SELECT "fillingDate_bs", period_bs, "reportedCurrency_bs"
    FROM financial_stmts
    WHERE symbol_bs = '{test_symbol}'
"""

ALL_INFO_PER_SYMBOL_PERIOD_DATERANGE = """
    select *
    from financial_stmts
    where symbol_bs = '{test_symbol}' and
        period_bs = '{oldest_period}' and
        "fillingDate_bs" >= '{oldest_date}' and
        "fillingDate_bs" <= '{offset_date}'
"""

DATES_PERIOD_PER_DATE_SYMBOL = """
    SELECT date, "fillingDate_bs", period_bs
    FROM financial_stmts
    WHERE date > '{least_oldest_date}' and symbol_bs = '{test_symbol}'
    ORDER BY date
    LIMIT 1;
"""

ALL_PRICE_HIST_PER_SYMBOL_DATES = """
    select *
    from prices_history
    where symbol = '{test_symbol}' and date >= '{least_oldest_date}' and date <= '{plateau_date}'
"""

ALL_PRICE_HIST_PER_DATE_OFFSET_SYMBOL = """
    select *
    from prices_history
    where date >= '{oldest_lowest_date}' and date <= '{offset_3y}' and symbol = '{test_symbol}'
"""

ALL_PRICE_HIST_PER_E_VAL_SYMBOL_DATE_OFFSET = """
    SELECT *
    FROM prices_history
    WHERE high > {expected_return} and symbol = '{test_symbol}' and date >= '{oldest_lowest_date}' and date <= '{offset_3y}'
    ORDER BY high
    LIMIT 1;
"""

ALL_PER_SYMBOL_TYPE = """
    select *
    from {symbol_type_table}
"""

POTENTIAL_CANDIDATES_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS {table_name} (
    ticker VARCHAR NOT NULL,
    price numeric
)
"""
