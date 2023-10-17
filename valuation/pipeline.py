import sys
import pandas as pd
from valuation.extraction import get_income_stmt_info, get_balance_sheet_info
from valuation.data_injection import Injector
from valuation.utils import drop_df_cols, add_suffix_to_cols, dict_to_df
from valuation.constants import INCOME_STMT_COLS_TO_DROP
import logging

logging.basicConfig(
    stream=sys.stdout, level=logging.getLevelName("INFO")
)
log = logging.getLogger(__name__)

def single_ticker_pipeline(ticker):
    income_stmt = get_income_stmt_info(ticker=ticker, period="quarter", limit=50)
    balance_sheet = get_balance_sheet_info(ticker=ticker, period="quarter", limit=50)
    log.info("balance sheet & income stmt data loaded.")
    income_stmt_df = dict_to_df(fa_info=income_stmt)
    balance_sheet_df = dict_to_df(fa_info=balance_sheet)
    log.info("balance sheet & income stmt dicts transformed into df.")
    income_stmt_df = income_stmt_df.set_index("date")
    balance_sheet_df = balance_sheet_df.set_index("date")
    log.info("`date` col added as index.")
    income_stmt_df = drop_df_cols(income_stmt_df, cols=INCOME_STMT_COLS_TO_DROP)
    log.info("repeated cols dropped from income statement source.")
    income_stmt_df = add_suffix_to_cols(df=income_stmt_df, suffix="_is")
    balance_sheet_df = add_suffix_to_cols(df=balance_sheet_df, suffix="_bs")
    log.info("balance sheet & income stmt df cols modified with suffixes")
    financial_info = pd.concat([balance_sheet_df, income_stmt_df], axis=1)
    financial_info = financial_info.reset_index()

    log.info("concatenation succeeded.")
    injector = Injector()
    try:
        injector.df_dump(df=financial_info)
    except BaseException:
        raise("data dump failed")
    log.info("data dump successful.")

if __name__ == "__main__":
    single_ticker_pipeline(ticker="JCTCF")
