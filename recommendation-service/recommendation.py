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
import datetime
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

@app.route("/get-recommendation", methods=["POST"])
@cross_origin()
def get_recommendation() -> List[Dict]:

    body = request.get_json()
    username = body['username']

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    # get user id
    query = "SELECT user_id FROM users WHERE username =\'" + username + "\'"
    cursor.execute(query)
    user = cursor.fetchone()[0]
    
    # get all orders
    query = "SELECT * FROM orders"
    cursor.execute(query)
    orders = [[item_id, user_id, quantity] for (_, item_id, user_id, quantity, _) in cursor]
    
    orders.sort(key = lambda x : x[1])
    sorted_orders = orders[-5 : ]
    
    results = []
    for sorted_order in sorted_orders:
        item_id = sorted_order[0]
        query = "SELECT item_name, provider FROM stock WHERE item_id =\'" + str(item_id) + "\'"
        cursor.execute(query)
        name_and_provider = cursor.fetchone()
        query = "SELECT price FROM price WHERE item_id =\'" + str(item_id) + "\'"
        cursor.execute(query)
        price = cursor.fetchone()[0]
        results.append([name_and_provider[0], name_and_provider[1], price])

    cursor.close()
    connection.close()
    app.logger.info(results)
    return json.dumps(results)

@app.route("/get-custom-recommendation", methods=["POST"])
@cross_origin()
def get_custom_recommendation() -> str:
    body = request.get_json()

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    body = request.get_json()
    provider = body['provider']

    min_val = int(body["min_val"])
    max_val = int(body["max_val"])
    
    query = "SELECT item_id, item_name, provider FROM stock"
    cursor.execute(query)
    stocks = [[item_id, item_name, provider] for (item_id, item_name, provider) in cursor]
    if provider != 'Choose...':
        stocks = [stock for stock in stocks if stock[2] == provider]

    results = []

    for stock in stocks:
        item_id = stock[0]
        item_name = stock[1]
        provider = stock[2]
        query = "SELECT price FROM price WHERE item_id =\'" + str(item_id) + "\'"
        cursor.execute(query)
        price = cursor.fetchone()[0]
        if (price >= min_val and price <= max_val) :
            results.append([item_name, provider, price])

    cursor.close()
    connection.close()
    app.logger.info(results)
    return json.dumps(results)

@app.route("/get-providers", methods=["GET"])
@cross_origin()
def get_providers() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT provider FROM stock"
    cursor.execute(query)
    results = []
    for provider in cursor:
        results.append(provider)
    cursor.close()
    connection.close()
    return json.dumps(list( dict.fromkeys(results)))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)