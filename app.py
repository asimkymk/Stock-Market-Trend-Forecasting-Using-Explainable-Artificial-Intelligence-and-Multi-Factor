from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
import hashlib
from flask_jwt import JWT, jwt_required, current_identity
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'

#BACKEND

@app.route('/model/<string:symbol>', methods=['GET'])
def  getfeecback(symbol):
    try:
        print(symbol)
        return jsonify(symbol), 200
    except:
        return jsonify({'error': 'Database error!'}), 400

