from sqlalchemy import text
from app.db import db
import time

class AttendantModel(db.Model):
    __tablename__ = 'attendant'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)
    session_id = db.Column(db.Integer)
    attendant_time = db.Column(db.DateTime)
    type_check = db.Column(db.Integer)

    def __init__(self, user_id, room_id, session_id, type_check):
        self.user_id = user_id
        self.room_id = room_id
        self.session_id = session_id
        self.type_check = type_check
        self.attendant_time = int(time.time())

    def convert_json(self):
        inf_list = ['id','user_id', 'room_id', 'attendant_time', 'type_check', 'session_id']
        inf_list_DETAIL = [self.id, self.user_id, self.room_id, self.attendant_time, self.type_check, self.session_id]
        class_inf = {}
        for index, key in enumerate(inf_list):
            class_inf[key] = inf_list_DETAIL[index]

        return class_inf

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_record(self):
        db.session.commit()

    @classmethod
    def find_all_by_filter(cls, page = 1, perPage = 20, **kwargs):
        query = cls.query
        for key, value in kwargs.items():
            if value not in [None, ""]:
                query = query.filter(getattr(cls, key).ilike(f"%{value}%"))
        paginated_query = query.offset((page - 1) * perPage).limit(perPage)
        return paginated_query.all()

    @classmethod
    def get_all_records(cls):
        return cls.query.order_by(cls.id.desc()).all()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def find_by_name(cls, class_id):
        return cls.query.filter_by(class_id=class_id).first()
    
    @classmethod
    def search_by_display_name(cls, display_name):
        return cls.query.filter(text("lower(display_name) like lower(:term)")).params(term=f'%{display_name}%').all()
    