from sqlalchemy import text
from app.db import db
import datetime

class SessionModel(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    subject_id = db.Column(db.Integer)
    class_period = db.Column(db.Integer)

    def __init__(self, class_id, start_at, end_at, subject_id, class_period):
        self.class_id = class_id
        self.start_at = start_at
        self.end_at = end_at
        self.subject_id = subject_id
        self.class_period = class_period

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()    

    def convert_json(self):
        inf_list = ['id', 'class_id', 'start_at', 'end_at', 'subject_id', 'class_period']
        inf_list_DETAIL = [self.id, self.class_id, self.start_at, self.end_at, self.subject_id, self.class_period]
        session_inf = {}
        for index, key in enumerate(inf_list):
            session_inf[key] = inf_list_DETAIL[index]

        return session_inf

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
    
    # @classmethod
    # def filter_by_date_range(cls, start_date=None, end_date=None, **kwargs):
    #     # Xử lý logic thời gian
    #     date_range = None
    #     if start_date and end_date:
    #         date_range = (start_date, end_date)
    #     elif start_date:
    #         date_range = (start_date, datetime.max)
    #     elif end_date:
    #         date_range = (datetime.min, end_date)

    #     if date_range:
    #         kwargs['start_time'] = date_range

    #     # Gọi lại find_all_by_filter với các điều kiện đã xử lý
    #     return cls.find_all_by_filter(**kwargs)
    
    @classmethod
    def find_all_by_filter(cls, **kwargs):
        query = cls.query
        for key, value in kwargs.items():
            if value not in [None, ""]:
                if isinstance(value, tuple) and len(value) == 2 and all(isinstance(v, datetime) for v in value):
                    query = query.filter(getattr(cls, key).between(value[0], value[1]))
                else:
                    query = query.filter(getattr(cls, key).ilike(f"%{value}%"))
        return query.all()