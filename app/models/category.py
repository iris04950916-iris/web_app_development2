from . import db

class Category(db.Model):
    """分類模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    @classmethod
    def create(cls, name):
        """新增分類"""
        try:
            category = cls(name=name)
            db.session.add(category)
            db.session.commit()
            return category
        except Exception as e:
            db.session.rollback()
            print(f"Error creating category: {e}")
            return None
        
    @classmethod
    def get_all(cls):
        """取得所有分類"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
        
    @classmethod
    def get_by_id(cls, category_id):
        """取得單筆分類"""
        try:
            return cls.query.get(category_id)
        except Exception as e:
            print(f"Error getting category {category_id}: {e}")
            return None
        
    def update(self, name):
        """更新分類"""
        try:
            self.name = name
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating category: {e}")
            return None
        
    def delete(self):
        """刪除分類"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting category: {e}")
            return False
