from flask import render_template, request, redirect, url_for, flash, abort
from . import recipe_bp
from app.models import db
from app.models.recipe import Recipe, Review, Ingredient, Step
from app.models.category import Category

@recipe_bp.route('/new', methods=['GET'])
def new_recipe():
    """顯示新增食譜表單頁面。"""
    categories = Category.get_all()
    return render_template('form.html', categories=categories, recipe=None)

@recipe_bp.route('/new', methods=['POST'])
def create_recipe():
    """接收表單資料並建立新食譜。"""
    title = request.form.get('title')
    description = request.form.get('description')
    image_url = request.form.get('image_url')
    
    if not title:
        flash('標題為必填欄位', 'error')
        return redirect(url_for('recipe.new_recipe'))
        
    # 營養資訊 (可選)
    try:
        calories = float(request.form.get('calories')) if request.form.get('calories') else None
        protein = float(request.form.get('protein')) if request.form.get('protein') else None
        carbs = float(request.form.get('carbs')) if request.form.get('carbs') else None
        fat = float(request.form.get('fat')) if request.form.get('fat') else None
    except ValueError:
        flash('營養資訊格式錯誤，請輸入數字', 'error')
        return redirect(url_for('recipe.new_recipe'))

    # 建立食譜
    recipe = Recipe.create(
        title=title, description=description, image_url=image_url,
        calories=calories, protein=protein, carbs=carbs, fat=fat
    )
    
    if not recipe:
        flash('新增食譜失敗，請稍後再試', 'error')
        return redirect(url_for('recipe.new_recipe'))
        
    # 處理分類
    category_ids = request.form.getlist('category_ids')
    if category_ids:
        for cid in category_ids:
            cat = Category.get_by_id(int(cid))
            if cat:
                recipe.categories.append(cat)
        db.session.commit()
        
    # 處理食材
    ingredient_names = request.form.getlist('ingredient_name[]')
    ingredient_amounts = request.form.getlist('ingredient_amount[]')
    for name, amount in zip(ingredient_names, ingredient_amounts):
        if name.strip() and amount.strip():
            Ingredient.create(recipe.id, name.strip(), amount.strip())
            
    # 處理步驟
    step_instructions = request.form.getlist('step_instruction[]')
    for idx, instruction in enumerate(step_instructions, start=1):
        if instruction.strip():
            Step.create(recipe.id, idx, instruction.strip())
            
    flash('食譜新增成功！', 'success')
    return redirect(url_for('recipe.recipe_detail', id=recipe.id))

@recipe_bp.route('/<int:id>', methods=['GET'])
def recipe_detail(id):
    """顯示單筆食譜詳細內容。"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('detail.html', recipe=recipe)

@recipe_bp.route('/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """顯示編輯食譜表單頁面。"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    categories = Category.get_all()
    selected_category_ids = [c.id for c in recipe.categories]
    return render_template('form.html', recipe=recipe, categories=categories, selected_category_ids=selected_category_ids)

@recipe_bp.route('/<int:id>/edit', methods=['POST'])
def update_recipe(id):
    """接收表單資料並更新食譜。"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    title = request.form.get('title')
    if not title:
        flash('標題為必填欄位', 'error')
        return redirect(url_for('recipe.edit_recipe', id=id))
        
    try:
        recipe.title = title
        recipe.description = request.form.get('description')
        recipe.image_url = request.form.get('image_url')
        recipe.calories = float(request.form.get('calories')) if request.form.get('calories') else None
        recipe.protein = float(request.form.get('protein')) if request.form.get('protein') else None
        recipe.carbs = float(request.form.get('carbs')) if request.form.get('carbs') else None
        recipe.fat = float(request.form.get('fat')) if request.form.get('fat') else None
    except ValueError:
        flash('營養資訊格式錯誤，請輸入數字', 'error')
        return redirect(url_for('recipe.edit_recipe', id=id))

    # 更新分類
    category_ids = request.form.getlist('category_ids')
    recipe.categories = []
    for cid in category_ids:
        cat = Category.get_by_id(int(cid))
        if cat:
            recipe.categories.append(cat)
            
    # 清除舊的食材和步驟並重新寫入
    for ing in recipe.ingredients:
        ing.delete()
    for step in recipe.steps:
        step.delete()
        
    ingredient_names = request.form.getlist('ingredient_name[]')
    ingredient_amounts = request.form.getlist('ingredient_amount[]')
    for name, amount in zip(ingredient_names, ingredient_amounts):
        if name.strip() and amount.strip():
            Ingredient.create(recipe.id, name.strip(), amount.strip())
            
    step_instructions = request.form.getlist('step_instruction[]')
    for idx, instruction in enumerate(step_instructions, start=1):
        if instruction.strip():
            Step.create(recipe.id, idx, instruction.strip())
            
    db.session.commit()
    
    flash('食譜更新成功！', 'success')
    return redirect(url_for('recipe.recipe_detail', id=recipe.id))

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """刪除指定的食譜。"""
    recipe = Recipe.get_by_id(id)
    if recipe:
        recipe.delete()
        flash('食譜已成功刪除', 'success')
    return redirect(url_for('index.home'))

@recipe_bp.route('/<int:id>/reviews', methods=['POST'])
def add_review(id):
    """新增評論與評分。"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    rating = request.form.get('rating')
    content = request.form.get('content')
    
    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        flash('請提供1到5星的評分', 'error')
        return redirect(url_for('recipe.recipe_detail', id=id))
        
    Review.create(recipe_id=id, rating=int(rating), content=content)
    flash('評論已送出', 'success')
    return redirect(url_for('recipe.recipe_detail', id=id))
