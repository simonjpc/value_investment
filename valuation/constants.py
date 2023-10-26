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
        "cashAndCashEquivalents_bs" bigint,
        "shortTermInvestments_bs" bigint,
        "cashAndShortTermInvestments_bs" bigint,
        "netReceivables_bs" bigint,
        inventory_bs bigint,
        "otherCurrentAssets_bs" bigint,
        "totalCurrentAssets_bs" bigint,
        "propertyPlantEquipmentNet_bs" bigint,
        goodwill_bs bigint,
        "intangibleAssets_bs" bigint,
        "goodwillAndIntangibleAssets_bs" bigint,
        "longTermInvestments_bs" bigint,
        "taxAssets_bs" bigint,
        "otherNonCurrentAssets_bs" bigint,
        "totalNonCurrentAssets_bs" bigint,
        "otherAssets_bs" bigint,
        "totalAssets_bs" bigint,
        "accountPayables_bs" bigint,
        "shortTermDebt_bs" bigint,
        "taxPayables_bs" bigint,
        "deferredRevenue_bs" bigint,
        "otherCurrentLiabilities_bs" bigint,
        "totalCurrentLiabilities_bs" bigint,
        "longTermDebt_bs" bigint,
        "deferredRevenueNonCurrent_bs" bigint,
        "deferredTaxLiabilitiesNonCurrent_bs" bigint,
        "otherNonCurrentLiabilities_bs" bigint,
        "totalNonCurrentLiabilities_bs" bigint,
        "otherLiabilities_bs" bigint,
        "capitalLeaseObligations_bs" bigint,
        "totalLiabilities_bs" bigint,
        "preferredStock_bs" bigint,
        "commonStock_bs" bigint,
        "retainedEarnings_bs" bigint,
        "accumulatedOtherComprehensiveIncomeLoss_bs" bigint,
        "othertotalStockholdersEquity_bs" bigint,
        "totalStockholdersEquity_bs" bigint,
        "totalEquity_bs" bigint,
        "totalLiabilitiesAndStockholdersEquity_bs" bigint,
        "minorityInterest_bs" bigint,
        "totalLiabilitiesAndTotalEquity_bs" bigint,
        "totalInvestments_bs" bigint,
        "totalDebt_bs" bigint,
        "netDebt_bs" bigint,
        link_bs varchar,
        "finalLink_bs" varchar,
        revenue_is bigint,
        "costOfRevenue_is" bigint,
        "grossProfit_is" bigint,
        "grossProfitRatio_is" integer,
        "researchAndDevelopmentExpenses_is" bigint,
        "generalAndAdministrativeExpenses_is" bigint,
        "sellingAndMarketingExpenses_is" bigint,
        "sellingGeneralAndAdministrativeExpenses_is" bigint,
        "otherExpenses_is" bigint,
        "operatingExpenses_is" bigint,
        "costAndExpenses_is" bigint,
        "interestIncome_is" bigint,
        "interestExpense_is" bigint,
        "depreciationAndAmortization_is" bigint,
        ebitda_is bigint,
        ebitdaratio_is integer,
        "operatingIncome_is" bigint,
        "operatingIncomeRatio_is" integer,
        "totalOtherIncomeExpensesNet_is" bigint,
        "incomeBeforeTax_is" bigint,
        "incomeBeforeTaxRatio_is" integer,
        "incomeTaxExpense_is" bigint,
        "netIncome_is" bigint,
        "netIncomeRatio_is" integer,
        eps_is integer,
        epsdiluted_is integer,
        "weightedAverageShsOut_is" bigint,
        "weightedAverageShsOutDil_is" bigint
    )
"""


CREATE_INDEX_QUERY = """
    CREATE INDEX {index_name} ON {table_name} ({column_name})
"""

DAILY_PRICES_HISTORY_DUMP_QUERY = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        date date,
        date_weekday integer,
        symbol_bs varchar,
        "reportedCurrency_bs" varchar,
        "fillingDate_bs" timestamp,
        "fillingDate_weekday" integer,
        "acceptedDate_bs" timestamp,
        "acceptedDate_weekday" integer,
        price_low numeric,
        price_high numeric,
        price_open numeric,
        price_close numeric,
        price_avg numeric,
        volume_avg numeric,
    )
"""

OLDEST_FILLING_DATE_PER_SYMBOL_QUERY = """
    SELECT symbol_bs, "fillingDate_bs"
    FROM financial_stmts stmts1
    WHERE "fillingDate_bs" = (
        SELECT MIN("fillingDate_bs")
        FROM financial_stmts stmts2
        WHERE stmts1.symbol_bs = stmts2.symbol_bs
    )
"""
FINANCIAL_STMT_TABLE_NAME = "financial_stmts"
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
TICKERS_PATH = "./tickers_list_03092023.txt"
