from flask import Blueprint, request, jsonify
from app.models import Item, ItemImage
from app import db
from app.utils.database import get_current_time, get_current_date
from app.utils.validators import validate_item_data, validate_image_size
from app.utils.auth import get_current_user

items_bp = Blueprint('items', __name__)


@items_bp.route('', methods=['GET'])
def get_items():
    """获取所有物品（公开）"""
    # 支持搜索和筛选
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    query = Item.query
    
    # 搜索
    if search:
        query = query.filter(Item.name.contains(search))
    
    # 分类筛选
    if category:
        query = query.filter(Item.category == category)
    
    # 排序（白名单校验防止任意字段排序）
    ALLOWED_SORT_COLUMNS = {
        'id': Item.id, 'name': Item.name, 'category': Item.category,
        'purchase_amount': Item.purchase_amount, 'purchase_date': Item.purchase_date,
        'created_at': Item.created_at, 'updated_at': Item.updated_at,
        'extra_cost': Item.extra_cost, 'disposal_price': Item.disposal_price,
    }
    ALLOWED_SORT_ORDERS = {'asc', 'desc'}

    if sort_by not in ALLOWED_SORT_COLUMNS:
        sort_by = 'created_at'
    if sort_order not in ALLOWED_SORT_ORDERS:
        sort_order = 'desc'

    sort_column = ALLOWED_SORT_COLUMNS[sort_by]
    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    items = query.all()
    
    return jsonify({
        'items': [item.to_dict() for item in items],
        'total': len(items)
    }), 200


@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """获取单个物品（公开）"""
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'error': '物品不存在'}), 404
    
    return jsonify({'item': item.to_dict()}), 200


@items_bp.route('', methods=['POST'])
def create_item():
    """创建新物品（需认证）"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    # 验证数据
    errors = validate_item_data(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # 创建物品
    item = Item(
        emoji=data['emoji'],
        name=data['name'],
        category=data['category'],
        purchase_amount=int(data['purchase_amount']),
        purchase_date=data['purchase_date'],
        extra_cost=int(data.get('extra_cost', 0)),
        disposal_price=int(data.get('disposal_price', 0)),
        remark=data.get('remark'),
        usage_frequency_type=data.get('usage_frequency_type'),
        usage_frequency_value=data.get('usage_frequency_value', 1),
        expiry_date=data.get('expiry_date') or None,
        manual_usage_count=0,
        created_at=get_current_time(),
        updated_at=get_current_time()
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({
        'message': '物品创建成功',
        'item': item.to_dict()
    }), 201


@items_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """更新物品（需认证）"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'error': '物品不存在'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    # 验证数据
    errors = validate_item_data(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # 更新物品
    item.emoji = data['emoji']
    item.name = data['name']
    item.category = data['category']
    item.purchase_amount = int(data['purchase_amount'])
    item.purchase_date = data['purchase_date']
    item.extra_cost = int(data.get('extra_cost', 0))
    item.disposal_price = int(data.get('disposal_price', 0))
    item.remark = data.get('remark')
    item.usage_frequency_type = data.get('usage_frequency_type')
    item.usage_frequency_value = data.get('usage_frequency_value', 1)
    item.expiry_date = data.get('expiry_date') or None
    item.updated_at = get_current_time()
    
    db.session.commit()
    
    return jsonify({
        'message': '物品更新成功',
        'item': item.to_dict()
    }), 200


@items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """删除物品（需认证）"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'error': '物品不存在'}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': '物品删除成功'}), 200


@items_bp.route('/<int:item_id>/images', methods=['POST'])
def upload_image(item_id):
    """上传物品图片（需认证）"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'error': '物品不存在'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('image_data'):
        return jsonify({'error': '图片数据不能为空'}), 400
    
    # 检查图片数量限制
    existing_count = item.images.count()
    if existing_count >= 3:
        return jsonify({'error': '每个物品最多上传3张图片'}), 400
    
    # 验证图片大小
    is_valid, error_msg = validate_image_size(data['image_data'])
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # 创建图片记录
    image = ItemImage(
        item_id=item_id,
        image_data=data['image_data'],
        image_order=existing_count + 1,
        created_at=get_current_time()
    )
    
    db.session.add(image)
    db.session.commit()
    
    return jsonify({
        'message': '图片上传成功',
        'image': image.to_dict()
    }), 201


@items_bp.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """删除图片（需认证）"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    image = ItemImage.query.get(image_id)
    
    if not image:
        return jsonify({'error': '图片不存在'}), 404
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'message': '图片删除成功'}), 200


@items_bp.route('/<int:item_id>/usage', methods=['POST'])
def record_usage(item_id):
    """记录使用次数（需认证）"""
    user = get_current_user(request)
    
    if not user:
        return jsonify({'error': '未登录'}), 401
    
    item = Item.query.get(item_id)
    
    if not item:
        return jsonify({'error': '物品不存在'}), 404
    
    data = request.get_json() or {}
    action = data.get('action', 'increment')  # increment or decrement
    
    if action == 'increment':
        item.manual_usage_count += 1
    elif action == 'decrement' and item.manual_usage_count > 0:
        item.manual_usage_count -= 1
    
    item.updated_at = get_current_time()
    db.session.commit()
    
    return jsonify({
        'message': '使用次数已更新',
        'manual_usage_count': item.manual_usage_count
    }), 200
