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

from datetime import datetime

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
    results = [[user_id, username, _, _] for (user_id, username, _, _) in cursor]
    cursor.close()
    connection.close()
    return json.dumps(results)

@app.route("/get-orders-report", methods=["GET"])
@cross_origin()
def get_orders_report() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = f"SELECT o.order_id, s.item_name, u.username, o.quantity, o.order_timestamp, p.price " \
            f"FROM orders o, stock s, users u, price p " \
            f"WHERE o.item_id=s.item_id AND o.user_id=u.user_id AND o.item_id=p.item_id"
    # query = "SELECT * FROM orders"
    app.logger.info("QUERY: " + query)
    cursor.execute(query)
    results = [[order_id, item_id, user_id, quantity, (price * quantity),str(datetime.fromtimestamp(oder_timestamp))] for (order_id, item_id, user_id, quantity, oder_timestamp, price) in cursor]
    cursor.close()
    connection.close()
    return json.dumps(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
