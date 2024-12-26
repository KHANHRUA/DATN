from flask import Blueprint, jsonify, request

from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus

from blueprints.session import controller as session_control
from blueprints.classes import controller as class_control
from blueprints.subject import controller as subject_control
from blueprints.session.model import SessionModel
from blueprints.user.model import UserRole

session_route = Blueprint('session', __name__, url_prefix='/api/session')

@session_route.route('/list', methods=['GET'])
def list():
    try:
        class_id = request.args.get('class_id')
        date_from = request.args.get('date_from')
        date_to= request.args.get('date_to')
        sessions = session_control.get_all_sessions_by_filter(class_id, date_from, date_to)
        for session in sessions:
            class_object = class_control.get_by_id(session['class_id'])
            session["class"] = class_object
            subject_object = subject_control.get_by_id(session['subject_id'])
            session['subject'] = subject_object
        content = sessions
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status
    
@session_route.route('/create', methods=['PUT'])
@jwt_required()
def create():
    try:
        jwt = get_jwt_identity()
        if( jwt.get('role') == str(UserRole.student.value)):
            raise ValueError("You have no permission")
        data = request.get_json()
        class_id = data.get('class_id', None)
        subject_id = data.get('subject_id', None)
        class_period = data.get('class_period', None)
        room_id = data.get('room_id', None)
        user_id = data.get('user_id', None)
        date_from = data.get('date_from')
        newSession = SessionModel(
            class_id=class_id,
            start_at=date_from,
            end_at=date_from + (2 * 60 * 60 * 1000),
            subject_id=subject_id,
            user_id=user_id,
            class_period=class_period,
            room_id=room_id
        )
        newSession.save_to_db()
        content = {
            'message' : 'Send notification successful!'
        }
        status = HTTPStatus.OK
        return jsonify(content), status
    
    except ValueError as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.UNAUTHORIZED
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status

@session_route.route('/create-multiple', methods=['PUT'])
@jwt_required()
def createMultiple():
    try:
        jwt = get_jwt_identity()
        if( jwt.get('role') == str(UserRole.student.value)):
            raise ValueError("You have no permission")
        data = request.get_json()
        class_id = data.get('class_id', None)
        subject_id = data.get('subject_id', None)
        class_period = data.get('class_period', None)
        date_from = data.get('date_from')
        week = data.get('week')
        for i in range(week):
            newSession = SessionModel(
                class_id=class_id,
                start_at=int(date_from) + (i * 1000 * 60 * 60 * 24 * 7),
                end_at=int(date_from) + (2 * 60 * 60 * 1000) + (i * 1000 * 60 * 60 * 24 * 7),
                subject_id=subject_id,
                user_id=jwt.get('id'),
                class_period=class_period
            )
            newSession.save_to_db()
        content = {
            'message' : 'Send notification successful!'
        }
        status = HTTPStatus.OK
        return jsonify(content), status
    
    except ValueError as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.UNAUTHORIZED
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status
