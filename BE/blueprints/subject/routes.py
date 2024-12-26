from flask import Blueprint, jsonify, request

from http import HTTPStatus

from blueprints.subject import controller as subject_control

subject_route = Blueprint('subject', __name__, url_prefix='/api/subject')

@subject_route.route('/list', methods=['GET'])
def list():
    try:
        page = int(request.args.get('page', 1))
        perPage = int(request.args.get('perPage', 20))
        name = request.args.get('name')
        subjects = subject_control.get_all_classes_by_filter(page,perPage,name)
        content = subjects
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status

