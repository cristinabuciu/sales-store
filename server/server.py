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
lastID = 4


c = Counter('my_requests', 'Number of Requests', ['method', 'endpoint'])
stock = Gauge('stock', 'Stock per item', ['id','name','provider'])
purchasesPerProvider = Counter('purchases_per_provider', 'Purhcases per provider', ['provider'])



def favorite_colors(item_id, item_name) -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    if item_id != "":
        query = "SELECT * FROM stock WHERE item_id = \'" + item_id + "\'"
    else:
        query = "SELECT * FROM stock WHERE item_name = \'" + item_name + "\'"
    cursor.execute(query)
    results = [[id,name,provider, str(stock)] for (id,name, provider, stock) in cursor]
    cursor.close()
    connection.close()

    return results

def updateDb(item_name,provider, quantity):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }

    app.logger.info("provider = " + provider)
    app.logger.info("item_name = " + item_name)
    app.logger.info("quantity = " + str(quantity))
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "SELECT * FROM stock WHERE item_name = \'" + item_name + "\' AND provider = \'" + provider + "\'"

    cursor.execute(query)
    results = [stock for (id,name, provider, stock) in cursor]

    if len(results) == 0:
        return False


    stock = results[0]

    app.logger.info("stock = " + str(stock))

    stock = stock - quantity

    app.logger.info("stock after= " + str(stock))

    query = "UPDATE stock SET stock=" + str(stock) + " WHERE item_name = \'" + item_name + "\' AND provider = \'" + provider + "\'"
    cursor.execute(query)
    connection.commit()


    cursor.close()
    connection.close()
    return True

def addStockDb(item_id, item_name, provider, quantity):
    try:
        global lastID
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'store'
        }

        # app.logger.info("provider = " + provider)
        # app.logger.info("item_name = " + item_name)
        # app.logger.info("quantity = " + str(quantity))
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        if (item_id == "") :
            query = "SELECT * FROM stock WHERE item_name = \'" + item_name + "\' AND provider = \'" + provider + "\'"
        else:
            query = "SELECT * FROM stock WHERE item_id = \'" + item_id + "\'"

        cursor.execute(query)
        results = [stock for (id,name, provider, stock) in cursor]

        update_query = ""

        if len(results) == 0:
            app.logger.info("len 0")
            lastID = lastID + 1
            update_query = "INSERT INTO stock VALUES (" + str(lastID) + "," + "\'"+item_name + "\',\'" + provider + "\'," + str(quantity) + ")"
        else:
            app.logger.info("len dif de 0")
            stock = results[0]
            stock = stock + quantity
            update_query = "UPDATE stock SET stock=" + str(stock) + " WHERE item_name = \'" + item_name + "\' AND provider = \'" + provider + "\'"

        app.logger.info("QUERY: " + update_query)
        cursor.execute(update_query)
        connection.commit()


        cursor.close()
        connection.close()
        return True
    except:
        return False

def getStockDbState(item_name, provider):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT * FROM stock WHERE item_name = \'" + item_name + "\' AND provider = \'" + provider + "\'"


    cursor.execute(query)
    results = [[id,name, provider, stock] for (id,name, provider, stock) in cursor]
    cursor.close()
    connection.close()

    return results[0]




@app.route("/")
@app.route("/home")
def home() :
    return render_template('layout.html')


@app.route("/stock", methods=["POST"])
@cross_origin()
def stock_function() -> str:
    c.labels('get', '/stock').inc()

    body = request.get_json()

    item_id = body["item_id"]
    item_name = body["item_name"]
    username = body["username"]
    token = body["token"]


    app.logger.info("item_id = " + item_id)
    app.logger.info("item_name = " + item_name)
    app.logger.info("username = " + username)
    app.logger.info("token = " + token)

    return_val = favorite_colors(item_id,item_name)
    return json.dumps(return_val)

@app.route("/sales", methods=["POST"])
@cross_origin()
def sales_function() -> str:
    c.labels('post', '/sales').inc()

    body = request.get_json()
    # c.inc()
    # item_name = request.args.get('item_name')
    # provider = request.args.get('provider')
    # quantity = int(request.args.get('quantity'))

    item_name = body["item_name"]
    provider = body["provider"]
    quantity = int(body["quantity"])
    username = body["username"]
    token = body["token"]

    result = updateDb(item_name, provider,quantity)

    if result:
        purchasesPerProvider.labels(provider).inc(quantity)
        [id, name, provider, ret_stock] = getStockDbState(item_name, provider)
        stock.labels(id, name, provider).set(ret_stock)
        return json.dumps("Update done")
    else:
        return json.dumps("Couldn't find product in stock, please check stock before")


@app.route("/add-stock", methods=["POST"])
@cross_origin()
def add_stock_fucntion() -> str:
    c.labels('post', '/add-stock').inc()

    body = request.get_json()
    # item_id = request.args.get('item_id')
    # item_name = request.args.get('item_name')
    # provider = request.args.get('provider')
    # quantity = int(request.args.get('quantity'))

    item_id = body["item_id"]
    item_name = body["item_name"]
    provider = body["provider"]
    quantity = body["quantity"]
    username = body["username"]
    token = body["token"]

    result = addStockDb(item_id, item_name, provider, quantity)

    if result:
        [id, name, provider, ret_stock] = getStockDbState(item_name, provider)
        stock.labels(id, name, provider).set(ret_stock)
        return json.dumps("Update done")
    else:
        return json.dumps("An error occurred. Please try again")



@app.route("/metrics")
def metrics():
    return generate_latest(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)