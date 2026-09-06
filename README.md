# MeowLog · 喵喵日记

[![CI](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml/badge.svg)](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Sinera-kiki/meowlog-ai-companion)

一款面向移动端的 AI 治愈系虚拟宠物游戏。玩家可以领养具有不同性格的猫咪，通过喂食、抚摸、玩耍和对话建立关系；猫咪拥有独立状态、长期记忆、双槽位换装和离线生活。

> 当前状态：作品集级全栈 MVP，已打通互动、AI 记忆、探险、手帐与奖励循环。

## 核心体验

- **AI 性格对话**：傲娇、黏人、哲学家、探险家等人格影响回复方式。
- **情感记忆**：记录玩家表达的重要事件和情绪，在后续对话中召回。
- **自主状态**：依据离线时间推演饱食度、心情和行为状态。
- **互动反馈**：喂鱼干、摸头、玩毛线球均有动画和数值变化。
- **森系换装**：服装与配饰双槽位，可收藏、解锁并持久保存。
- **移动端优先**：针对手机浏览器设计，桌面端以手机画布展示。

## 技术架构

```mermaid
flowchart LR
    UI[React + Vite H5] --> API[FastAPI]
    API --> DB[(PostgreSQL)]
    API --> LLM[OpenAI-compatible LLM]
    API --> SIM[Lazy Tick 状态推演]
    DB --> MEM[长期记忆 / 对话 / 穿搭]
```

| 层级 | 技术 |
| --- | --- |
| 前端 | React 18、TypeScript、Vite、CSS Animation |
| 后端 | FastAPI、Pydantic、HTTPX |
| 数据 | PostgreSQL、幂等 Schema 初始化 |
| AI | OpenAI-compatible Chat Completions API |
| 部署 | Docker、Docker Compose、Render Blueprint |
| 工程 | GitHub Actions CI |

## 本地运行

> 国内部署（阿里云/腾讯云）请看 [`deploy/README.md`](deploy/README.md)，或者直接在服务器上执行一条一键脚本。

### 方式一：Docker Compose（推荐）

```bash
cp .env.example .env
docker compose up --build
```

访问：`http://localhost:8000`

不填写 `LLM_API_KEY` 时，应用自动使用本地演示回复；填写后启用真实 AI 对话。

### 方式二：分别启动

1. 启动 PostgreSQL，并配置 `DATABASE_URL`。
2. 初始化数据库：

```bash
pip install -r backend/requirements.txt
python -m backend.init_db
```

3. 构建前端并启动后端：

```bash
cd frontend && npm ci && npm run build && cd ..
uvicorn backend.app:app --reload --port 8000
```

## 自动化验证

```bash
pip install -r backend/requirements-dev.txt
export DATABASE_URL=postgresql://meowlog:meowlog@localhost:5432/meowlog
python -m backend.init_db
pytest -q
```

GitHub Actions 会自动执行前端构建、数据库初始化、API 测试和 Docker 镜像构建。

## 环境变量

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `DATABASE_URL` | 是 | PostgreSQL 连接串 |
| `LLM_API_KEY` | 否 | 留空时使用演示回复 |
| `LLM_BASE_URL` | 否 | 默认 OpenAI，可替换为 DeepSeek 等兼容接口 |
| `LLM_MODEL` | 否 | 默认 `gpt-4o-mini` |
| `APP_PORT` | 否 | 默认 `8000` |

## 一键部署到 Render

仓库已包含 `render.yaml`：

1. 将仓库推送到 GitHub。
2. 在 Render 创建 Blueprint，选择本仓库。
3. 确认创建 Web Service 与 PostgreSQL。
4. 部署完成后获得公开访问地址；未配置密钥时使用内置演示回复。
5. 如需真实 AI，在 Render 服务的 Environment 中添加 `LLM_API_KEY`，并按需修改 `LLM_BASE_URL` 与 `LLM_MODEL`。

## 数据与隐私

- 浏览器首次访问会生成随机游客 ID，用于隔离猫咪和聊天数据。
- 密钥只通过环境变量注入，不提交到仓库。
- 当前游客模式适合作品演示，不等同于正式账号安全体系。

## 项目亮点

1. 用 **Lazy Tick** 替代高频后台轮询，在玩家上线时一次性结算离线状态。
2. 将人格、亲密度、历史记忆组合进 AI 上下文，使回复随关系变化。
3. 将游戏状态、记忆、对话和双槽位穿搭持久化到 PostgreSQL。
4. 单容器同时托管 API 与前端构建产物，降低个人项目部署复杂度。

## Roadmap

- [x] 领养、互动、状态持久化
- [x] AI 对话与初版情绪记忆
- [x] 双槽位换装和收藏
- [x] Docker、CI、公网配置适配
- [x] 探险—手帐—奖励闭环
- [x] 结构化记忆提取、相关性召回与删除管理
- [ ] AIGC 明信片图像与战利品图鉴
- [ ] 自动化 API 测试与错误监控

## License

MIT License © 2026 Deng Wanting.
