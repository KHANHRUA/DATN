from sqlalchemy import text
from app.db import db

class SessionModel(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    session_id = db.Column(db.Integer)
    attendant_time = db.Column(db.Datetime)
    leave_time = db.Column(db.Datetime)

    def __init__(self, user_id, session_id, attendant_time, leave_time):
        self.user_id = user_id
        self.session_id = session_id
        self.attendant_time = attendant_time
        self.leave_time = leave_time

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
    