from flask import Blueprint, jsonify, request

from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus

import datetime

from blueprints.notification import controller as notification_control
from blueprints.notification.model import NotificationModel
from blueprints.user.model import UserRole
from blueprints.user import controller as user_control

notification_route = Blueprint('notification', __name__, url_prefix='/api/notification')

@notification_route.route('/list', methods=['GET'])
@jwt_required()
def list():
    try:
        jwt = get_jwt_identity()
        page = int(request.args.get('page', 1))
        perPage = int(request.args.get('perPage', 20))
        notifications = []

        if( jwt.get('role') != str(UserRole.admin.value)):
            id = request.args.get('id')
            user = user_control.get_user_by_id(id)
            myNotifications = notification_control.get_all_notification_by_filter(page,perPage,user_id=id,class_id=None)
            myClassNotifications = notification_control.get_all_notification_by_filter(page,perPage,user_id=None,class_id=user.class_id)
            notifications.extend(myNotifications)
            notifications.extend(myClassNotifications)
        
        else:
            id = request.args.get('id')
            class_id = request.args.get('class_id')
            adminNotifications = notification_control.get_all_notification_by_filter(page,perPage,admin = 1,user_id=id,class_id=class_id)
            notifications.extend(adminNotifications)

        content = notifications
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status
    
@notification_route.route('/create', methods=['PUT'])
@jwt_required()
def create():
    try:
        jwt = get_jwt_identity()
        if( jwt.get('role') == str(UserRole.student.value)):
            raise ValueError("You have no permission")
        data = request.get_json()
        message = data['message']
        class_id = data.get('class', None)
        user_id = data.get('user', None)
        newNotification = NotificationModel(
            message=message,
            user_id=user_id,
            class_id=class_id,
        )
        newNotification.save_to_db()
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


