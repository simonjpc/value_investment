# Financial stmts constants
EPS_KEY = "eps"
TOTAL_ASSETS_KEY = "totalAssets"
GOODWILL_KEY = "goodwill"
INTANGIBLE_ASSETS_KEY = "intangibleAssets"
TOTAL_LIAB_KEY = "totalLiabilities"
GOODWILL_AND_INTANGILE_ASSETS_KEY = "goodwillAndIntangibleAssets"
SHARES_OUTS_KEY = "weightedAverageShsOutDil"
CASH_AND_EQUIV_KEY  = "cashAndCashEquivalents"
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
        "grossProfitRatio_is" integer,
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
        eps_is integer,
        epsdiluted_is integer,
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
