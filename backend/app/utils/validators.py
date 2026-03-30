import re
from flask import jsonify


def validate_item_data(data):
    """验证物品数据"""
    errors = []
    
    # 必填字段验证
    if not data.get('emoji'):
        errors.append('图标（Emoji）不能为空')
    
    if not data.get('name'):
        errors.append('物品名称不能为空')
    
    if not data.get('category'):
        errors.append('分类不能为空')
    
    if data.get('purchase_amount') is None:
        errors.append('购买金额不能为空')
    elif not isinstance(data['purchase_amount'], (int, float)) or data['purchase_amount'] < 0:
        errors.append('购买金额必须是非负数')
    
    if not data.get('purchase_date'):
        errors.append('购买日期不能为空')
    else:
        # 验证日期格式
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, data['purchase_date']):
            errors.append('购买日期格式不正确，应为 YYYY-MM-DD')
    
    # 可选字段验证
    if data.get('extra_cost') is not None:
        if not isinstance(data['extra_cost'], (int, float)) or data['extra_cost'] < 0:
            errors.append('额外成本必须是非负数')
    
    if data.get('disposal_price') is not None:
        if not isinstance(data['disposal_price'], (int, float)) or data['disposal_price'] < 0:
            errors.append('处置价格必须是非负数')
    
    if data.get('expiry_date') is not None and data.get('expiry_date') != '':
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, data['expiry_date']):
            errors.append('使用截止日期格式不正确，应为 YYYY-MM-DD')
    
    # 使用频率验证
    valid_frequency_types = ['daily', 'weekly', 'monthly', 'yearly', 'manual']
    if data.get('usage_frequency_type') and data['usage_frequency_type'] not in valid_frequency_types:
        errors.append('使用频率类型不正确')
    
    if data.get('usage_frequency_value') is not None:
        if not isinstance(data['usage_frequency_value'], int) or data['usage_frequency_value'] < 1:
            errors.append('使用频率值必须是正整数')
    
    return errors


def validate_image_size(image_data, max_size_mb=5):
    """验证图片大小"""
    if not image_data:
        return False, '图片数据为空'
    
    # Base64 编码后的大小约为原始数据的 4/3
    # 粗略估算原始大小
    size_bytes = len(image_data.encode('utf-8'))
    size_mb = size_bytes / (1024 * 1024)
    
    if size_mb > max_size_mb:
        return False, f'图片大小不能超过 {max_size_mb}MB'
    
    return True, None
