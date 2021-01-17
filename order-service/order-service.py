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
lastID = 0


c = Counter('my_requests', 'Number of Requests', ['method', 'endpoint'])
stock = Gauge('stock', 'Stock per item', ['id','name','provider'])
purchasesPerProvider = Counter('purchases_per_provider', 'Purhcases per provider', ['provider'])


def updateDb(item_name, quantity):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "SELECT * FROM stock WHERE item_name = \'" + item_name + "\'"

    cursor.execute(query)
    results = [stock for (id,name, provider, stock) in cursor]

    if len(results) == 0:
        return False


    stock = results[0]
    stock = stock - quantity

    query = "UPDATE stock SET stock=" + str(stock) + " WHERE item_name = \'" + item_name + "\'"
    cursor.execute(query)
    connection.commit()


    cursor.close()
    connection.close()
    return True

def getStockDbState(item_name):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT * FROM stock WHERE item_name = \'" + item_name + "\'"


    cursor.execute(query)
    results = [[id,name, provider, stock] for (id,name, provider, stock) in cursor]
    cursor.close()
    connection.close()

    return results[0]

def updateOrdersDb(item_id, username, quantity):

    # get user-id
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT user_id FROM users WHERE username = \'" + username + "\'"

    cursor.execute(query)
    user_id_result = [user_id for (user_id) in cursor]
    cursor.close()
    connection.close()

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    global lastID
    lastID = lastID + 1

    ts = int(time.time())

    query = "INSERT INTO orders VALUES (" + str(lastID) + "," + str(item_id) + "," + str(user_id_result[0][0]) + "," + str(quantity) + "," + str(ts) + ")"
    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def get_price(id):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT price FROM price WHERE item_id = " + str(id)

    cursor.execute(query)
    results = [price for (price) in cursor]
    cursor.close()
    connection.close()

    return results[0]


@app.route("/")
@app.route("/home")
def home() :
    return render_template('layout.html')

@app.route("/add-order", methods=["POST"])
@cross_origin()
def sales_function() -> str:
    c.labels('post', '/add-order').inc()

    body = request.get_json()

    item_name = body["item_name"]
    quantity = int(body["quantity"])
    username = body["username"]
    token = body["token"]

    result = updateDb(item_name,quantity)

    if result:
        [id, name, provider, ret_stock] = getStockDbState(item_name)
        stock.labels(id, name, provider).set(ret_stock)
        price = get_price(id)
        value = price[0] * quantity

        updateOrdersDb(id, username, quantity)

        return json.dumps("Order registered. Your order total value is " + str(value) + " RON")
    else:
        return json.dumps("Couldn't find product in stock, please check stock before")

@app.route("/get-existing-items", methods=["GET"])
@cross_origin()
def get_existing_items() -> str:
    c.labels('post', '/get-existing-items').inc()

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT item_name FROM stock"
    cursor.execute(query)
    results = [name for (name) in cursor]
    cursor.close()
    connection.close()
    return json.dumps(results)


@app.route("/metrics")
def metrics():
    return generate_latest(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)