from flask import Blueprint, jsonify, request

from http import HTTPStatus

from blueprints.subject import controller as subject_control

subject_route = Blueprint('user-subject', __name__, url_prefix='/api/user-subject')

# @subject_route.route('/list-by-user', methods=['GET'])
# def list():
#     try:
#         id = request.args.get('user_id')
#         subjects = subject_control.get_all_classes_by_filter(page,perPage,name)
#         content = subjects
#         status = HTTPStatus.OK
#         return jsonify(content), status

#     except Exception as ex:
#         content = {
#             'error': str(ex)
#         }
#         status = HTTPStatus.INTERNAL_SERVER_ERROR
#         return jsonify(content), status

