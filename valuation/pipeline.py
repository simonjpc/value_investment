import sys
import pandas as pd
import concurrent.futures
from sqlalchemy import create_engine
from valuation.extraction import get_income_stmt_info, get_balance_sheet_info
from valuation.utils import drop_df_cols, add_suffix_to_cols, dict_to_df, batch_tickers
from valuation.data_injection import Injector
from valuation.data_loading import DataLoader
from valuation.constants import (
    INCOME_STMT_COLS_TO_DROP,
    FINANCIAL_STMT_DUMP_QUERY,
    FINANCIAL_STMT_TABLE_NAME,
    TICKERS_PATH,
)
import logging
import time

logging.basicConfig(
    stream=sys.stdout, level=logging.getLevelName("INFO")
)
log = logging.getLogger(__name__)

def define_engine()
def single_ticker_pipeline(ticker, connection):
    income_stmt = get_income_stmt_info(ticker=ticker, period="quarter", limit=120)
    balance_sheet = get_balance_sheet_info(ticker=ticker, period="quarter", limit=120)
    log.info("balance sheet & income stmt data loaded.")

    if not all([len(history) for history in (income_stmt, balance_sheet)]):
        return False

    income_stmt_df = dict_to_df(fa_info=income_stmt)
    balance_sheet_df = dict_to_df(fa_info=balance_sheet)
    log.info("balance sheet & income stmt dicts transformed into df.")
    
    try:
        income_stmt_df = income_stmt_df.set_index("date")
        balance_sheet_df = balance_sheet_df.set_index("date")
    except:
        print(ticker)
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
        injector.df_dump(df=financial_info, connection=connection)
    except:
        raise("data dump failed")
    log.info("data dump successful.")
    return True

if __name__ == "__main__":
    #start = time.time()
    # create table if it does not exist
    injector = Injector()
    dataloader = DataLoader()
    engine = create_engine(injector.db_uri)
    connection = engine.connect()
    injector.create_table(
        FINANCIAL_STMT_DUMP_QUERY.format(table_name=FINANCIAL_STMT_TABLE_NAME),
        connection,
    )
    # multiprocessing
    tickers = dataloader.load_tickers_from_txt(TICKERS_PATH)
    ticker_batches = batch_tickers(tickers=tickers, batch_size=100)
    # We execute this per batch considering the limit of the api
    for idx, batch in enumerate(ticker_batches):
        log.info(f"Starting batch {idx + 1} with {len(batch)} tickers...")
        executor = concurrent.futures.ProcessPoolExecutor()
        dumping_futures = [
            executor.submit(single_ticker_pipeline, args=(ticker, connection)) for ticker in batch
        ]
        for future in concurrent.futures.as_completed(dumping_futures):
            dumping_flag = future.result()
        log.info(f"batch {idx + 1} executed")
        log.info(f"waiting 1 min...")
        time.sleep(60)
        log.info(f"Restarting")
    connection.close()
    engine.dispose()

    #end = time.time()
    #log.info(f"execution time: {end - start}")
