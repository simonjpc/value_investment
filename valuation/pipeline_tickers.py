import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from valuation.constants import ALL_TICKERS_DUMP_QUERY, CREATE_INDEX_QUERY
from valuation.data_injection import Injector
from valuation.extraction import get_all_delisted_tickers_list, get_all_tickers_list
from valuation.utils import list_to_single_col_df
from celery_app import app

injector = Injector()
engine = create_engine(
    injector.db_uri,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
)


def tickers_pipeline(
    table_name: str,
    connection: sqlalchemy.engine,
    delisted_flag: bool = False,
) -> None:
    if delisted_flag:
        all_tickers = get_all_delisted_tickers_list()
    else:
        all_tickers = get_all_tickers_list()
    df = list_to_single_col_df(all_tickers, col_name="ticker")
    df.index.name = "id"
    injector.df_to_db(
        df=df,
        table_name=table_name,
        conn=connection,
        idx_flag=True,
    )


@app.task()
def tickers_data(
    self,
):

    with engine.connect() as connection:
        # public companies
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

        # delisted companies
        injector.execute_query(
            query=ALL_TICKERS_DUMP_QUERY.format(table_name="delisted_company_tickers"),
            connection=connection,
        )
        injector.execute_query(
            query=CREATE_INDEX_QUERY.format(
                index_name="ticker_id_index",
                table_name="delisted_company_tickers",
                column_name="id",
            ),
            connection=connection,
        )
        injector.execute_query(
            query=CREATE_INDEX_QUERY.format(
                index_name="ticker_str_index",
                table_name="delisted_company_tickers",
                column_name="ticker",
            ),
            connection=connection,
        )

        tickers_pipeline(
            table_name="delisted_company_tickers",
            connection=connection,
            delisted_flag=True,
        )

    engine.dispose()
    print("all tickers extracted")


if __name__ == "__main__":

    tickers_data()
