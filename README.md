# Percost — 物品成本管理工具

算清每件东西的真实成本，让「值不值」有据可依。

买入价只是开始。一副用了 200 次的耳机和一件穿了 3 次的外套，哪个更值？
Percost 把购入价、额外投入、处置残值和实际使用频率放在一起算，给出**每次使用花费**这个唯一可横向对比的指标。

---

## 功能

| 能力 | 说明 |
|---|---|
| 成本核算 | 支持日/周/月/年自动推算与手动计数五种频率模式 |
| 档位着色 | 按每次花费自动分级配色，扫一眼即可分辨优劣 |
| 数据概览 | 记录件数、累计花费、件均价格、在用件数 |
| 检索排序 | 名称搜索、分类筛选、8 种排序（按结果描述，非字段名） |
| 权限分离 | 未登录可浏览全部数据，登录后方可增删改 |
| 自适应分页 | 每页数量随视窗尺寸自动计算，无需手动设置 |
| 响应式 | 从 414px 手机到 2K 桌面均为同一套布局逻辑 |

界面采用液态玻璃材质与动态光斑背景，信息层级参照地铁导向标识的分层原则设计。

---

## 技术栈

**前端** — Vue 3 · TypeScript · Vite 5 · Tailwind CSS 3 · Pinia · Vue Router · Lucide Icons

**后端** — Flask 3 · SQLAlchemy 2 · SQLite · PyJWT · bcrypt · Gunicorn

**部署** — Docker 单容器（多阶段构建）

> **架构说明**：前端构建产物由 Flask 直接托管，不使用 nginx。
> 整个应用是**一个容器、一个进程**，无需自定义网络，部署面板里也只有一个条目。

---

## 快速开始

### 方式一：Docker 部署（推荐）

适合服务器部署、长期运行。

**1. 准备环境变量**

```bash
cp .env.example .env
```

编辑 `.env`，**生产环境务必修改以下两项**：

```env
ADMIN_PASSWORD=替换为你的密码
JWT_SECRET_KEY=替换为随机字符串
```

生成随机密钥：

```bash
openssl rand -hex 32
```

**2. 启动**

```bash
docker compose up -d --build
```

或使用脚本（会自动检查 Docker 状态、创建 `.env`）：

```bash
chmod +x start.sh && ./start.sh
```

**3. 访问**

- 前台（公开浏览）：<http://localhost:12800>
- 管理后台：<http://localhost:12800/你设置的-ADMIN_PATH>

默认账号 `admin` / `admin123`（或你在 `.env` 中设置的密码）。

---

### 方式二：npm 本地开发

适合改代码、调样式，**前端带热更新**。

**环境要求**：Node.js ≥ 18、Python ≥ 3.9

**一键启动**

```bash
chmod +x dev.sh && ./dev.sh
```

脚本会自动创建 Python 虚拟环境、安装前后端依赖、加载 `.env` 并拉起两个服务：

| 服务 | 地址 | 说明 |
|---|---|---|
| 前端 | <http://localhost:3000> | Vite dev server，**开发请访问这个** |
| 后端 | <http://localhost:5000> | Flask，`/api` 由 Vite 自动代理 |

```bash
./dev.sh stop      # 停止
./dev.sh restart   # 重启
```

日志位于 `/tmp/percost-backend.log` 与 `/tmp/percost-frontend.log`。

<details>
<summary>手动启动（不使用脚本）</summary>

```bash
# 后端
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
set -a && source ../.env && set +a
.venv/bin/python run.py

# 前端（另开终端）
cd frontend
npm install
npm run dev
```

</details>

> **注意**：`dev.sh` 启动时会删除 `backend/static` 目录。
> 该目录是单容器构建的前端产物，若残留会覆盖 Vite 的热更新。

---

## 计算规则

**每次使用花费 = (购买金额 + 额外成本 − 处置价格) ÷ 总使用次数**

总使用次数按所选频率模式推算：

| 模式 | 公式 |
|---|---|
| 每天 | 持有天数 × 每日次数 |
| 每周 | ⌊持有天数 ÷ 7⌋ × 每周次数 |
| 每月 | ⌊持有天数 ÷ 30⌋ × 每月次数 |
| 每年 | ⌊持有天数 ÷ 365⌋ × 每年次数 |
| 手动录入 | 通过卡片上的 `−` / `+` 按钮累计 |

> 已填写「使用截止日期」的物品，持有天数截止到该日期，不再继续累加。

### 档位配色

