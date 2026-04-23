from . import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    @classmethod
    def create(cls, name):
        category = cls(name=name)
        db.session.add(category)
        db.session.commit()
        return category
        
    @classmethod
    def get_all(cls):
        return cls.query.all()
        
    @classmethod
    def get_by_id(cls, category_id):
        return cls.query.get(category_id)
        
    def update(self, name):
        self.name = name
        db.session.commit()
        return self
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
