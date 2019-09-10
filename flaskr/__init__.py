# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')
socketio = SocketIO(app)


from flaskr import views


