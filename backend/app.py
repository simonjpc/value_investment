from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from valuation.constants import (
    POTENTIAL_NCAV_CANDIDATES_TABLE_NAME,
    POTENTIAL_PFV_CANDIDATES_TABLE_NAME,
)

app = Flask(__name__)
CORS(app)

from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def get_data_from_db(query):
    conn = psycopg2.connect(
        dbname="",
        user="",
        password="",
        host="",
        port="",
    )
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    data = {col: [] for col in columns}
    for row in rows:
        for col, value in zip(columns, row):
            data[col].append(value)

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
