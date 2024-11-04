from sqlalchemy import create_engine, text
from valuation.data_injection import Injector
from valuation.constants import TERMINATE_ALL_CONNECTIONS_QUERY

injector = Injector()


def terminate_all_connections() -> None:
    engine = create_engine(injector.db_uri)
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        op = connection.execute(text(TERMINATE_ALL_CONNECTIONS_QUERY))


if __name__ == "__main__":
    terminate_all_connections()
