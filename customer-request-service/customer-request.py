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

@app.route("/get-messages", methods=["GET"])
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
    query = "SELECT * FROM messages"
    cursor.execute(query)
    results = [[date.strftime("%m/%d/%Y"), name, email, phone_number, message] for (date, name, email, phone_number, message) in cursor]
    cursor.close()
    connection.close()
    return json.dumps(results)

@app.route("/post-message", methods=["POST"])
@cross_origin()
def post_message() -> str:
    body = request.get_json()
    name = ''
    email = ''
    phone_number = ''
    message = ''
    if "name" in body:
        name = body['name']
    if "email" in body:
        email = body['email']
    if "phone_number" in body:
        phone_number = body['phone_number']
    if "message" in body:
        message = body['message']
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    update_query = "INSERT INTO messages VALUES (" +  "\'" + time.strftime('%Y-%m-%d %H:%M:%S') + "\'" + "," + "\'" + name + "\'" + "," + "\'"+email + "\',\'" + phone_number + "\'," + "\'" + message + "\'" + ")"
    app.logger.info("QUERY: " + update_query)
    # cursor.execute("INSERT INTO messages (date, name, email, phone_number, message) VALUES ('%s',%s, %s, %s)")
    cursor.execute(update_query)
    connection.commit()

    cursor.close()
    connection.close()
    return json.dumps("OK")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)