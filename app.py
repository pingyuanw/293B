import os
import sys

import inference
import storage

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


# Some utilites
import numpy as np
from util import base64_to_pil

TCP_PORT = 5000
aws_access_key_id='Secret'
aws_secret_access_key='Secret'
# Declare a flask app
app = Flask(__name__)


inference_handler = inference.Inference(aws_access_key_id, aws_secret_access_key)
print('Model loaded. Check http://127.0.0.1:'+str(TCP_PORT))




@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        img = base64_to_pil(request.json)

        response = inference_handler.predict(img)
        storage.store(response, img)
        
        return jsonify(result=response)

    return None


if __name__ == '__main__':

    http_server = WSGIServer(('0.0.0.0', TCP_PORT), app)
    http_server.serve_forever()
