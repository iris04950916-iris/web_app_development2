from datetime import datetime
from . import db
from .category import Category

# 多對多關聯的關聯表 (Recipe <-> Category)
recipe_category = db.Table('recipe_category',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)

class Recipe(db.Model):
    """食譜模型"""
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    calories = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯設定
    categories = db.relationship('Category', secondary=recipe_category, lazy='subquery',
        backref=db.backref('recipes', lazy=True))
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade="all, delete-orphan")
    steps = db.relationship('Step', backref='recipe', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='recipe', lazy=True, cascade="all, delete-orphan")
    
    @classmethod
    def create(cls, title, description=None, image_url=None, calories=None, protein=None, carbs=None, fat=None):
        """新增食譜"""
        try:
            recipe = cls(
                title=title, description=description, image_url=image_url,
                calories=calories, protein=protein, carbs=carbs, fat=fat
            )
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            print(f"Error creating recipe: {e}")
            return None
        
    @classmethod
    def get_all(cls):
        """取得所有食譜"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting recipes: {e}")
            return []
        
    @classmethod
    def get_by_id(cls, recipe_id):
        """依 ID 取得食譜"""
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            print(f"Error getting recipe {recipe_id}: {e}")
            return None
        
    def update(self, **kwargs):
        """更新食譜資料"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating recipe: {e}")
            return None
        
    def delete(self):
        """刪除食譜"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting recipe: {e}")
            return False


class Ingredient(db.Model):
    """食材模型"""
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(50), nullable=False)
    
    @classmethod
    def create(cls, recipe_id, name, amount):
        """新增食材"""
        try:
            ingredient = cls(recipe_id=recipe_id, name=name, amount=amount)
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            print(f"Error creating ingredient: {e}")
            return None
        
    def update(self, name=None, amount=None):
        """更新食材"""
        try:
            if name: self.name = name
            if amount: self.amount = amount
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating ingredient: {e}")
            return None
        
    def delete(self):
        """刪除食材"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting ingredient: {e}")
            return False


class Step(db.Model):
    """步驟模型"""
    __tablename__ = 'steps'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    
    @classmethod
    def create(cls, recipe_id, step_number, instruction):
        """新增步驟"""
        try:
            step = cls(recipe_id=recipe_id, step_number=step_number, instruction=instruction)
            db.session.add(step)
            db.session.commit()
            return step
        except Exception as e:
            db.session.rollback()
            print(f"Error creating step: {e}")
            return None
        
    def update(self, step_number=None, instruction=None):
        """更新步驟"""
        try:
            if step_number: self.step_number = step_number
            if instruction: self.instruction = instruction
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating step: {e}")
            return None
        
    def delete(self):
        """刪除步驟"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting step: {e}")
            return False


class Review(db.Model):
    """評論模型"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def create(cls, recipe_id, rating, content=None):
        """新增評論"""
        try:
            review = cls(recipe_id=recipe_id, rating=rating, content=content)
            db.session.add(review)
            db.session.commit()
            return review
        except Exception as e:
            db.session.rollback()
            print(f"Error creating review: {e}")
            return None
        
    def update(self, rating=None, content=None):
        """更新評論"""
        try:
            if rating: self.rating = rating
            if content is not None: self.content = content
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating review: {e}")
            return None
        
    def delete(self):
        """刪除評論"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting review: {e}")
            return False
