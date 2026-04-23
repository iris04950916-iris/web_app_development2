from flask import Flask
from app.models import db
from app.routes import index_bp, recipe_bp
import os

def create_app():
    app = Flask(__name__)
    
    # 基礎設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    # 設定 SQLite 資料庫路徑於 instance 目錄下
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化套件
    db.init_app(app)
    
    # 註冊 Blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(recipe_bp)
    
    # 自動建立資料表 (適用於開發初期)
    with app.app_context():
        db.create_all()
        
    return app
