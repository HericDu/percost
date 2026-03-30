import os
from app import create_app

# 从环境变量获取配置名称，默认为 development
config_name = os.environ.get('FLASK_ENV', 'development')

app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
