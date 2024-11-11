from sqlalchemy import text
from app.db import db



class ClassModel(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String)

    def __init__(self, class_name):
        self.class_name = class_name

    def convert_json(self):
        inf_list = ['id', 'class_name']
        inf_list_DETAIL = [self.id, self.class_name]
        class_inf = {}
        for index, key in enumerate(inf_list):
            class_inf[key] = inf_list_DETAIL[index]

        return class_inf

    @classmethod
    def get_all_records(cls):
        return cls.query.order_by(cls.id.desc()).all()
    
    @classmethod
    def find_all_by_filter(cls, page = 1, perPage = 20, **kwargs):
        query = cls.query
        for key, value in kwargs.items():
            if value not in [None, ""]:
                query = query.filter(getattr(cls, key).ilike(f"%{value}%"))
        paginated_query = query.offset((page - 1) * perPage).limit(perPage)
        return paginated_query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, class_name):
        return cls.query.filter_by(class_name=class_name).first()
    
    @classmethod
    def search_by_display_name(cls, display_name):
        return cls.query.filter(text("lower(display_name) like lower(:term)")).params(term=f'%{display_name}%').all()
    