from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import request
from app.app import socketio
import json
    
@socketio.on('attendant')
def attendant():
    print('hello')

@socketio.on('login')
def on_login(data):
    class_id = data['class_id']
    print('join')
    join_room(class_id)

@socketio.on('logout')
def on_logout(data):
    class_id = data['class_id']
    print('leave')
    leave_room(class_id)

@socketio.on('check-in')
def handle_checkin():
    print('a')
    emit('attendant', {'data': "hello"}, room=2, broadcast=True)