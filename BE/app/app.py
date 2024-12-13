import flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from flask import Flask, jsonify, request
from blueprints.account.routes import auth_route
from blueprints.gender.routes import gender_route
from blueprints.user.routes import user_route
from blueprints.classes.routes import class_route
from blueprints.notification.routes import notification_route
from blueprints.session.routes import session_route
from blueprints.attendant.routes import attendant_route
from blueprints.subject.routes import subject_route
from blueprints.room.routes import room_route
from app.db import db
import time

from http import HTTPStatus
from blueprints.attendant import controller as attendant_control
from blueprints.attendant.model import AttendantModel
from blueprints.session import controller as session_control
from blueprints.user import controller as user_control
from blueprints.room import controller as room_control


from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__, instance_relative_config=True, static_folder='./dist/static',
            template_folder='./dist')

app = Flask(__name__)

# Cấu hình kết nối MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/datn'

app.config['SECRET_KEY'] = "khanh"
app.config["JWT_SECRET_KEY"] = "khanhrua"

CORS(app, resource={r"/*": {"origins": "*"}}, allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "cache-control", "Pragma", "Expires", "Access-Control-Allow-Credentials"], supports_credentials=True)

app.register_blueprint(auth_route)
app.register_blueprint(gender_route)
app.register_blueprint(user_route)
app.register_blueprint(class_route)
app.register_blueprint(notification_route)
app.register_blueprint(session_route)
app.register_blueprint(subject_route)
app.register_blueprint(attendant_route)
app.register_blueprint(room_route)
jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/api/check-in', methods=['POST'])
def attendant():
    try:
        data = request.get_json()
        user_id = data['user_id']
        room = data['room']
        room = room_control.get_record_by_name(room)
        session = session_control.get_current_session(room['id'], int(time.time()))
        if(session is False): 
            raise ValueError('Not session in time')
        user = user_control.get_user_by_id(user_id)
        if(user['class_id'] != session['class_id']):
            raise ValueError('You not in this session')
        type_check = data['type_check']
        newAttendant = AttendantModel(user_id=user_id,room_id=room['id'],session_id=session['id'],type_check=type_check)
        newAttendant.save_to_db()
        user['role'] = user['role'].value
        dataSocket = {
            'session': session,
            "user": user,
            "room": room,
            'typeCheck': type_check
        }
        socketio.emit('attendant', {'data': dataSocket})
        content = data
        status = HTTPStatus.OK
        return jsonify(content), status
    except ValueError as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.FORBIDDEN
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status



