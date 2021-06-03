from flask import Flask, request
import digital_sig
from datetime import datetime
import pipeline
import global_config
from time import sleep
import hashlib
from pprint import pprint
import database as db

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global_counter = 1


@app.route('/api/validar', methods=["POST", "GET"])
def validar():
    global global_counter

    global_config.DEBUG = False

    data = request.json
    num_cuenta = data["num_cuenta"]
    password_hash = data["hash"]
    photo_uri = data["base64_encoded_photo"]

    img = pipeline.img_from_uri(photo_uri)
    recognized_name = pipeline.recognize(img)

    print("Detectado:{}\n".format(recognized_name))

    valid_entry = db.valid_credentials(
        recognized_name, password_hash, num_cuenta)

    nombres = ""
    primer_apellido = ""
    segundo_apellido = ""

    my_hash = None

    if valid_entry:
        (nombres, primer_apellido, segundo_apellido) = db.get_first_name_if_exists(
            recognized_name)
        my_hash = digital_sig.get_unique_signature(
            nombres, primer_apellido, segundo_apellido)

    return {"valid": valid_entry, "key": my_hash, "nombres": nombres, "primer_apellido": primer_apellido, "segundo_apellido": segundo_apellido}


@app.route('/api/send_photo', methods=["POST"])
def get_photo():
    photo = request.files["photo"]


if __name__ == "__main__":
    app.run()
