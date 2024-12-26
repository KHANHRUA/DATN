from app.db import db



class SubjectModel(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

    def convert_json(self):
        inf_list = ['id', 'name']
        inf_list_DETAIL = [self.id, self.name]
        subject_inf = {}
        for index, key in enumerate(inf_list):
            subject_inf[key] = inf_list_DETAIL[index]

        return subject_inf

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
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    