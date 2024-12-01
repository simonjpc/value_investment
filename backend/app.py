import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from valuation.constants import (
    POTENTIAL_NCAV_CANDIDATES_TABLE_NAME,
    POTENTIAL_PFV_CANDIDATES_TABLE_NAME,
)
from valuation.data_injection import Injector
from valuation.utils import display_verification
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

app = Flask(__name__)
CORS(app)

injector = Injector()
engine = create_engine(
    injector.db_uri, poolclass=QueuePool, pool_size=10, max_overflow=20
)


def get_data_from_db(query):
    # conn = psycopg2.connect(
    #     dbname="",
    #     user="",
    #     password="",
    #     host="",
    #     port="",
    # )
    # cursor = conn.cursor()
    # cursor.execute(query)
    # rows = cursor.fetchall()
    # columns = [desc[0] for desc in cursor.description]
    # conn.close()

    # data = {col: [] for col in columns}
    # for row in rows:
    #     for col, value in zip(columns, row):
    #         data[col].append(value)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    data = df.to_dict("list")

    for key in data:
        data[key] = list(map(lambda x: display_verification(x), data[key]))
    return data


def transform_data(data):
    keys = data.keys()
    transformed_data = []

    for i in range(len(next(iter(data.values())))):
        row = {key: (data[key][i] if data[key][i] is not None else "") for key in keys}
        transformed_data.append(row)

    return transformed_data


@app.route("/api/ncav", methods=["GET"])
def get_ncav_data():
    query = f"SELECT * FROM {POTENTIAL_NCAV_CANDIDATES_TABLE_NAME}"
    data = get_data_from_db(query)
    transformed_data = transform_data(data)
    print(transformed_data)
    return jsonify(transformed_data)


@app.route("/api/epsx", methods=["GET"])
def get_epsx_data():
    query = f"SELECT * FROM {POTENTIAL_PFV_CANDIDATES_TABLE_NAME}"
    data = get_data_from_db(query)
    transformed_data = transform_data(data)
    print(transformed_data)
    return jsonify(transformed_data)


if __name__ == "__main__":
    app.run(debug=True)
