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
aws_access_key_id=''
aws_secret_access_key=''
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
        hash_value = str(hex(hash(img.tobytes())))
        response = inference_handler.predict(img)
        storage.temp_store(hash_value, img)
        
        return jsonify(result=response, hash_value=hash_value)

    return None

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        hash_value = request.json['hash_value']
        correct_label = request.json['label']
        if(correct_label != "ok"):
            storage.copy_file(correct_label, hash_value)
        #print("Label is "+correct_label+" Hash is "+hash_value) 
        #print("Received feedback") 
        storage.remove_file(hash_value)
        resp = jsonify(success=True)
        return resp

    return None



if __name__ == '__main__':

    http_server = WSGIServer(('0.0.0.0', TCP_PORT), app)
    http_server.serve_forever()
