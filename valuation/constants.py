# Financial stmts constants
EPS_KEY = "eps"
TOTAL_ASSETS_KEY = "totalAssets"
GOODWILL_KEY = "goodwill"
INTANGIBLE_ASSETS_KEY = "intangibleAssets"
TOTAL_LIAB_KEY = "totalLiabilities"
GOODWILL_AND_INTANGILE_ASSETS_KEY = "goodwillAndIntangibleAssets"
SHARES_OUTS_KEY = "weightedAverageShsOutDil"
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
COLS_TO_PLOT = [
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
COLS_WITH_SAME_SCALE = [
    ("totalAssets", "totalLiabilities"),
    ("de_ratio1", "de_ratio2", "de_ratio3"),
]
