from flask import render_template, request
from . import index_bp
from app.models.recipe import Recipe
from app.models.category import Category

@index_bp.route('/', methods=['GET'])
def home():
    """
    顯示首頁與食譜列表。
    輸入: category_id (Query Parameter, 可選)
    邏輯: 若有 category_id 則篩選特定分類的食譜，否則列出所有食譜。取得所有分類供篩選區塊使用。
    輸出: 渲染 templates/index.html
    """
    category_id = request.args.get('category_id', type=int)
    categories = Category.get_all()
    
    if category_id:
        # 使用 Flask-SQLAlchemy 查詢關聯表中包含特定分類的食譜
        recipes = Recipe.query.filter(Recipe.categories.any(id=category_id)).all()
    else:
        recipes = Recipe.get_all()
        
    return render_template('index.html', recipes=recipes, categories=categories, current_category_id=category_id)