| 档位 | 区间 | 颜色 |
|---|---|---|
| 划算 | < ¥10 | 绿 |
| 一般 | ¥10 – ¥50 | 琥珀 |
| 偏贵 | ≥ ¥50 | 红 |

---

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `ADMIN_USERNAME` | `admin` | 管理员用户名 |
| `ADMIN_PASSWORD` | `admin123` | 管理员密码，**生产环境必改** |
| `ADMIN_PATH` | `login` | 管理后台入口路径，**公网部署建议改为随机值** |
| `JWT_SECRET_KEY` | 占位字符串 | Token 签名密钥，**生产环境必改** |
| `TOKEN_EXPIRE_DAYS` | `7` | 登录有效期（天） |
| `CORS_ORIGINS` | `http://localhost:12800` | 跨域白名单，单容器部署下同源，一般无需放开 |
| `DATA_DIR` | 容器内 `/app/data` | 数据目录 |
| `DATABASE_URL` | SQLite | 可替换为其他 SQLAlchemy 连接串 |

`.env` 已在 `.gitignore` 中，不会进入版本库。**新服务器上需要手动创建。**

---

## 访问控制

前台完全公开，任何人都能浏览物品与成本数据；**增删改一律需要登录**。

### 隐藏式后台入口

登录页不在固定的 `/login`，而是由 `ADMIN_PATH` 决定：

```env
ADMIN_PATH=k7m2x9p4q1
```

访问 `https://域名/k7m2x9p4q1` 才会出现登录表单，其余任何路径都返回 404。

生成随机路径：

```bash
openssl rand -hex 12
```

实现上有三点保证路径不被轻易发现：

1. **路径不下发前端** — 构建产物里不含该值，读 JS 也拿不到。浏览器只能把候选路径提交给 `/api/auth/gate`，由服务端比对
2. **常量时间比较** — 使用 `hmac.compare_digest`，无法通过响应耗时逐字符推断
3. **探测限流** — 同一 IP 5 分钟内最多 10 次探测，超限返回 429

未登录状态下，页面上不存在任何指向后台的按钮或链接。

### 登录爆破防护

同一 IP 连续 8 次密码错误后锁定 15 分钟，登录成功即清零。

> ⚠️ **务必理解**：隐藏路径属于 security through obscurity，它只能**降低被自动化扫描批量命中的概率**，不构成真正的访问控制。
> 一旦路径泄露（如浏览器历史、Referer、他人代操作），唯一的防线就是密码。
> **因此 `ADMIN_PASSWORD` 仍然必须设置为强密码，`JWT_SECRET_KEY` 必须随机。**

### 已知限制

- 限流状态存于单进程内存，仅适用于当前的 `gunicorn --workers 1` 配置。若扩为多 worker 或多实例，需改用 Redis 等共享存储
- 容器重启会清空限流计数
- `X-Forwarded-For` 可被伪造，仅在部署于可信反向代理之后时才可靠

---

## 数据与备份

全部数据存于 **`data/percost.db`** 一个 SQLite 文件中，`docker-compose.yml` 已挂载 `./data`。

> 物品图片以 base64 存于数据库，不落盘。除 `./data` 外**无其他需要挂载的目录**。

```bash
# 备份
cp data/percost.db data/percost.db.$(date +%Y%m%d).bak

# 打包备份
tar -czf percost-backup-$(date +%Y%m%d).tar.gz data/

# 定时备份（crontab，每日 02:00）
0 2 * * * cd /path/to/Percost && tar -czf backup-$(date +\%Y\%m\%d).tar.gz data/
```

---

## API

所有接口以 `/api` 为前缀，认证通过 `Authorization: Bearer <token>` 请求头。

### 认证

| 方法 | 路径 | 说明 | 需认证 |
|---|---|---|---|
| POST | `/api/auth/gate` | 校验后台入口路径，错误返回 404 | — |
| POST | `/api/auth/login` | 登录，返回 token | — |
| POST | `/api/auth/logout` | 登出 | ✓ |
| GET | `/api/auth/verify` | 校验 token 有效性 | ✓ |
| GET | `/api/auth/user` | 获取当前用户信息 | ✓ |

### 物品

| 方法 | 路径 | 说明 | 需认证 |
|---|---|---|---|
| GET | `/api/items` | 物品列表 | — |
| GET | `/api/items/:id` | 单个物品 | — |
| POST | `/api/items` | 新建 | ✓ |
| PUT | `/api/items/:id` | 更新 | ✓ |
| DELETE | `/api/items/:id` | 删除 | ✓ |
| POST | `/api/items/:id/usage` | 手动增减使用次数 | ✓ |
| POST | `/api/items/:id/images` | 上传图片（最多 3 张，单张 ≤ 5MB） | ✓ |
| DELETE | `/api/items/images/:id` | 删除图片 | ✓ |

