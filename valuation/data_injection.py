import os
from typing import Any, Dict

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text

from valuation.constants import (FINANCIAL_STMT_DUMP_QUERY,
                                 FINANCIAL_STMT_TABLE_NAME, SQLALCHEMY_DB_PATH)


class Injector:
    def __init__(self):
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PWD")
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")
        self.db = os.environ.get("DB_NAME")
        self.db_uri = SQLALCHEMY_DB_PATH.format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db,
        )

    def df_to_db(
        self,
        df: pd.DataFrame,
        table_name: str,
        conn: sqlalchemy.engine,
        if_exists: str = "append",
        idx_flag: bool = False,
    ) -> None:
        df.to_sql(table_name, con=conn, if_exists=if_exists, index=idx_flag)
        
    def execute_query(self, query: str, connection: sqlalchemy.engine) -> None:
        connection.execute(text(query))
        connection.commit()

    # DEPRICATED
    def define_index(self, query: str, connection: sqlalchemy.engine) -> None:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        connection.execute(text(query))

    # DEPRICATED
    def create_table(self, query: str, connection: sqlalchemy.engine) -> None:
        #engine = create_engine(self.db_uri)
        #with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        connection.execute(text(query))

    def df_dump(self, df: Dict[str, Any], engine: sqlalchemy.engine) -> None:
        #engine = create_engine(self.db_uri)
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            self.df_to_db(
                df=df,
                table_name=FINANCIAL_STMT_TABLE_NAME,
                conn=connection,
            )
