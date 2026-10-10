#!/bin/bash
# Percost 本地开发启动脚本（不使用 Docker）
# 后端 Flask :5000 + 前端 Vite :3000（Vite 已配置 /api 代理到 5000）

set -e
cd "$(dirname "$0")"
ROOT=$(pwd)

case "${1:-start}" in
  stop)
    pkill -f "Percost/backend/run.py" 2>/dev/null && echo "后端已停止" || echo "后端未运行"
    pkill -f "Percost/frontend.*vite" 2>/dev/null && echo "前端已停止" || echo "前端未运行"
    exit 0
    ;;
  restart)
    "$0" stop; sleep 1
    ;;
esac

# ---- 后端 ----
cd "$ROOT/backend"
if [ ! -d .venv ]; then
  echo "创建 Python 虚拟环境..."
  python3 -m venv .venv
  .venv/bin/pip install -q --upgrade pip
  .venv/bin/pip install -q -r requirements.txt
fi

# 本地开发时移除静态产物，避免覆盖 Vite 热更新
[ -d static ] && rm -rf static

if [ -f "$ROOT/.env" ]; then
  set -a; source "$ROOT/.env"; set +a
fi

pkill -f "Percost/backend/run.py" 2>/dev/null || true
nohup .venv/bin/python run.py > /tmp/percost-backend.log 2>&1 &
echo "后端启动中 -> http://localhost:5000  (日志: /tmp/percost-backend.log)"

# ---- 前端 ----
cd "$ROOT/frontend"
[ -d node_modules ] || npm install

pkill -f "Percost/frontend.*vite" 2>/dev/null || true
nohup npm run dev > /tmp/percost-frontend.log 2>&1 &
echo "前端启动中 -> http://localhost:3000  (日志: /tmp/percost-frontend.log)"

sleep 5
echo ""
echo "后端 /api/items : $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5000/api/items)"
echo "前端首页        : $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000/)"
echo ""
echo "访问 http://localhost:3000   账号 admin / admin123"
echo "停止：./dev.sh stop"
