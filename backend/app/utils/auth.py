import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app
from app.models import User
from app import db


def hash_password(password):
    """加密密码"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password, password_hash):
    """验证密码"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def generate_token(user_id):
    """生成 JWT Token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRE_DAYS']),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], 
                       algorithm=current_app.config['JWT_ALGORITHM'])
    return token


def verify_token(token):
    """验证 JWT Token"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'],
                            algorithms=[current_app.config['JWT_ALGORITHM']])
        return True, payload['user_id']
    except jwt.ExpiredSignatureError:
        return False, 'Token 已过期'
    except jwt.InvalidTokenError:
        return False, '无效的 Token'


def init_admin():
    """初始化管理员账号"""
    try:
        admin = User.query.filter_by(username=current_app.config['ADMIN_USERNAME']).first()
        
        if not admin:
            admin = User(
                username=current_app.config['ADMIN_USERNAME'],
                password_hash=hash_password(current_app.config['ADMIN_PASSWORD']),
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            db.session.add(admin)
            db.session.commit()
            print(f"管理员账号已创建: {current_app.config['ADMIN_USERNAME']}")
    except Exception as e:
        db.session.rollback()
        print(f"初始化管理员账号时出错: {e}")


def get_current_user(request):
    """从请求中获取当前用户"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    # Bearer token format
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    token = parts[1]
    is_valid, result = verify_token(token)
    
    if not is_valid:
        return None
    
    user = User.query.get(result)
    return user
