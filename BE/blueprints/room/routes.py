from flask import Blueprint, jsonify, request

from http import HTTPStatus

from blueprints.room import controller as room_control

from blueprints.session.model import SessionModel
from blueprints.user.model import UserRole

room_route = Blueprint('room', __name__, url_prefix='/api/room')

@room_route.route('/list', methods=['GET'])
def list():
    try:
        name= request.args.get('name')
        page = int(request.args.get('page', 1))
        perPage = int(request.args.get('perPage', 20))
        sessions = room_control.get_all_room_by_filter(page, perPage, name)
        content = sessions
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status