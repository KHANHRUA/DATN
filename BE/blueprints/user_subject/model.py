from app.db import db



class UserSubjectModel(db.Model):
    __tablename__ = 'user-subject'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    subject_id = db.Column(db.Integer)

    def __init__(self, user_id, subject_id):
        self.user_id = user_id
        self.subject_id = subject_id

    def convert_json(self):
        inf_list = ['id', 'user_id', 'subject_id']
        inf_list_DETAIL = [self.id, self.user_id, self.subject_id]
        relative_inf = {}
        for index, key in enumerate(inf_list):
            relative_inf[key] = inf_list_DETAIL[index]

        return relative_inf
    
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
        return cls.query.order_by(cls.id.asc()).all()
    
    @classmethod
    def find_all_by_filter(cls, page = 1, perPage = 20, **kwargs):
        query = cls.query
        for key, value in kwargs.items():
            if value not in [None, ""]:
                query = query.filter(getattr(cls, key).ilike(f"%{value}%"))
        paginated_query = query.offset((page - 1) * perPage).limit(perPage)
        return paginated_query.all()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def find_by_subject_id(cls, subject_id):
        return cls.query.filter_by(subject_id=subject_id).all()
    
    # @classmethod
    # def find_by_name(cls, name):
    #     return cls.query.filter_by(name=name).first()
    
    