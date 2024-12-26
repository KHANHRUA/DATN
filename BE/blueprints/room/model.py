from sqlalchemy import text
from app.db import db

class RoomModel(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String)

    def __init__(self, room_name):
        self.room_name = room_name

    def convert_json(self):
        inf_list = ['id', 'room_name']
        inf_list_DETAIL = [self.id, self.room_name]
        room_inf = {}
        for index, key in enumerate(inf_list):
            room_inf[key] = inf_list_DETAIL[index]

        return room_inf

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_record(self):
        db.session.commit()

    @classmethod
    def find_all_by_filter(cls, page = 1, perPage = 20 , **kwargs):  
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
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, room_name):
        return cls.query.filter_by(room_name=room_name).first()
    