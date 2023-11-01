from valuation.constants import ALL_TICKERS_DUMP_QUERY, CREATE_INDEX_QUERY
from valuation.extraction import get_all_tickers_list
from valuation.utils import list_to_single_col_df
from valuation.data_injection import Injector
from  sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import  sqlalchemy

def tickers_pipeline(table_name: str, connection: sqlalchemy.engine) -> None:
    all_tickers = get_all_tickers_list()
    df = list_to_single_col_df(all_tickers, col_name="ticker")
    df.index.name = "id"
    injector.df_to_db(
        df=df,
        table_name=table_name,
        conn=connection,
        idx_flag=True,
    )


if __name__ == "__main__":
    injector = Injector()
    engine = create_engine(
        injector.db_uri,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
    )
    try:
        with engine.connect() as connection:
            injector.execute_query(
                query=ALL_TICKERS_DUMP_QUERY.format(table_name="company_tickers"),
                connection=connection,
            )
            injector.execute_query(
                query=CREATE_INDEX_QUERY.format(
                    index_name="ticker_id_index",
                    table_name="company_tickers",
                    column_name="id",
                ),
                connection=connection,
            )
            injector.execute_query(
                query=CREATE_INDEX_QUERY.format(
                    index_name="ticker_str_index",
                    table_name="company_tickers",
                    column_name="ticker",
                ),
                connection=connection,
            )

            tickers_pipeline(
                table_name="company_tickers",
                connection=connection,
            )
    finally:
        engine.dispose()
