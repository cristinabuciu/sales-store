from flask import Flask, render_template, url_for, flash, redirect, request
import mysql.connector
import json
import logging
import random
import string
import hashlib


from flask_cors import CORS, cross_origin

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
connections = {}
current_user_id = 2

@app.route("/logout", methods=["POST"])
@cross_origin()
def removeToken() -> str:
    body = request.get_json()
    username = body['username']

    if username in connections.keys():
        del connections[username]

    return json.dumps("Token removed")


@app.route("/verify-token", methods=["POST"])
@cross_origin()
def verifyToken() -> str:
    body = request.get_json()
    username = body['username']
    token = body['token']

    if username not in connections.keys():
        return json.dumps("access-denied")
    elif connections[username] == token:
        return json.dumps("access-granted")
    else:
        return json.dumps("access-denied")


@app.route("/login", methods=["POST"])
@cross_origin()
def generateToken() -> str:

    permision = False
    body = request.get_json()

    username = body['username']
    password = body['password']
    scope = ''
    hashedPassword = hashlib.md5(password.encode()).hexdigest()

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "SELECT password_hash, scope FROM users WHERE username=\'" + username + "\'"

    cursor.execute(query)
    results = [passs for (passs) in cursor]

    if len(results) == 0:
        permision = False
    else:
        dbPassword = results[0][0]
        scope = results[0][1]
        app.logger.info("db: " + str(dbPassword))
        app.logger.info("pass: " + hashedPassword)
        app.logger.info("scope: " + scope)

        if dbPassword == hashedPassword:
            permision = True
        else:
            permision = False
    cursor.close()
    connection.close()

    if permision:
        letters = string.ascii_lowercase
        token = ''.join(random.choice(letters) for i in range(30))
        connections[username] = token
        vals = {"token" : token, "scope" : scope}
        return json.dumps(vals)
    else:
        return json.dumps("Permission denied")

@app.route("/register", methods=["POST"])
@cross_origin()
def register() -> str:

    try:
        permision = False
        body = request.get_json()
        username = body['username']
        password = body['password']

        hashedPassword = hashlib.md5(password.encode()).hexdigest()
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'store'
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        global current_user_id
        current_user_id = current_user_id + 1
        scope = 'user'
        query = "INSERT INTO users VALUES (" + str(current_user_id) + "," + "\'"+username + "\',\'" + hashedPassword + "\',\'" + scope + "\'" + ")"
        app.logger.info("REGISTER: " + query);

        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        app.logger.info("Successful register")
        return json.dumps("Success")
    except:
        app.logger.info("Failed register")
        return json.dumps("Permission denied")


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)