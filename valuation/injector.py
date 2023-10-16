import psycopg2
from valuation.data_injection import Injector
from valuation.utils import dict_to_df
from typing import Dict, Any

def df_dump(fa_info: Dict[str, Any], table_name: str) -> None:
    injector = Injector()
    fa_info_df = dict_to_df(fa_info)
    db_params = injector.get_dbparams()
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            # Create the table if it doesn't exist
            # cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (column1 datatype, column2 datatype)")

            # Insert data from the Pandas DataFrame
            # df.to_sql(table_name, con=conn, if_exists="replace", index=False)
            injector.df_to_db(fa_info_df, table_name, conn)
