# MeowLog · 喵喵日记

[![CI](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml/badge.svg)](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-718263.svg)](LICENSE)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](frontend)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](backend)

**一只有自己生活、会记住你的心事，也会带着故事回家的 AI 伴侣猫。**

MeowLog 是面向移动端的治愈系虚拟宠物游戏。它将放置养成、AI 长期记忆、自主状态模拟与轻量游戏经济结合，让虚拟宠物不只是等待指令的聊天框，而是一个拥有性格、关系和生活轨迹的角色。

- 在线体验：http://154.8.153.135:8000
- 一键部署：[Render Blueprint](https://render.com/deploy?repo=https://github.com/Sinera-kiki/meowlog-ai-companion)
- 产品案例：[docs/PRODUCT_CASE_STUDY.md](docs/PRODUCT_CASE_STUDY.md)
- 系统架构：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 游戏与经济设计：[docs/GAME_DESIGN.md](docs/GAME_DESIGN.md)

> 当前状态：作品集级全栈 MVP。核心闭环、部署链路和自动化测试已经跑通。

---

## 为什么做它

传统虚拟宠物有养成感，但无法理解玩家；AI 聊天产品能对话，却通常缺乏持续目标和游戏反馈。

MeowLog 尝试连接二者：

| 用户需求 | 产品解法 |
| --- | --- |
| 希望被倾听，而非每次重新介绍自己 | 结构化长期记忆与相关性召回 |
| 希望宠物像“活着”，而不是等待点击 | 离线状态推演、探险和随机事件 |
| 希望长期使用有目标 | 亲密等级、每日任务、叶子币、商店与收藏 |
| 希望情绪陪伴不沉重 | 猫咪人格、短对话、动作反馈与治愈系视觉 |

## 30 秒体验路线

1. 进入森林初遇页，命名并选择猫咪人格。
2. 喂鱼干、摸头或玩毛线球，观察状态和亲密度变化。
3. 完成每日陪伴任务并领取叶子币。
4. 在商店购买服装，回衣橱组合“服装 + 配饰”双槽穿搭。
5. 派猫咪外出探险，等待它带回手帐、礼物和叶子币。
6. 向猫咪讲述偏好或烦恼，再从“回忆”中查看它保存的长期记忆。

## 核心游戏循环

```mermaid
flowchart LR
    A[每日互动] --> B[亲密度 / 任务进度]
    B --> C[领取叶子币]
    C --> D[商店购买服装]
    D --> E[双槽穿搭与收藏]
    B --> F[外出探险]
    F --> G[AI 手帐 / 战利品]
    G --> C
    A --> H[情绪与偏好记忆]
    H --> I[后续对话自然召回]
    I --> A
```

## 已实现能力

### 游戏体验

- 六种人格领养与森林绘本式新手流程
- 饱食、心情、亲密度与离线状态推演
- 喂食、抚摸、玩耍动画；Web Audio 与移动端震动反馈
- 每日签到与四类陪伴任务
- 叶子币奖励、商店购买、等级限制和资产持久化
- 服装 / 配饰双槽位、收藏与试穿
- 探险倒计时、AI 手帐、战利品和奖励结算

### AI 与记忆

- OpenAI-compatible API，支持 OpenAI、DeepSeek 等服务
- 人格、亲密度与记忆共同构建对话上下文
- 对偏好、事件、情绪和目标进行结构化提取
- 基于文本相关性和记忆重要度召回，而非简单拼接全部历史
- 用户可查看和删除长期记忆
- 未配置 Key 时自动进入可演示的离线回复模式

### 工程能力

- React 18 + TypeScript + Vite 移动端 SPA
- FastAPI + PostgreSQL 单服务架构
- Docker / Docker Compose 一键运行
- Render Blueprint 与国内云服务器自动部署脚本
- GitHub Actions：前端构建、数据库初始化、API 测试、Docker 构建
- 游客 ID 数据隔离；密钥通过环境变量注入

## 系统架构

```mermaid
flowchart TB
    Browser[Mobile Web · React] -->|X-Guest-Id| API[FastAPI API]
    API --> Cat[Cat State / Lazy Tick]
    API --> Game[Quest / Shop / Adventure]
    API --> Memory[Memory Extractor & Retriever]
    API --> LLM[OpenAI-compatible LLM]
    Cat --> PG[(PostgreSQL)]
    Game --> PG
    Memory --> PG
    API --> Static[Vite Static Assets]
```

| 层级 | 技术与职责 |
| --- | --- |
| 前端 | React、TypeScript、CSS Animation；移动端场景、换装、任务、手帐与聊天 |
| 后端 | FastAPI、Pydantic；状态机、经济系统、AI 编排与接口校验 |
| 数据 | PostgreSQL；猫咪、记忆、对话、探险、资产与每日进度 |
| AI | OpenAI-compatible Chat Completions；人格回复、记忆萃取、探险叙事 |
| 运维 | Docker Compose、Render、腾讯云/阿里云脚本、GitHub Actions |

## 关键设计取舍

### 1. Lazy Tick，而非持续后台轮询

服务器只记录 `last_interact_time`。玩家再次上线时，根据离线时长一次性结算饱食度、心情和行为，既营造“宠物独立生活”的感觉，又避免持续任务消耗资源。

### 2. 结构化记忆，而非无限堆聊天记录

只萃取值得长期保存的信息，再依据当前问题的文本相关性、重要度与访问次数召回。这样能够控制 Token 成本，也让记忆使用更可解释。

### 3. 单容器交付

FastAPI 同时提供 API 和静态前端，个人项目只需维护一个 Docker 服务和一个 PostgreSQL，降低部署与排障成本。

### 4. 演示模式与真实 AI 解耦

不配置 API Key 也可以完整体验游戏流程；填写 Key 后无缝开启真实 AI，避免作品因密钥或额度问题完全不可用。

## 快速开始

### Docker Compose（推荐）

```bash
cp .env.example .env
docker compose up --build
```

访问 `http://localhost:8000`。

### 本地开发

```bash
# PostgreSQL 准备完成后
pip install -r backend/requirements-dev.txt
export DATABASE_URL=postgresql://meowlog:meowlog@localhost:5432/meowlog
python -m backend.init_db

cd frontend && npm ci && npm run build && cd ..
uvicorn backend.app:app --reload --port 8000
```

## 配置

| 环境变量 | 必填 | 默认值 / 说明 |
| --- | --- | --- |
| `DATABASE_URL` | 是 | PostgreSQL 连接串 |
| `LLM_API_KEY` | 否 | 留空启用离线演示回复 |
| `LLM_BASE_URL` | 否 | `https://api.openai.com/v1` |
| `LLM_MODEL` | 否 | `gpt-4o-mini` |
| `ADVENTURE_DURATION_SECONDS` | 否 | `45`，演示环境探险时长 |

DeepSeek 示例：

```env
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
LLM_API_KEY=your-key
```

## 部署

### 国内云服务器

参见 [deploy/README.md](deploy/README.md)。Ubuntu 服务器可执行：

```bash
curl -fsSL https://raw.githubusercontent.com/Sinera-kiki/meowlog-ai-companion/main/deploy/install.sh | sudo bash
```

### Render

点击页面顶部的 **Deploy to Render**，Blueprint 会创建 Web Service 与 PostgreSQL。

## 测试与质量门禁

```bash
pip install -r backend/requirements-dev.txt
python -m backend.init_db
pytest -q
```

CI 每次提交自动执行：

1. npm 依赖锁定安装与前端构建
2. PostgreSQL 容器健康检查与幂等建表
3. 领养、互动、任务、商店、换装、探险和记忆 API 测试
4. Docker 镜像构建

## 目录结构

```text
meowlog-ai-companion/
├── frontend/            # React 移动端游戏
├── backend/             # FastAPI、AI 编排、数据库逻辑
├── tests/               # API 与核心算法测试
├── deploy/              # 国内云服务器一键部署
├── docs/                # 产品、架构和游戏设计文档
├── Dockerfile
├── docker-compose.yml
└── render.yaml
```

## 当前边界与下一步

- AIGC 明信片目前采用生成故事 + 程序化卡片，后续可接图像模型。
- 游客 ID 适合作品演示，正式产品需升级为账号体系与跨设备同步。
- 后续计划增加更多房间、季节天气、互动小游戏和主动通知。

## License

MIT License © 2026 Deng Wanting.
