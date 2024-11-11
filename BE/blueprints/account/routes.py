from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from jwt import ExpiredSignatureError, InvalidTokenError

from http import HTTPStatus

import datetime

import base64

import bcrypt

from blueprints.account.model import AccountModel

from blueprints.user.model import UserModel

def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    # Verify the password by checking it against the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

auth_route = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_route.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        username = data['username']
        password = data['password']

        account = AccountModel.find_by_name(username)  
        if account is None:
            raise ValueError("The user not found")

        if account and verify_password(password, account.password):
            user = UserModel.find_by_id(account.user_id)  
            user_dict = {
                'id': user.id,
                'name': user.name,
                'age': user.age,
                'role': user.role.value,
                'gender_id': user.gender_id,
                'class_id': user.class_id
            }
            access_token = create_access_token(identity=user_dict, expires_delta=datetime.timedelta(weeks=1))
            refesh_token = create_refresh_token(identity=user_dict)     

            content = {
                'message' : 'Logged in successfully',
                'access_token' : access_token,
                'refresh_token' : refesh_token,
                'user': user_dict
            }
            status = HTTPStatus.OK
            return jsonify(content), status
        else:
            raise ValueError('Wrong username or password')
        
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

@auth_route.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        name = data['name']
        age = data['age']
        role = data['role']
        face_image = data['face_image']
        gender_id = data['gender_id']
        class_id = data['class_id']
        username = data['username']
        password = data['password']

        account = AccountModel.find_by_name(username)  
        print(account)
        if account:
            raise ValueError("The user already exist")
        
        newUser = UserModel(
            name=name,
            age=age,
            role=role,
            face_image=face_image,
            gender_id=gender_id,
            class_id=class_id
        )

        newUser.save_to_db()
        
        newAccount = AccountModel(
            username=username,
            password=hash_password(password),
            user_id=newUser.id
        )

        newAccount.save_to_db()

        createdAccount = {
            "username": username,
            "password": password,
            "message": 'Create account success'
        }
        status = HTTPStatus.OK
        return jsonify(createdAccount), status
        
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
        print(str(ex))
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status

@auth_route.route('/user-check', methods=['GET'])
@jwt_required()
def Auth():
    try:
        jwt_parse = get_jwt_identity()
        content = jwt_parse
        status = HTTPStatus.OK
        return jsonify(content), status
    except Exception as ex:
        content = {
            'error': str(ex)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return jsonify(content), status
