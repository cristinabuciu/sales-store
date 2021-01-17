from typing import List, Dict
# from flask import Flask
from flask import Flask, render_template, url_for, flash, redirect, request
import mysql.connector
import json
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import start_http_server, Summary, Counter, make_wsgi_app, generate_latest, Gauge
import random
import time
import logging
from multiprocessing.pool import ThreadPool


from flask_cors import CORS, cross_origin

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@app.route("/home")
def home() :
    return render_template('layout.html')

@app.route("/get-stock-report", methods=["GET"])
@cross_origin()
def get_stock_report() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT * FROM stock"
    cursor.execute(query)
    results = [[id,name,provider, str(stock)] for (id,name, provider, stock) in cursor]
    cursor.close()
    connection.close()
    return json.dumps(results)

@app.route("/get-users-report", methods=["GET"])
@cross_origin()
def get_users_report() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    results = [[user_id, username] for (user_id, username, password_hash) in cursor]
    cursor.close()
    connection.close()
    return json.dumps(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
