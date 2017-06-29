#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "dbMongoEntrega4"
MONGOSERVER = "query17-13.ing.puc.cl"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/flaskr/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)

collection = mongodb["escuchas"]
collection.create_index([('contenido', 'text')])

@app.route("/query1", methods=['GET'])
def consulta_1():
    date = request.args.get('fecha')
    db = mongodb.escuchas
    result = json_util.dumps(escuchas.find({"fecha": date}, {"numero":1}))
    resp = Response(result)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

@app.route("/query2", methods=['GET'])
def consulta_2():
    num = request.args.get('num')
    k = request.args.get('k')
    db = mongodb.escuchas
    result = json_util.dumps(escuchas.find({"numero": num} ,{"contenido": 1}).limit(k))
    resp = Response(result)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return(resp)

@app.route("/query3", methods=['GET'])
def consulta_3():
    alias = request.args.get('alias')
    db = mongodb.escuchas
    result = json_util.dumps(escuchas.find({'$text': {'$search': alias}},{'numero':1, 'fecha':1, 'ciudad':1 , 'contenido':1}))
    resp = Response(result)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp


@app.route("/mongo", methods=['POST'])
def mongo():
    # query = request.args.get("query")
    num = request.form.get("num")
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
    query = json_file[int(num) - 1]["query"]

    if num == "1":
        print(num)
        date = request.form.get("date")
        print(date)
        print(request.form)
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return "Error, formato de fecha invalido."
        query = query.replace("val", date)

    elif num == "2":
        number = request.form.get("number")
        k = request.form.get("k")
        if k.isdecimal() and k != "0" and number.isdecimal():
            query = query.replace("number", number).replace("k", k)
        else:
            return "Ambos k y num deben ser enteros, y k debe ser mayor a 0."
    
    elif num == "3":
        word = request.form.get("word")
        query = query.replace("palabra", word)
    print(query)
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"


# @app.route("/postgres")
# def postgres():
#     query = request.args.get("query")
#     cursor = postgresdb.cursor()
#     cursor.execute(query)
#     results = [[a for a in result] for result in cursor]
#     print(results)
#     return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
