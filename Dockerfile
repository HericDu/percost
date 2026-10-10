# ---------- 阶段 1：构建前端 ----------
FROM node:20-alpine AS frontend-build

WORKDIR /build

RUN npm config set registry https://registry.npmmirror.com

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


# ---------- 阶段 2：运行时（前端 + 后端同一进程） ----------
FROM python:3.11-slim

WORKDIR /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 后端代码
COPY backend/ ./

# 前端构建产物，由 Flask 直接托管
COPY --from=frontend-build /build/dist ./static

RUN mkdir -p /app/data

ENV FLASK_ENV=production \
    DATA_DIR=/app/data \
    FRONTEND_DIST=/app/static

EXPOSE 5000

# 单 worker 避免 SQLite 初始化冲突；多线程承载并发
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "8", "--timeout", "120", "run:app"]
