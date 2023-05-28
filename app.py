from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
from multiprocessing import Process
from waitress import serve
import os
import signal
from model.webService_model import run_dashboard
CORS(app) #comment this on deployment
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'


def stop_server(port):
    import requests
    try:
        requests.get(f'http://localhost:{port}/shutdown')
        print('Server shutting down...')
    except Exception as e:
        print('Could not shut down the server: ', e)

@app.route('/shutdown', methods=['GET'])
def shutdown():
    try:
         
        stop_server(8050)
        message = {
                "message":"Success",
                "data":"Sutted down."
                }
        return jsonify(message), 200
    except:
        return jsonify({"message":"Error",'data': 'API Service error occured!'}), 400

@app.route('/model/<string:symbol>/<string:news_model>/<string:useTrend>/<string:modelName>/<string:delay>', methods=['GET'])
def  getfeecback(symbol,news_model,useTrend,modelName,delay):
    try:

        useTrend_bool = useTrend.lower() == 'true'
        stop_server(8050)
        p = Process(target=run_dashboard, args=(8050,symbol,news_model,useTrend_bool,modelName,int(delay)))
        p.start()
        message = {
                "message":"Success",
                "data":"Model started."
                }
        return jsonify(message), 200
    except:
        return jsonify({"message":"Error",'data': 'API Service error occured!'}), 400

