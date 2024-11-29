from sqlalchemy import create_engine, text
from valuation.data_injection import Injector
from valuation.constants import TABLES_TO_DROP
from celery_app import app

injector = Injector()


@app.task()
def drop_tables():
    engine = create_engine(injector.db_uri)
    for table_name in TABLES_TO_DROP:
        query = f"DROP TABLE {table_name};"
        try:
            with engine.connect() as connection:
                connection.execute(text(query))
                connection.commit()
        except Exception as e:
            print(f"An error occurred while dropping table {table_name}: {e}")
        continue
    connection.close()
    engine.dispose()
    print("all tables dropped")


if __name__ == "__main__":
    drop_tables()
