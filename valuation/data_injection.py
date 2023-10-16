import pandas as pd
import psycopg2
import os
from typing import Dict

class Injector:
    def __init__(self):
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PWD")
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")
        self.db = os.environ.get("DB_NAME")

    def get_dbparams(self,) -> Dict[str, str]:
        pass

    def df_to_db(
        self,
        df: pd.DataFrame,
        table: str,
        conn: psycopg2.connection,
    ) -> None:
        pass

            
