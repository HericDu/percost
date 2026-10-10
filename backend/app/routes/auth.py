import hmac

from flask import Blueprint, request, jsonify, current_app
from app.models import User
from app.utils.auth import hash_password, check_password, generate_token, verify_token, get_current_user
from app.utils.ratelimit import check_rate_limit, reset_rate_limit, client_ip

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/gate', methods=['POST'])
def gate():
    """校验管理后台入口路径。

    设计要点：真实路径只存在于服务端，绝不下发给客户端，
    前端只能提交候选路径由此接口比对，避免扫描者直接从 JS 中读取。
    """
    ip = client_ip(request)

    # 入口探测的限流比登录更严格：路径空间大，爆破价值低但噪音高
    allowed, retry_after = check_rate_limit(f'gate:{ip}', limit=10, window=300)
    if not allowed:
        return jsonify({'ok': False, 'retry_after': retry_after}), 429

    data = request.get_json(silent=True) or {}
    candidate = str(data.get('path', '')).strip().strip('/')
    expected = current_app.config['ADMIN_PATH']

    # 常量时间比较，避免通过响应耗时逐字符推断路径
    if not expected or not hmac.compare_digest(candidate, expected):
        return jsonify({'ok': False}), 404

    reset_rate_limit(f'gate:{ip}')
    return jsonify({'ok': True}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    ip = client_ip(request)

    # 密码爆破防护：15 分钟内最多 8 次失败
    allowed, retry_after = check_rate_limit(f'login:{ip}', limit=8, window=900)
    if not allowed:
        return jsonify({
            'error': f'尝试过于频繁，请 {retry_after} 秒后重试'
        }), 429

    data = request.get_json(silent=True)

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

    reset_rate_limit(f'login:{ip}')
    
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
