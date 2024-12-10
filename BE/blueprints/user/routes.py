from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from jwt import ExpiredSignatureError, InvalidTokenError

from http import HTTPStatus

import os,json,datetime,base64

from blueprints.user import controller as user_control
from blueprints.classes import controller as class_control
from blueprints.gender import controller as gender_control
from blueprints.user_subject import controller as user_subject_control

from blueprints.account.model import AccountModel
from blueprints.classes.model import ClassModel
from blueprints.user.model import UserModel, UserRole
from blueprints.user_subject.model import UserSubjectModel

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
            item['subject'] = user_subject_control.get_by_user_id(item['id'])
            if item['class_id']:
                item['class'] = class_control.get_by_id(item['class_id'])
            if item['gender_id']:
                item['gender'] = gender_control.get_by_id(item['gender_id'])
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
    
@user_route.route('/change-info/<int:user_id>', methods=['patch'])
def changeInfo(user_id):
    try:
        data = request.get_json()
        user = UserModel.find_by_id(user_id)
        if 'subject' in data:
            subs = user_subject_control.get_model_by_user_id(user_id)
            for sub in subs:
                sub.delete_to_db()
            subjects = data['subject']
            for subject_id in subjects:
                new_relative = UserSubjectModel(
                    user_id=user_id,
                    subject_id=subject_id
                )
                new_relative.save_to_db()
            del data['subject']
        for key, value in data.items():
            if hasattr(user, key):  # Check if the attribute exists in the User model
                setattr(user, key, value)
        user.save_record()
        content = {
            'message' : 'success'
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
        me['subject'] = user_subject_control.get_by_user_id(me['id'])
        if me['class_id']:
            me['class'] = class_control.get_by_id(me['class_id'])
        if me['gender_id']:
            me['gender'] = gender_control.get_by_id(me['gender_id'])
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
