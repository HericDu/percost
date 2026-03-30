#!/bin/bash

# Percost 快速启动脚本

echo "==================================="
echo "  Percost 智能物品成本管理工具"
echo "==================================="
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker Desktop"
    exit 1
fi

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "📝 创建环境配置文件..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件（使用默认配置）"
    echo ""
fi

echo "🚀 正在启动服务..."
echo ""

# 启动 Docker Compose
docker-compose up -d --build

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ 服务启动成功！"
    echo ""
    echo "📱 访问地址：http://localhost:12800"
    echo ""
    echo "👤 默认管理员账号："
    echo "   用户名：admin"
    echo "   密码：admin123"
    echo ""
    echo "💡 提示："
    echo "   - 数据保存在 ./data 目录中"
    echo "   - 停止服务：docker-compose down"
    echo "   - 查看日志：docker-compose logs -f"
    echo ""
else
    echo ""
    echo "❌ 服务启动失败，请检查日志："
    echo "   docker-compose logs"
fi
