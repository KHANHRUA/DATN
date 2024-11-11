from flask import Blueprint, jsonify, request

from http import HTTPStatus

from blueprints.gender import controller as gender_control

gender_route = Blueprint('gender', __name__, url_prefix='/api/gender')

@gender_route.route('/list', methods=['GET'])
def list():
    try:
        genders = gender_control.get_all_genders()
        content = genders
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status

