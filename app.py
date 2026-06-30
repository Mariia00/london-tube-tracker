import os
from dotenv import load_dotenv
from flask import send_from_directory
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from stations import  get_route
from flask import Flask, render_template



load_dotenv()

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)

@app.route('/')
def serve_index():
    return render_template('index.html', maptiler_api_key=os.getenv("MAPTILER_API_KEY"))
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/routes')
def serve_routes():
    return jsonify(get_route("victoria"))

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Hello, World!'})