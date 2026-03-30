# Percost - 智能物品成本管理工具

科学计算已拥有物品的每日使用成本，做出理性消费决策。

## 功能特性

- 📦 **物品管理**: 添加、编辑、删除物品，支持 Emoji 图标分类
- 💰 **智能成本计算**: 根据使用频率自动计算每次成本，支持多种频率模式
- 📊 **数据统计**: 总物品数、总投资、平均每次成本、使用中物品数
- 🔍 **搜索筛选**: 按名称搜索、按分类筛选、多维度排序
- 🔐 **权限控制**: 未登录可浏览，登录后才能增删改
- 🎨 **液态玻璃 UI**: 现代化大圆角设计，液态玻璃毛玻璃视觉效果
- 📱 **响应式布局**: 完美适配手机和电脑
- 🐳 **一键部署**: Docker Compose 容器化部署

## 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- Tailwind CSS（液态玻璃设计系统）
- Pinia（状态管理）
- Vue Router
- Lucide Icons

### 后端
- Flask (Python)
- SQLite（数据库）
- SQLAlchemy（ORM）
- JWT（认证）

### 部署
- Docker + Docker Compose
- Nginx（反向代理 + 静态文件服务）
- EdgeOne Pages（前端静态托管，可选）

## 快速开始

### 方式一：使用启动脚本（推荐）

```bash
# 1. 给脚本添加执行权限（首次运行）
chmod +x start.sh clean.sh

# 2. 启动服务
./start.sh
```

启动脚本会自动：
- ✅ 检查 Docker 是否运行
- ✅ 创建环境配置文件
- ✅ 构建并启动所有服务
- ✅ 显示访问地址和默认账号

### 方式二：手动启动

#### 1. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```

#### 2. 启动服务

```bash
docker-compose up -d
```

#### 3. 访问应用

打开浏览器访问：**http://localhost:12800**

**默认管理员账号：**
- 用户名：`admin`
- 密码：`admin123`（或您在 `.env` 中设置的密码）

## 使用频率计算规则

| 模式 | 计算公式 |
|------|---------|
| 每天 | 总使用次数 = 持有天数 × 每日次数 |
| 每周 | 总使用次数 = (持有天数 / 7) × 每周次数 |
| 每月 | 总使用次数 = (持有天数 / 30) × 每月次数 |
| 每年 | 总使用次数 = (持有天数 / 365) × 每年次数 |
| 手动录入 | 通过 +/- 按钮累计记录 |

> 每次成本 = (购买金额 + 额外成本 - 处置价格) / 总使用次数

## 成本分级

| 等级 | 条件 | 颜色标识 |
|------|------|---------|
| 🟢 低成本 | 每次成本 < ¥10 | 绿色 |
| 🟡 中成本 | ¥10 ≤ 每次成本 < ¥50 | 黄色 |
| 🔴 高成本 | 每次成本 ≥ ¥50 | 红色 |

## 目录结构

```
Percost/
├── frontend/                # Vue 3 前端项目
│   ├── src/
│   │   ├── api/             # API 调用层
│   │   ├── components/      # 核心组件
│   │   │   ├── AddItemModal.vue   # 添加/编辑物品弹窗
│   │   │   └── ItemCard.vue       # 物品卡片组件
│   │   ├── views/           # 页面视图
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── data/            # 静态数据（Emoji 分类等）
│   │   ├── router/          # 路由配置
│   │   ├── types/           # TypeScript 类型定义
│   │   ├── utils/           # 工具函数
│   │   ├── App.vue          # 根组件
│   │   └── index.css        # 全局样式（液态玻璃设计系统）
│   ├── Dockerfile
│   └── package.json
├── backend/                 # Flask 后端项目
│   ├── app/
│   │   ├── models.py        # 数据模型
│   │   ├── routes/          # API 路由
│   │   └── utils/           # 工具函数
│   ├── config.py
│   ├── run.py
│   ├── Dockerfile
│   └── requirements.txt
├── nginx/
│   └── nginx.conf           # Nginx 配置
├── data/                    # 数据持久化目录
├── docker-compose.yml       # Docker Compose 配置
├── .env.example             # 环境变量示例
├── start.sh                 # 快速启动脚本
├── clean.sh                 # 清理脚本
└── README.md
```

## API 文档

### 认证 API

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/auth/login` | 用户登录 | 否 |
| POST | `/api/auth/logout` | 用户登出 | 是 |
| GET | `/api/auth/verify` | 验证 Token | 是 |

### 物品 API

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/items` | 获取所有物品 | 否 |
| POST | `/api/items` | 创建物品 | 是 |
| GET | `/api/items/:id` | 获取单个物品 | 否 |
| PUT | `/api/items/:id` | 更新物品 | 是 |
| DELETE | `/api/items/:id` | 删除物品 | 是 |
| POST | `/api/items/:id/usage` | 记录使用次数 | 是 |

## 常用命令

| 操作 | 命令 |
|------|------|
| 启动服务 | `./start.sh` 或 `docker-compose up -d` |
| 停止服务 | `docker-compose down` |
| 查看日志 | `docker-compose logs -f` |
| 查看服务状态 | `docker-compose ps` |
| 重启服务 | `docker-compose restart` |
| 清理并重建 | `./clean.sh` |

## 数据持久化

数据存储在 `./data` 目录中：
- `percost.db`: SQLite 数据库文件

**备份数据库：**
```bash
cp data/percost.db data/percost.db.backup
tar -czf percost-backup-$(date +%Y%m%d).tar.gz data/
```

## 开发环境

### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

后端运行在：http://localhost:5000

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

前端运行在：http://localhost:3000

## 生产部署建议

1. **修改敏感信息**
   - 修改 `.env` 中的管理员密码
   - 修改 `JWT_SECRET_KEY` 为随机字符串

2. **配置 HTTPS**
   - 使用 Nginx + Let's Encrypt
   - 或通过腾讯云 EdgeOne 配置 CDN + SSL

3. **定期备份数据**
   ```bash
   # 添加到 crontab
   0 2 * * * cd /path/to/Percost && tar -czf backup-$(date +\%Y\%m\%d).tar.gz data/
   ```

4. **监控服务状态**
   - 使用 Docker 的健康检查
   - 配置日志监控

## 常见问题

### 端口被占用怎么办？

修改 `docker-compose.yml` 中的端口映射：

```yaml
services:
  frontend:
    ports:
      - "你的端口:80"  # 默认是 12800:80
```

### 如何修改管理员密码？

编辑 `.env` 文件，然后重启服务：

```bash
docker-compose down
rm -rf data/percost.db  # 删除旧数据库（会清空所有数据）
docker-compose up -d
```

### 构建失败怎么办？

```bash
./clean.sh
docker-compose build --no-cache
docker-compose up -d
```

## 许可证

MIT License

---

&copy; 2025 - 2027 By HericDu
