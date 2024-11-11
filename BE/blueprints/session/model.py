from sqlalchemy import text
from app.db import db

class SessionModel(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    start_at = db.Column(db.Datetime)
    end_at = db.Column(db.Datetime)

    def __init__(self, class_id, start_at, end_at):
        self.class_id = class_id
        self.start_at = start_at
        self.end_at = end_at

    @classmethod
    def get_all_records(cls):
        return cls.query.order_by(cls.id.desc()).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, class_id):
        return cls.query.filter_by(class_id=class_id).first()
    
    @classmethod
    def search_by_display_name(cls, display_name):
        return cls.query.filter(text("lower(display_name) like lower(:term)")).params(term=f'%{display_name}%').all()
    