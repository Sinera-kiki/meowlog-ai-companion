# MeowLog · 喵喵日记 🐾

> **基于自主智能体与长效记忆的 AI 治愈系伴侣猫**
> 一只有自己生活、会记住你的心事，也会带着故事回家的虚拟宠物。

[![CI](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml/badge.svg)](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-718263.svg)](LICENSE)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**[🌐 在线体验公网 Demo](http://154.8.153.135:8000)** · **[📖 产品案例深度剖析](docs/PRODUCT_CASE_STUDY.md)** · **[🏗️ 系统架构设计](docs/ARCHITECTURE.md)** · **[🎮 游戏与经济设计](docs/GAME_DESIGN.md)**

---

## 📱 产品演示

<table>
  <tr>
    <td width="25%" align="center">
      <img src="docs/screenshots/onboarding.png" alt="森林初遇与人格领养" width="100%" />
      <br />
      <sub><b>1. 森林绘本领养 · 六维人格定制</b></sub>
    </td>
    <td width="25%" align="center">
      <img src="docs/screenshots/home-room.png" alt="森系小屋与生命感互动" width="100%" />
      <br />
      <sub><b>2. 森系小屋 · 触感与动画反馈</b></sub>
    </td>
    <td width="25%" align="center">
      <img src="docs/screenshots/wardrobe-shop.png" alt="双槽位换装与叶子币商店" width="100%" />
      <br />
      <sub><b>3. 暖暖式衣橱 · 经济与装扮系统</b></sub>
    </td>
    <td width="25%" align="center">
      <img src="docs/screenshots/journal-memory.png" alt="探险手帐与长期记忆抽屉" width="100%" />
      <br />
      <sub><b>4. 离线探险 · 叙事手帐与长效记忆</b></sub>
    </td>
  </tr>
</table>

---

## 🎯 产品背景：不是再做一个聊天框

传统虚拟宠物（如电子鸡、猫咪后院）具备陪伴感与收集乐趣，但**交互死板、无法真正理解玩家**；而主流 AI 聊天伴侣虽然能对话，却通常存在以下痛点：

- **记忆断层与角色失真**：每次打开像重新认识，无法沉淀长期关系；
- **缺乏游戏目标**：纯文字聊天容易产生疲劳感，用户缺乏持续打开的动力；
- **被动等待与工具感**：NPC 缺乏自主生活，始终是被动应答的“问答机器”；
- **情绪负担过重**：许多陪伴类产品对话沉重，缺乏轻松治愈的解压体验。

因此，本项目将问题重新定义为：

> **通过“自主状态推演（Lazy Tick）+ 结构化长期记忆（RAG）+ 轻量成长经济（Quest-Shop-Gacha）”，打造一个兼具角色深度与游戏可玩性的 AI 伴侣智能体。**

---

## 🧩 核心机制与闭环设计

```mermaid
flowchart LR
    subgraph CoreLoop["🎮 核心游戏循环 (Game Loop)"]
        A[每日陪伴互动\n喂食 · 抚摸 · 玩耍 · 倾诉] --> B[任务进度 & 签到]
        B --> C[获取叶子币 🍃]
        C --> D[森林商店购买服饰]
        D --> E[暖暖式双槽换装 & 收藏]
        A --> F[提升亲密度 Lv]
        F --> G[解锁高阶探险 & 稀有装扮]
        G --> H[派遣离线探险]
        H --> I[生成 AI 探险手帐 & 战利品]
        I --> C
    end

    subgraph MemoryLoop["🧠 情感与认知循环 (AI Memory Loop)"]
        A --> J[自然语言对话]
        J --> K[异步结构化记忆萃取\nPreference · Event · Emotion]
        K --> L[(PostgreSQL 长期记忆库)]
        L --> M[Top-K 相关性 & 重要度检索]
        M --> N[动态注入 System Prompt]
        N --> J
    end
```

### 1. 森林绘本领养与个性化人格（Onboarding）
- **六维人格设定**：傲娇猫猫、黏人甜心、哲学发呆猫、神经质探险家、吃货摆烂猫、护短大佬猫；
- **开箱即用新手资产**：领养即送 4 件新手装（赤豆围巾、林间雏菊、苔藓斗篷、野餐围裙）与 30 叶子币，零门槛体验双槽换装。

### 2. 状态机与离线自主生活（Lazy Tick Engine）
- 小猫拥有饱食度、心情值、亲密度与实时状态；
- **离线推演**：根据上次互动时间差，一次性演算离线期间的生活轨迹（觅食、睡觉、打工、探险），避免后台高频轮询消耗算力。

### 3. 双槽位森系换装系统（Nikki-Style Wardrobe）
- **独立槽位**：服装槽（斗篷/雨衣/针织衫/礼服）与配饰槽（围巾/帽子/挎包/领结）自由叠穿并持久化存储；
- **单品收藏**：支持一键点亮爱心收藏，在收藏页集中查看与管理。

### 4. 探险手帐与 AIGC 叙事（Adventure Journal）
- 派遣小猫外出探险（支持倒计时推演），归来自动结合猫咪人格与目的地生成 **80~120 字第一人称探险故事**，并带回战利品与明信片。

### 5. 记忆沉淀与可解释管理（Memory Drawer）
- 自动提取偏好、事件与情绪，并在聊天抽屉中提供专属“回忆”入口，用户可透明查看或随时删除不想保留的记忆。

---

## 🏗️ 全栈系统架构

```mermaid
flowchart TB
    subgraph Client["📱 客户端 (React 18 + TypeScript + Vite)"]
        UI[森系房间 · 绘本领养 · 双槽衣橱 · 探险手帐 · 聊天抽屉]
        Sensory[Web Audio 提示音 & Vibration 触觉反馈]
        Guest[Guest UUID 游客隔离会话]
    end

    subgraph Server["⚡ 业务与状态层 (FastAPI)"]
        Router[RESTful API 路由]
        Auth[X-Guest-Id 游客中间件 / SSO]
        StateEngine[Lazy Tick 离线推演状态机]
        QuestEngine[签到 · 任务 · 商店原子结算]
        AdventureEngine[探险调度 & 故事生成器]
        MemoryEngine[结构化记忆萃取 & 相关性检索器]
    end

    subgraph Storage["💾 持久化存储 (PostgreSQL 16)"]
        CatsTable[(cats 表: 状态 · 货币 · 资产 · 穿搭)]
        MemsTable[(memories 表: 记忆 · 情绪 · 重要度)]
        LogsTable[(chat_logs 表: 对话流)]
        AdvTable[(adventures 表: 探险 · 手帐 · 战利品)]
    end

    subgraph LLM["🤖 大模型推理层 (OpenAI-compatible)"]
        ChatModel[DeepSeek / OpenAI / Qwen 文本推理]
    end

    UI --> Auth
    Auth --> Router
    Router --> StateEngine --> CatsTable
    Router --> QuestEngine --> CatsTable
    Router --> AdventureEngine --> AdvTable
    Router --> MemoryEngine --> MemsTable
    AdventureEngine --> ChatModel
    MemoryEngine --> ChatModel
```

---

## 💡 关键技术难点与工程取舍

### 1. 状态模拟：Lazy Tick 懒结算 vs 定时后台守护进程
- **问题**：如果为每只猫在后台起定时器推演状态，当用户规模增长时服务器 CPU 与数据库连接池会被迅速耗尽。
- **解法**：采用经典放置游戏的懒计算方案，仅在用户打开应用调用 `/api/cat/status` 时，对比当前时间戳与 `last_interact_time`，一次性完成状态演化与衰减，**兼顾了“猫在自主生活”的拟真感与零后台算力消耗**。

### 2. 记忆架构：结构化萃取与轻量召回 vs 全量上下文硬塞
- **问题**：将全部聊天历史灌入 LLM 会导致 Token 成本暴增、推理延迟拉长，且模型容易在长文本中迷失重点。
- **解法**：在聊天后置链路中提取结构化事实（`preference`、`event`、`emotion`），对话时根据当前输入计算**关键词与重要度复合权重**进行 Top-K 召回，既压低了 Token 消耗，又提升了情感记忆的命中精度。

### 3. 可靠性设计：确定性安全 Fallback 与环境自适应
- **解法**：在未配置或断网无法连接外部 LLM 时，系统无缝降级为**确定性规则生成引擎**，保证作品集的各个核心玩法（领养、换装、任务、探险）100% 可玩，不因三方 API 欠费或故障导致整个项目瘫痪。

---

## 🚀 快速开始与一键部署

### 方式一：国内云服务器一键脚本（阿里云 / 腾讯云 Ubuntu 推荐）

直接登录你的云服务器终端执行：

```bash
curl -fsSL https://raw.githubusercontent.com/Sinera-kiki/meowlog-ai-companion/main/deploy/install.sh | sudo bash
```

脚本自动完成：`基础环境` → `2GB Swap 防爆内存` → `Docker 环境` → `国内镜像加速` → `代码拉取与启动`。

### 方式二：Docker Compose 本地部署

```bash
# 1. 克隆代码
git clone https://github.com/Sinera-kiki/meowlog-ai-companion.git
cd meowlog-ai-companion

# 2. 准备环境变量（可填入 DeepSeek API Key）
cp .env.example .env

# 3. 启动全栈容器
docker compose up --build
```

访问 `http://localhost:8000` 即可开始游玩。

### 方式三：Render Blueprint 一键托管

点击仓库顶部的 **Deploy to Render** 按钮，系统将自动基于 `render.yaml` 创建 Web Service 与 PostgreSQL 数据库。

---

## 📊 质量保障与自动化测试

本项目在 GitHub Actions 中配置了完整的持续集成流水线（CI）：

```bash
# 运行本地自动化测试集
pip install -r backend/requirements-dev.txt
export DATABASE_URL=postgresql://meowlog:meowlog@localhost:5432/meowlog_test
python -m backend.init_db
pytest -q
```

- ✅ **端到端测试覆盖**：领养流程、双槽换装、每日签到、任务奖励核销、探险触发与手帐生成、记忆萃取。
- ✅ **构建门禁**：Vite 前端 TypeScript 强类型校验、Python 字节码编译、Docker 镜像构建。

---

## 📂 仓库目录结构

```text
meowlog-ai-companion/
├── frontend/               # React 18 + Vite 移动端 H5
│   ├── src/
│   │   ├── App.tsx         # 核心交互与状态分发引擎
│   │   ├── index.css       # 基础设计系统与变量规范
│   │   ├── forest-upgrade.css      # 森系小屋主题层
│   │   ├── closet-tabs-upgrade.css # 双槽换装与收藏抽屉
│   │   ├── tailoring-fix.css       # 服装自然剪裁与图层穿透
│   │   ├── adventure.css   # 探险手帐与明信片视觉
│   │   ├── memory.css      # 长期记忆透明化管理抽屉
│   │   ├── gameplay.css    # 每日任务、商店与触感反馈
│   │   └── adoption-upgrade.css    # 森林绘本领养与性格卡片
├── backend/                # FastAPI 业务后端与 AI 引擎
│   ├── app.py              # API 控制器、Lazy Tick、RAG 记忆召回
│   ├── init_db.py          # 幂等 PostgreSQL DDL 与版本平滑迁移
│   └── requirements.txt    # 生产依赖包
├── deploy/                 # 云服务器一键化运维
│   ├── install.sh          # Ubuntu 一键部署脚本（集成 Swap & 镜像加速）
│   └── README.md           # 详细部署踩坑指南
├── docs/                   # 深度设计与交付文档
│   ├── screenshots/        # 产品高清运行截图
│   ├── PRODUCT_CASE_STUDY.md # 产品商业背景与案例复盘
│   ├── ARCHITECTURE.md     # 系统详细架构与时序图
│   └── GAME_DESIGN.md      # 数值模型、成长经济与玩法设计
├── tests/                  # Pytest 自动化测试套件
├── Dockerfile              # 多阶段瘦身镜像构建规范
├── docker-compose.yml      # 全栈一体化编排
└── render.yaml             # PaaS Blueprint 配置文件
```

---

## 🛣️ 迭代路线图 (Roadmap)

- [x] 森林绘本领养与六维人格定制
- [x] 森系小屋与拟真动作动画反馈
- [x] Nikki 暖暖式双槽位（服装+配饰）换装与持久化
- [x] 每日签到与四类陪伴任务系统
- [x] 森林商店与叶子币成长经济闭环
- [x] Web Audio 提示音与移动端震动触感
- [x] 探险倒计时、AIGC 手帐日记与战利品结算
- [x] 结构化长期记忆萃取、Top-K 召回与透明删除
- [x] Docker / Compose / Render / 腾讯云一键部署
- [x] GitHub Actions CI 全自动化测试流
- [ ] 动态天气与昼夜光影对猫咪行为的自适应
- [ ] 扩散模型（SD/Flux）AIGC 探险实况拍立得生成
- [ ] PWA 离线运行与主动消息通知

---

## 📄 License

MIT License © 2026 Deng Wanting.
