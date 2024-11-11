from flask_socketio import send, emit, join_room, SocketIO ,leave_room
from flask import request
from app.app import app

socketio = SocketIO(app, cors_allowed_origins='*')