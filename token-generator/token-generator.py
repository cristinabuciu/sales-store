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

@app.route("/remove-token", methods=["POST"])
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


@app.route("/token", methods=["POST"])
@cross_origin()
def generateToken() -> str:

    permision = False
    body = request.get_json()

    username = body['username']
    password = body['password']
    hashedPassword = hashlib.md5(password.encode()).hexdigest()
    scope = ''

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'store'
    }
    connection = mysql.connector.connect(**config)
    app.logger.info(connection.is_connected())
    cursor = connection.cursor()
    query = "SELECT password_hash, scope FROM users WHERE username=\'" + username + "\'"

    cursor.execute(query)
    results = [passs for (passs) in cursor]

    if len(results) == 0:
        app.logger.info("intra1")
        permision = False
    else:
        app.logger.info("intra2")
        dbPassword = results[0][0]
        scope = results[0][1]
        app.logger.info("db: " + str(dbPassword))
        app.logger.info("pass: " + hashedPassword)
        app.logger.info("scope: " + scope)

        if dbPassword == hashedPassword:
            app.logger.info("intra3")
            permision = True
        else:
            app.logger.info("intra4")
            permision = False
    cursor.close()
    connection.close()

    if permision:
        app.logger.info("intra5")
        letters = string.ascii_lowercase
        token = ''.join(random.choice(letters) for i in range(30))
        connections[username] = token
        vals = {"token" : token, "scope" : scope}
        return json.dumps(vals);#{"token": token, "scope" : scope})
    else:
        app.logger.info("intra6")
        return json.dumps("Permission denied")




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)