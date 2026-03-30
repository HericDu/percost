import os
from pathlib import Path

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    BASE_DIR = Path(__file__).resolve().parent.parent  # 指向 backend 目录
    
    # 在 Docker 中使用 /app/data，本地开发使用相对路径
    DATA_DIR = Path(os.environ.get('DATA_DIR', '/app/data' if Path('/app').exists() else BASE_DIR / 'data'))
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{DATA_DIR}/percost.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRE_DAYS = int(os.environ.get('TOKEN_EXPIRE_DAYS', 7))
    
    # 管理员配置
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 最大上传大小
    UPLOAD_FOLDER = DATA_DIR / 'uploads'
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    
    # CORS 配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
