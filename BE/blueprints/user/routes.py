from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from jwt import ExpiredSignatureError, InvalidTokenError

from http import HTTPStatus

import os,json,datetime,base64

from blueprints.user import controller as user_control

from blueprints.account.model import AccountModel

from blueprints.classes.model import ClassModel

from blueprints.user.model import UserModel, UserRole

from werkzeug.utils import secure_filename

user_route = Blueprint('user', __name__, url_prefix='/api/user')

@user_route.route('/roles', methods=['get'])
def rolesList():
    try:
        content = user_control.get_all_roles()
        status = HTTPStatus.OK
        return jsonify(content), status
    
    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status

@user_route.route('/list', methods=['get'])
# @jwt_required()
def userList():
    try:
        # get_jwt_identity()
        page = int(request.args.get('page', 1))
        perPage = int(request.args.get('perPage', 20))
        name = request.args.get('name')
        role = request.args.get('role')
        users = user_control.get_all_users_by_filter(page,perPage,name,role)
        total = UserModel.count_by_filter(name = name,role = role)
        for item in users:
            item['role'] = item['role'].value
        content = {
            'data': users,
            'total': total
        }
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status

@user_route.route('/upload-image', methods=['POST'])
def uploadImage():
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        os.makedirs("./data", exist_ok=True)
        file.save("data/{}".format(filename))
        with open("./data/{}".format(filename), "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
            url = "data:image/jpeg;base64," + my_string.decode('utf-8')  
        content = {
            'image' : url
        }
        status = HTTPStatus.OK
        return jsonify(content), status

    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status


@user_route.route('/my-information', methods=['GET'])
@jwt_required()
def getMyInformation():
    try:
        jwt = get_jwt_identity()
        myId = jwt.get('id')
        classId = jwt.get('class_id')
        me = UserModel.find_by_id(myId).convert_json()
        myClass = ClassModel.find_by_id(classId)
        status = HTTPStatus.OK
        me['role'] = me['role'].value
        me["class_name"] = myClass.class_name
        content = me
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


@user_route.route('/user-erase', methods=['DELETE'])
@jwt_required()
def DeleteUser():
    try:
        jwt = get_jwt_identity()
        # print(UserRole.admin)
        if( jwt.get('role') != str(UserRole.admin.value)):
            raise ValueError("You have no permission")
        id = request.args.get('id')
        account = AccountModel.find_by_id(id)
        account.delete_to_db()
        user = UserModel.find_by_id(id)
        user.delete_to_db()
        status = HTTPStatus.OK
        content = {
            'message': 'success'
        }
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
