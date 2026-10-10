import os
from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

# 前端构建产物目录（单容器部署时由构建阶段拷贝到此处）
STATIC_DIR = Path(os.environ.get(
    'FRONTEND_DIST',
    Path(__file__).resolve().parent.parent / 'static'
))


def create_app(config_name='default'):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    CORS(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.items import items_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')

    # 托管前端构建产物（单容器部署）。目录不存在时自动跳过，不影响本地前后端分离开发。
    if STATIC_DIR.is_dir():
        _register_spa(app)
    
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


def _register_spa(app):
    """用 Flask 直接托管 Vite 构建产物，实现单容器部署（前端 + 后端同进程）。"""

    # 带 hash 的静态资源永久缓存，index.html 不缓存，保证发版后立即生效
    IMMUTABLE_DIRS = ('assets/',)

    @app.route('/', defaults={'req_path': ''})
    @app.route('/<path:req_path>')
    def serve_spa(req_path):
        # /api 已由蓝图处理，此处不会命中；其余路径先查实体文件
        candidate = (STATIC_DIR / req_path).resolve()
        if req_path and candidate.is_file() and candidate.is_relative_to(STATIC_DIR.resolve()):
            resp = send_from_directory(STATIC_DIR, req_path)
            if req_path.startswith(IMMUTABLE_DIRS):
                resp.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            return resp

        # 其余一律回退到 index.html，交给 vue-router 处理
        resp = send_from_directory(STATIC_DIR, 'index.html')
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return resp
