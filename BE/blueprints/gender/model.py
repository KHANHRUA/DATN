from app.db import db



class GenderModel(db.Model):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String)

    def __init__(self, gender):
        self.gender = gender

    def convert_json(self):
        inf_list = ['id', 'gender']
        inf_list_DETAIL = [self.id, self.gender]
        gender_inf = {}
        for index, key in enumerate(inf_list):
            gender_inf[key] = inf_list_DETAIL[index]

        return gender_inf

    @classmethod
    def get_all_records(cls):
        return cls.query.order_by(cls.id.asc()).all()
    

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, gender):
        return cls.query.filter_by(gender=gender).first()
    
    