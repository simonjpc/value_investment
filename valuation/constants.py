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
