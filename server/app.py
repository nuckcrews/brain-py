import os
from dotenv import load_dotenv
import openai
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

load_dotenv()

from .error import AppError, missing_param
from src import Brain

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET_KEY").encode("utf8")

CORS(app, support_credentials=True)

socketio = SocketIO(app, cors_allowed_origins="*")

brain = Brain()

@app.route("/")
def welcome():
    return "Access to your Brain", 200


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.errorhandler(AppError)
def handle_bulsai_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    emit("error", response)

@socketio.on('connect')
def connect(params: any):
    openai_key = params.get("openai_key")
    if not openai_key:
        raise missing_param("openai_key is required")

    brain.setup(openai_key)
    print("connected")


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')