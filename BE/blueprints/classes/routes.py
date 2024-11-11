from flask import Blueprint, jsonify, request

from http import HTTPStatus

from blueprints.classes import controller as class_control

class_route = Blueprint('class', __name__, url_prefix='/api/class')

@class_route.route('/list', methods=['GET'])
def list():
    try:
        page = int(request.args.get('page', 1))
        perPage = int(request.args.get('perPage', 20))
        name = request.args.get('name')
        genders = class_control.get_all_classes_by_filter(page,perPage,class_name=name)
        content = genders
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status

