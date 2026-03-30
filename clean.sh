#!/bin/bash

echo "🧹 清理旧的构建文件..."

# 停止服务
docker-compose down 2>/dev/null

# 删除旧镜像
docker rmi percost-frontend percost-backend 2>/dev/null

# 清理 Docker 缓存
docker builder prune -f

# 删除前端 node_modules 和 dist（如果存在）
if [ -d "frontend/node_modules" ]; then
    echo "删除 frontend/node_modules..."
    rm -rf frontend/node_modules
fi

if [ -d "frontend/dist" ]; then
    echo "删除 frontend/dist..."
    rm -rf frontend/dist
fi

# 删除后端虚拟环境（如果存在）
if [ -d "backend/venv" ]; then
    echo "删除 backend/venv..."
    rm -rf backend/venv
fi

# 删除数据库文件（可选）
# read -p "是否删除数据库文件？(y/N) " -n 1 -r
# echo
# if [[ $REPLY =~ ^[Yy]$ ]]; then
#     rm -rf data/percost.db
# fi

echo "✅ 清理完成！"
echo ""
echo "现在可以运行: ./start.sh"
