from flask import Flask, request
from w3lib.url import parse_data_uri
import base64

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global_counter = 1

@app.route('/api/validar', methods=["POST","GET"])
def validar():
    global global_counter

    data = request.json
    num_cuenta = data["num_cuenta"]
    password_hash = data["hash"]
    photo_uri = data["base64_encoded_photo"]
    parsed_uri = parse_data_uri(photo_uri)
    with open("/tmp/photo.png","wb") as f:
        f.write(parsed_uri[2])
    return "ano"

@app.route('/api/send_photo', methods=["POST"])
def get_photo():
    photo = request.files["photo"]
