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
     stop_server(8050)

@app.route('/model/<string:symbol>/<string:news_model>/<string:useOpen>/<string:modelName>', methods=['GET'])
def  getfeecback(symbol,news_model,useOpen,modelName):
    try:

        useOpen_bool = useOpen.lower() == 'true'
        stop_server(8050)
        p = Process(target=run_dashboard, args=(8050,symbol,news_model,useOpen_bool,modelName))
        p.start()
        message = {
                "message":"Success",
                "data":"Model started."
                }
        return jsonify(message), 200
    except:
        return jsonify({"message":"Error",'data': 'API Service error occured!'}), 400

