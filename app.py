from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from flask_jwt import JWT, jwt_required, current_identity
from model.xgboost_explainerdashboardmodel import openPort
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
from multiprocessing import Process
from waitress import serve
import os
import signal
from model.xgboost_web import run_dashboard
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
     stop_server(8050)

@app.route('/model/<string:symbol>', methods=['GET'])
def  getfeecback(symbol):
    stop_server(8050)
    p = Process(target=run_dashboard, args=(8050,symbol))
    p.start()
    return True