---

## 常用命令

| 操作 | 命令 |
|---|---|
| 启动 | `docker compose up -d` |
| 构建并启动 | `docker compose up -d --build` |
| 停止 | `docker compose down` |
| 查看日志 | `docker compose logs -f` |
| 查看状态 | `docker compose ps` |
| 重启 | `docker compose restart` |
| 彻底清理重建 | `./clean.sh && docker compose up -d --build` |
| 本地开发 | `./dev.sh` |

---

## 目录结构

```
Percost/
├── Dockerfile               # 多阶段构建：node 编译前端 → Python 运行时
├── docker-compose.yml       # 单服务配置
├── dev.sh                   # 本地开发启停脚本
├── start.sh / clean.sh      # Docker 启动 / 清理脚本
├── .env.example             # 环境变量模板
├── data/                    # 数据持久化（已挂载，不入库）
│   └── percost.db
├── backend/
│   ├── app/
│   │   ├── __init__.py      # 应用工厂 + SPA 静态托管
│   │   ├── models.py        # User / Item / ItemImage
│   │   ├── routes/          # auth.py · items.py
│   │   └── utils/           # 认证、校验、时间工具
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/             # axios 封装与接口定义
    │   ├── components/
    │   │   ├── ItemCard.vue       # 物品卡片
    │   │   ├── AddItemModal.vue   # 新增/编辑弹窗
    │   │   └── PaginationBar.vue  # 分页
    │   ├── composables/
    │   │   └── useResponsivePageSize.ts  # 视窗自适应分页
    │   ├── views/           # ItemsView · LoginView
    │   ├── stores/          # Pinia
    │   ├── data/            # Emoji 分类数据（337 个）
    │   ├── index.css        # 设计令牌 + 液态玻璃材质
    │   └── App.vue
    ├── tailwind.config.js   # 圆角比例尺、ink 中性色
    └── package.json
```

---

## 生产部署建议

1. **改掉默认凭据** — `ADMIN_PASSWORD` 与 `JWT_SECRET_KEY` 必须替换，否则等同裸奔
2. **设置随机后台入口** — `ADMIN_PATH` 改为 `openssl rand -hex 12` 生成的随机值
3. **收紧 CORS** — 单容器下前后端同源，`CORS_ORIGINS` 设为实际访问域名即可
4. **配置 HTTPS** — 在前置网关（Nginx / Caddy / 云厂商负载均衡）终止 TLS。
   注意：未加密传输时后台路径会以明文出现在链路中
5. **定期备份** — 见上文 crontab 示例
6. **反向代理** — 若前置 Nginx，将 `/` 整体转发至容器 `5000` 端口，无需按路径分流

---

## 常见问题

<details>
<summary>端口 12800 被占用</summary>

修改 `docker-compose.yml` 的端口映射左侧：

```yaml
ports:
  - "你的端口:5000"
```

</details>

<details>
<summary>忘记后台入口路径</summary>

查看服务器上的 `.env` 文件：

```bash
grep ADMIN_PATH .env
```

改完需重启容器生效：`docker compose up -d`（无需重新构建）。

</details>

<details>
<summary>登录被锁定（429）</summary>

同一 IP 连续 8 次密码错误会锁定 15 分钟。等待窗口结束即可，或重启容器立即清空计数：

```bash
docker compose restart
```

</details>

<details>
<summary>忘记管理员密码</summary>

管理员账号在数据库首次初始化时写入，改 `.env` 不会影响已有账号。需要删库重建：

```bash
docker compose down
rm data/percost.db          # 会清空所有数据，请先备份
docker compose up -d
```

</details>

<details>
<summary>构建失败 / 改动不生效</summary>

```bash
./clean.sh
docker compose build --no-cache
docker compose up -d
```

</details>

<details>
<summary>本地开发时页面空白或样式错乱</summary>

多半是 `backend/static` 残留覆盖了 Vite 产物。执行 `./dev.sh restart`，脚本会自动清理。

</details>

<details>
<summary>浏览器兼容性</summary>

界面使用了 `oklch()`、`color-mix()`、`mask-composite` 等较新特性，需要：

- Chrome / Edge ≥ 111
- Safari ≥ 16.4
- Firefox ≥ 113

</details>

---

## 许可证

MIT License

&copy; 2025 - 2027 By HericDu
