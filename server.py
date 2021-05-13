from flask import Flask, request
from time import sleep

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
    with open("resources/test_uri","w") as f:
        f.write(photo_uri)
    sleep(3)

    return {"valid":True, "key": "unsha"}

@app.route('/api/send_photo', methods=["POST"])
def get_photo():
    photo = request.files["photo"]
