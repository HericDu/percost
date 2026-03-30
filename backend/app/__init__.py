from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    CORS(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.items import items_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    
    # 创建数据库表
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"数据库初始化警告: {e}")
            pass
        # 初始化管理员账号
        from app.models import User
        from app.utils.auth import init_admin
        init_admin()
    
    return app
