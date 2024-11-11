from sqlalchemy import text
from app.db import db
import datetime

class NotificationModel(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    user_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(self, message, user_id, class_id):
        self.message = message
        self.user_id = user_id
        self.class_id = class_id
        self.created_at = datetime.datetime.now()

    def convert_json(self):
        inf_list = ['id', 'message', 'user_id', 'class_id', 'created_at']
        inf_list_DETAIL = [self.id, self.message, self.user_id, self.class_id, self.created_at]
        notification_inf = {}
        for index, key in enumerate(inf_list):
            notification_inf[key] = inf_list_DETAIL[index]

        return notification_inf

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_record(self):
        db.session.commit()

    @classmethod
    def find_all_by_filter(cls, page = 1, perPage = 20 ,admin = 0, **kwargs):
        if( admin == 0 ):
            if "class_id" in kwargs and kwargs["class_id"] is None and "user_id" in kwargs and kwargs["user_id"] is None:
                return []
            
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
    