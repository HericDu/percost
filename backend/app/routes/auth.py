from flask import Blueprint, request, jsonify, current_app
from app.models import User
from app.utils.auth import hash_password, check_password, generate_token, verify_token, get_current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password(password, user.password_hash):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 生成 token
    token = generate_token(user.id)
    
    return jsonify({
        'message': '登录成功',
        'token': token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    # JWT 是无状态的，客户端删除 token 即可
    return jsonify({'message': '登出成功'}), 200


@auth_bp.route('/verify', methods=['GET'])
def verify():
    """验证 Token 有效性"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'valid': False, 'error': '无效的 Token'}), 401
    
    return jsonify({
        'valid': True,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/user', methods=['GET'])
def get_user():
    """获取当前用户信息"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    return jsonify({'user': user.to_dict()}), 200
