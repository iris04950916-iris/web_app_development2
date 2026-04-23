from flask import render_template, request, redirect, url_for, flash, abort
from . import recipe_bp
from app.models.recipe import Recipe, Review, Ingredient, Step
from app.models.category import Category

@recipe_bp.route('/new', methods=['GET'])
def new_recipe():
    """
    顯示新增食譜表單頁面。
    邏輯: 取得所有分類資料，供表單的下拉選單或核取方塊使用。
    輸出: 渲染 templates/form.html
    """
    pass

@recipe_bp.route('/new', methods=['POST'])
def create_recipe():
    """
    接收表單資料並建立新食譜。
    輸入: title, description, image_url, calories, protein, carbs, fat 以及材料與步驟等表單資料。
    邏輯: 驗證必填欄位，處理圖片上傳，並將 Recipe, Ingredient, Step, recipe_category 寫入資料庫。
    輸出: 成功後重導向至該食譜的詳細頁面 (detail)。
    錯誤處理: 驗證失敗則重新渲染 form.html 並顯示錯誤訊息。
    """
    pass

@recipe_bp.route('/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    顯示單筆食譜詳細內容。
    輸入: 食譜 id
    邏輯: 查詢指定的食譜，並獲取其關聯的材料、步驟、營養資訊與評論。
    輸出: 渲染 templates/detail.html
    錯誤處理: 若找不到食譜則回傳 404 Not Found。
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET'])
def edit_recipe(id):
    """
    顯示編輯食譜表單頁面。
    輸入: 食譜 id
    邏輯: 查詢原有的食譜資料，以預填在表單上。
    輸出: 渲染 templates/form.html
    錯誤處理: 若找不到食譜則回傳 404 Not Found。
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['POST'])
def update_recipe(id):
    """
    接收表單資料並更新食譜。
    輸入: 食譜 id 與表單更新的內容。
    邏輯: 更新 Recipe 欄位，並更新關聯的 Ingredient, Step 等資料。
    輸出: 成功後重導向至詳情頁面。
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定的食譜。
    輸入: 食譜 id
    邏輯: 刪除指定的 Recipe，資料庫的 ON DELETE CASCADE 會一併刪除材料、步驟與評論。
    輸出: 重導向至首頁 (/)。
    """
    pass

@recipe_bp.route('/<int:id>/reviews', methods=['POST'])
def add_review(id):
    """
    在指定食譜新增評論與評分。
    輸入: 食譜 id, rating, content
    邏輯: 建立一筆新的 Review 紀錄並關聯至該食譜。
    輸出: 重導向回原本的食譜詳細頁面。
    """
    pass
