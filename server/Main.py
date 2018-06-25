from flask import Flask, jsonify
from flask import abort
from flask import request
from flask import Response
from flask import send_from_directory
from flask_cors import CORS
from Align import Align
from OpencvAlign import OpencvAlign
import logging
import json
import urllib3
import base64
import sys
import time
import codecs, json 
import pandas as pd
sys.path.insert(0, './train')
sys.path.insert(0, './model')
from Train import ChangeStyle


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)
cors = CORS(app,supports_credentials=True)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
changeStyle = ChangeStyle()

@app.route('/uploadToAnime', methods=['PUT'])
def becomeAnimeStyle():
    data = request.form
    img = data['file'].split(",")[1]
    img = base64.decodebytes(bytes(img, 'utf-8'))
    with open("imageToSave.png", "wb") as fh:
        fh.write(img)
    changeStyle.changeToAnime("imageToSave.png")

    with open("outfileAnime.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return Response(json.dumps(str(encoded_string)), mimetype='application/json')

@app.route('/realTime', methods=['PUT'])
def realTimeBecomeAnimeStyle():
    data = request.form
    img = data['file']
    img = base64.decodebytes(bytes(img, 'utf-8'))
    with open("cameraToSave.png", "wb") as fh:
        fh.write(img)

    #align = Align()
    #align.align('cameraToSave.png')
    align = OpencvAlign('cameraToSave.png')
    align.Cut()

    changeStyle.changeToAnime("./out/cameraToSave.png")

    with open("outfileCamera.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return Response(json.dumps(str(encoded_string)), mimetype='application/json')


@app.route('/uploadToReal', methods=['PUT'])
def becomeRealStyle():
    data = request.form
    img = data['file'].split(",")[1]
    img = base64.decodebytes(bytes(img, 'utf-8'))
    with open("imageToSave.png", "wb") as fh:
        fh.write(img)
    changeStyle.chamgeToReal("imageToSave.png")

    with open("outfileReal.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return Response(json.dumps(str(encoded_string)), mimetype='application/json')

@app.route('/outfileAnime.jpg', methods=['GET'])
def SendAnimeFile():
    return send_from_directory(app.root_path, "outfileAnime.jpg", as_attachment=True)

@app.route('/outfileReal.jpg', methods=['GET'])
def SendRealFile():
    return send_from_directory(app.root_path, "outfileReal.jpg", as_attachment=True)

@app.route('/outfileCamera.jpg', methods=['GET'])
def SendCameraFile():
    return send_from_directory(app.root_path, "outfileCamera.jpg", as_attachment=True)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port = 3000, use_reloader=False)

