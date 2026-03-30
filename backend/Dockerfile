FROM python:3.11-slim

WORKDIR /app

# 配置国内 PyPI 镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 5000

# 启动应用（使用单 worker 避免初始化冲突）
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "run:app"]
