from flask import Blueprint, jsonify, request, current_app

from flask_socketio import send, emit

from flask_jwt_extended import jwt_required, get_jwt_identity

import time

from http import HTTPStatus
from blueprints.attendant import controller as attendant_control
from blueprints.session import controller as session_control
from blueprints.user import controller as user_control
from blueprints.subject import controller as subject_control
from blueprints.room import controller as room_control

from blueprints.attendant.model import AttendantModel
from blueprints.user.model import UserRole

import json

attendant_route = Blueprint('attendant', __name__, url_prefix='/api/attendant')
    
@attendant_route.route('/list', methods=['GET'])
@jwt_required()
def list():
    try:
        jwt = get_jwt_identity()
        page = int(request.args.get('page', 1))
        perPage = int(request.args.get('perPage', 20))
        attendant = []

        if( jwt.get('role') == str(UserRole.student.value)):
            attending = attendant_control.get_all_classes_by_filter(page=page,perPage=perPage,user_id=jwt.get('id'))
            for ob in attending:
                ob['session'] = session_control.get_by_id(ob['session_id'])
                ob['subject'] = subject_control.get_by_id(ob['session']['subject_id'])
                ob['teacher'] = user_control.get_user_by_id(ob['session']['user_id'])
                ob['teacher']['role'] = ob['teacher']['role'].value
                ob['user'] = user_control.get_user_by_id(ob['user_id'])
                ob['user']['role'] = ob['user']['role'].value
                attendant.append(ob)
        else:
            print('aaa')

        content = attendant
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status