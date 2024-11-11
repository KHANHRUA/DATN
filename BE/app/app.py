from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from flask import Flask
from blueprints.account.routes import auth_route
from blueprints.gender.routes import gender_route
from blueprints.user.routes import user_route
from blueprints.classes.routes import class_route
from blueprints.notification.routes import notification_route
from app.db import db


app = Flask(__name__, instance_relative_config=True, static_folder='./dist/static',
            template_folder='./dist')

app = Flask(__name__)

# Cấu hình kết nối MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/datn'

app.config['SECRET_KEY'] = "khanh"
app.config["JWT_SECRET_KEY"] = "khanhrua"

CORS(app, resource={r"/*": {"origins": "*"}}, allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "cache-control", "Pragma", "Expires", "Access-Control-Allow-Credentials"], supports_credentials=True)

app.register_blueprint(auth_route)
app.register_blueprint(gender_route)
app.register_blueprint(user_route)
app.register_blueprint(class_route)
app.register_blueprint(notification_route)

jwt = JWTManager(app)


