import sqlite3
import hashlib
import sys
from sqlite3 import Error, Connection, Cursor
import global_config
import base64
import hmac
import pandas as pd


def init_db(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        create_user_table(conn)

    except Error as e:
        print(e, file=sys.stderr)

    finally:
        if conn:
            conn.close()


def sha256_base64(string):
    _bytes = bytes(string, 'utf-8')
    hash = hashlib.sha256(_bytes).hexdigest()
    return str(hash)


def create_user_table(conn: Connection):

    conn.execute('''CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        num_cuenta TEXT NOT NULL,
        nombres TEXT NOT NULL,
        primer_apellido TEXT NOT NULL,
        segundo_apellido TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        etiqueta TEXT NOT NULL
    );''')

    conn.close()


def list_all_users():
    conn = sqlite3.connect(global_config.DATABASE)

    result = pd.read_sql_query(
        "SELECT user_id,num_cuenta, nombres,primer_apellido,segundo_apellido,etiqueta from users", conn)

    print(result)


def insert_user(values: dict):
    conn = sqlite3.connect(global_config.DATABASE)

    values_tuple = (values["num_cuenta"], values["nombres"], values["primer_apellido"],
                    values["segundo_apellido"], values["password_hash"], values["etiqueta"])
    with conn:
        conn.execute(
            "INSERT INTO users (num_cuenta, nombres, primer_apellido, segundo_apellido,password_hash, etiqueta)VALUES (?,?,?,?,?,?)", values_tuple)


def get_name_if_exists(num_cuenta, password_hash):
    conn = sqlite3.connect(global_config.DATABASE)

    cur = conn.cursor()

    cur.execute(
        "SELECT (etiqueta) FROM users WHERE num_cuenta=? AND password_hash=?", (num_cuenta, password_hash))

    row = cur.fetchone()

    if row:
        return row[0]
    else:
        return None


def valid_credentials(recognized_name, password_hash, num_cuenta):

    retrieved_name = get_name_if_exists(num_cuenta, password_hash)

    if retrieved_name:
        return retrieved_name == recognized_name
    else:
        return False
