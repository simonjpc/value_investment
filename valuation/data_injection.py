import os
import pandas as pd
from typing import Dict, Any
import sqlalchemy
from sqlalchemy import create_engine, text
from valuation.constants import FINANCIAL_STMT_DUMP_QUERY, FINANCIAL_STMT_TABLE_NAME, SQLALCHEMY_DB_PATH

class Injector:
    def __init__(self):
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PWD")
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")
        self.db = os.environ.get("DB_NAME")

    def df_to_db(self, df: pd.DataFrame, table_name: str, conn: sqlalchemy.engine) -> None:
        df.to_sql(table_name, con=conn, if_exists="replace", index=False)

    def df_dump(self, df: Dict[str, Any]) -> None:
        db_uri = SQLALCHEMY_DB_PATH.format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db,
        )
        engine = create_engine(db_uri)
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute(
                text(FINANCIAL_STMT_DUMP_QUERY.format(table_name=FINANCIAL_STMT_TABLE_NAME))
            )
            self.df_to_db(
                df=df,
                table_name=FINANCIAL_STMT_TABLE_NAME,
                conn=connection,
            )
