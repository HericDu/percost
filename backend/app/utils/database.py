from datetime import datetime


def get_current_time():
    """获取当前时间字符串"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_current_date():
    """获取当前日期字符串"""
    return datetime.now().strftime('%Y-%m-%d')
