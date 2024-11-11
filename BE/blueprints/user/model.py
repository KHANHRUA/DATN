from enum import Enum
from sqlalchemy import Enum as SqlAlchemyEnum
from app.db import db

class UserRole(Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    role = db.Column(SqlAlchemyEnum(UserRole), nullable=False)
    face_image = db.Column(db.String)
    gender_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)

    def __init__(self, name, age, role, face_image, gender_id, class_id):
        self.name = name
        self.age = age
        self.role = role
        self.face_image = face_image
        self.gender_id = gender_id
        self.class_id = class_id

    def convert_json(self):
        user_list = ['id', 'name', 'age','role', 'face_image', 'gender_id', 'class_id']
        user_list_DETAIL = [self.id, self.name, self.age, self.role, self.face_image, self.gender_id, self.class_id]
        user_infor = {}
        for index, key in enumerate(user_list):
            user_infor[key] = user_list_DETAIL[index]

        return user_infor

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_record(self):
        db.session.commit()

    @classmethod
    def get_all_records(cls):
        return cls.query.order_by(cls.id.desc()).all()
    
    @classmethod
    def find_all_by_filter(cls, page = 1, perPage = 10, **kwargs):
        query = cls.query
        for key, value in kwargs.items():
            if value not in [None, ""]:
                query = query.filter(getattr(cls, key).ilike(f"%{value}%"))
        paginated_query = query.offset((page - 1) * perPage).limit(perPage)
        return paginated_query.all()
    
    @classmethod
    def count_by_filter(cls, **kwargs):
        filtered_kwargs = {key: value for key, value in kwargs.items() if value not in [None, ""]}
        return cls.query.filter_by(**filtered_kwargs).count()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    