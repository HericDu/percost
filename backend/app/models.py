from datetime import datetime
from app import db


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(20), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at
        }


class Item(db.Model):
    """物品表"""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    emoji = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    purchase_amount = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.String(20), nullable=False)
    extra_cost = db.Column(db.Integer, default=0)
    disposal_price = db.Column(db.Integer, default=0)
    remark = db.Column(db.Text)
    usage_frequency_type = db.Column(db.String(20))
    usage_frequency_value = db.Column(db.Integer, default=1)
    expiry_date = db.Column(db.String(20))  # 使用截止日期 YYYY-MM-DD
    manual_usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.String(20), nullable=False)
    
    # 关联图片
    images = db.relationship('ItemImage', backref='item', lazy='dynamic', 
                            cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'emoji': self.emoji,
            'name': self.name,
            'category': self.category,
            'purchase_amount': self.purchase_amount,
            'purchase_date': self.purchase_date,
            'extra_cost': self.extra_cost,
            'disposal_price': self.disposal_price,
            'remark': self.remark,
            'usage_frequency_type': self.usage_frequency_type,
            'usage_frequency_value': self.usage_frequency_value,
            'expiry_date': self.expiry_date,
            'manual_usage_count': self.manual_usage_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'images': [img.to_dict() for img in self.images]
        }


class ItemImage(db.Model):
    """物品图片表"""
    __tablename__ = 'item_images'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    image_data = db.Column(db.Text, nullable=False)
    image_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(20), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'image_data': self.image_data,
            'image_order': self.image_order,
            'created_at': self.created_at
        }
