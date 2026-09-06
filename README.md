# MeowLog · 喵喵日记 🐾

> **基于自主智能体与长效记忆的 AI 治愈系伴侣猫**
> 一只有自己生活、会记住你的心事，也会带着故事回家的虚拟宠物。

[![CI](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml/badge.svg)](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-718263.svg)](LICENSE)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**[🎮 立即在线试玩 (Live Game)](http://154.8.153.135:8000)** · **[📖 产品商业与案例复盘](docs/PRODUCT_CASE_STUDY.md)** · **[🏗️ 系统架构与时序设计](docs/ARCHITECTURE.md)** · **[🎮 数值模型与玩法设计](docs/GAME_DESIGN.md)**

---

## 📱 产品实机演示

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

## 🎯 为什么做这个产品？（痛点与行业机会）

在 AI 伴侣与情感陪伴赛道，传统方案普遍存在两大断层：

1. **传统虚拟宠物（如电子鸡、猫咪后院）**：有养成感与收集乐趣，但**交互死板、无法真正理解玩家的复杂情绪与现实经历**；
2. **纯对话类 AI Agent（如常见聊天 Bot）**：能听懂文字，但**缺乏游戏化目标驱动、NPC 缺乏自主生活感**，用户容易产生“聊天疲劳”并迅速流失。

| 玩家核心痛点 | 传统方案的缺陷 | MeowLog 的产品解法 |
|---|---|---|
| **记忆断层**：每次对话像重新认识 | 依赖固定窗口上下文，历史很快被冲刷 | **分层记忆库 + 动态 RAG 检索**，自动提炼偏好、情绪与关键事件 |
| **工具感强**：NPC 永远是被动等待提问 | 缺乏时间感知，NPC 状态完全静态 | **Lazy Tick 离线状态机**，推演猫咪自主生活轨迹与随机探险 |
| **缺乏留存动机**：聊完即走，无目标感 | 纯文字消耗，无成长与经济反馈 | **每日陪伴任务 + 叶子币成长经济 + 双槽森系换装** |
| **情绪负担重**：许多陪伴产品对话过于沉重 | 缺少趣味与游戏化距离感 | **六维猫咪性格 Prompt + 灵动触感反馈**，提供轻松解压的情绪价值 |

---

## 🧩 双螺旋核心循环设计

产品构建了 **「游戏玩法飞轮」** 与 **「AI 认知情感飞轮」** 的双螺旋驱动架构：

```mermaid
flowchart LR
    subgraph CoreLoop["🎮 游戏玩法飞轮 (Game Loop)"]
        A[每日陪伴互动\n喂食 · 抚摸 · 玩耍 · 倾诉] --> B[陪伴任务 & 签到]
        B --> C[获取叶子币 🍃]
        C --> D[森林商店选购心仪服饰]
        D --> E[暖暖式双槽换装 & 收藏]
        A --> F[提升亲密度 Lv]
        F --> G[解锁高阶探险 & 稀有装扮]
        G --> H[派遣离线探险]
        H --> I[生成 AI 探险手帐 & 战利品]
        I --> C
    end

    subgraph MemoryLoop["🧠 情感认知飞轮 (AI Memory Loop)"]
        A --> J[自然语言倾诉]
        J --> K[异步结构化事实萃取\nPreference · Event · Emotion]
        K --> L[(PostgreSQL 长期记忆表)]
        L --> M[Top-K 相关度 & 重要度加权检索]
        M --> N[动态组装 System Prompt]
        N --> J
    end
```

### 1. 森林绘本领养与个性化人格（Onboarding）
- **六维人格设定**：傲娇猫猫、黏人甜心、哲学发呆猫、神经质探险家、吃货摆烂猫、护短大佬猫；
- **新手正向反馈**：领养即送 4 件新手装（赤豆围巾、林间雏菊、苔藓斗篷、野餐围裙）与 30 叶子币，零门槛体验双槽换装。

### 2. 状态机与离线自主生活（Lazy Tick Engine）
- 模拟真实的饱食度、心情值与亲密度演化；
- **离线推演**：根据上次互动时间差，一次性演算离线期间的生活轨迹（睡觉、发呆、饿肚子、出门探险），兼顾拟真感与服务器成本。

### 3. 暖暖式双槽位森系换装（Nikki-Style Wardrobe）
- **独立双槽位**：服装槽（斗篷/雨衣/针织衫/礼服）与配饰槽（围巾/帽子/挎包/领结）自由叠穿，持久化存储；
- **单品收藏**：支持一键点亮爱心收藏，在专属收藏页分类管理。

### 4. 探险手帐与 AIGC 叙事（Adventure Journal）
- 派遣小猫外出探险（支持实时倒计时），归来结合猫咪人格与目的地动态生成 **80~120 字第一人称探险手帐**，带回专属战利品与明信片。

### 5. 记忆沉淀与透明化管理（Memory Drawer）
- 自动提取偏好、事件与情绪，在聊天界面提供专属“回忆”抽屉，用户可透明查看、一键删除，保护隐私并提升可解释性。

---

## 🏗️ 产品驱动的技术架构

```mermaid
flowchart TB
    subgraph Client["📱 前端层 (React 18 + TypeScript + Vite)"]
        UI[森系房间 · 绘本领养 · 双槽衣橱 · 探险手帐 · 聊天抽屉]
        Sensory[Web Audio 提示音 & Vibration 触觉反馈]
        Guest[Guest UUID 游客隔离会话]
    end

    subgraph Server["⚡ 业务与状态层 (FastAPI)"]
        Router[RESTful API 路由]
        Auth[X-Guest-Id 游客中间件]
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

## 💡 产品与工程深度结合的关键取舍

### 1. 状态模拟：Lazy Tick 懒推演 vs 定时后台守护进程
- **产品诉求**：让玩家感觉“小猫在我离线时也有自己的生活”。
- **工程挑战**：为每个用户在后台挂定时器跑状态机，服务器 CPU 和数据库连接池会随着用户量快速崩溃。
- **PM/架构解法**：采用经典放置类游戏的**时间差懒推演（Lazy Tick）**。仅在客户端上线请求 `/api/cat/status` 时，对比当前时间戳与 `last_interact_time`，一次性完成状态演变与消耗结算，**用 0 后台算力开销实现了 100% 的拟真生命感**。

### 2. 记忆架构：结构化事实萃取 + 加权检索 vs 全量上下文硬塞
- **产品诉求**：小猫能记住我的偏好与重要心事，并在后续对话中自然唤醒。
- **工程挑战**：无限堆叠聊天历史会导致 Token 成本剧增、回复延迟增加，且大模型容易遗忘重点。
- **PM/架构解法**：在对话后置链路中调用轻量提取器，将事实沉淀为带标签的结构化记录（`preference`、`event`、`emotion`）。对话前计算**输入文本相关度 + 记忆重要度 + 访问衰减**进行 Top-K 召回，既压低了 80% 的 Token 成本，又大幅提升了情感共鸣命中率。

### 3. 可靠性设计：确定性安全 Fallback 与环境解耦
- **产品诉求**：作品集 Demo 必须保证任何人随时随地点开都能顺畅玩，不能因为三方 API 故障导致白屏。
- **PM/架构解法**：在未配置或断网无法连接外部 LLM 时，系统无缝切换至**确定性规则生成引擎**，保证领养、换装、任务、探险等全部核心玩法 100% 可玩可用。

### 4. 移动端体验：App 级三层弹性布局 vs 传统页面滚动
- **产品诉求**：在手机浏览器里提供原生游戏级的精致操作手感。
- **PM/架构解法**：采用 `Flex Container` 独立分层架构——顶部 Header 磨砂吸顶、中间区域独立平滑滚动并隐藏滚动条、底部导航栏与弹窗抽屉精准贴底，彻底杜绝了 H5 常见的底栏漂移与内容遮挡 Bug。

---

## 📊 数值模型与成长经济

```text
每日签到 (12~24 🍃) + 4项陪伴任务 (45 🍃) + 探险归来 (8~18 🍃) ≈ 每日稳健产出 65~87 叶子币
```

| 装扮档位 | 定价区间 (🍃) | 解锁门槛 | 代表单品 | 设计目的 |
|---|---|---|---|---|
| **新手赠送** | 0 (初始送4件) | Lv.1 (零门槛) | 赤豆围巾、林间雏菊、苔藓斗篷、野餐围裙 | 确保首日即可体验双槽搭配乐趣 |
| **普通单品** | 38 ~ 58 | Lv.1 ~ Lv.2 | 森林探险挎包、云朵睡帽、青柠雨衣 | 建立首日留存目标，1天任务即可兑换 |
| **进阶单品** | 68 ~ 78 | Lv.2 ~ Lv.3 | 海盐领结、橡果针织衫 | 驱动 2~3 天连续回访 |
| **稀有典藏** | 98 ~ 108 | Lv.3 ~ Lv.4 | 莓果小礼服、神秘纸箱、月光睡袍 | 构筑长期养成目标与收集成就感 |

---

## 🚀 快速开始与部署指南

### 方式一：国内云服务器一键脚本（腾讯云 / 阿里云推荐）

登录服务器终端直接执行：

```bash
curl -fsSL https://raw.githubusercontent.com/Sinera-kiki/meowlog-ai-companion/main/deploy/install.sh | sudo bash
```

脚本自动完成：`基础环境` → `2GB Swap 内存防护` → `Docker 环境` → `国内镜像加速` → `全栈启动`。

### 方式二：Docker Compose 本地一键启动

```bash
# 1. 克隆代码
git clone https://github.com/Sinera-kiki/meowlog-ai-companion.git
cd meowlog-ai-companion

# 2. 准备环境变量（可选填 DeepSeek API Key）
cp .env.example .env

# 3. 启动全栈应用
docker compose up --build
```

访问 `http://localhost:8000` 即可开始游玩。

### 方式三：Render Blueprint 一键托管

点击仓库顶部的 **Deploy to Render** 按钮，系统将自动基于 `render.yaml` 创建 Web Service 与 PostgreSQL 数据库。

---

## 🧪 自动化测试与持续集成 (CI)

本项目配置了完整的 GitHub Actions CI 流水线：

```bash
# 运行本地自动化测试
pip install -r backend/requirements-dev.txt
export DATABASE_URL=postgresql://meowlog:meowlog@localhost:5432/meowlog_test
python -m backend.init_db
pytest -q
```

- ✅ **核心链路测试覆盖**：领养状态流转、双槽换装、每日任务与签到奖励核销、探险倒计时与手帐结算、记忆加权召回算法。
- ✅ **全自动化门禁**：TypeScript 静态检查、Vite 前端生产打包、Python 字节码编译、Docker 镜像构建。

---

## 📂 仓库目录规范

```text
meowlog-ai-companion/
├── frontend/               # React 18 + TypeScript + Vite 移动端 H5
│   ├── src/
│   │   ├── App.tsx         # 核心交互分发与状态流转引擎
│   │   ├── index.css       # 基础设计系统与视觉变量
│   │   ├── forest-upgrade.css      # 森系小屋主题渲染层
│   │   ├── closet-tabs-upgrade.css # 双槽换装与单品收藏抽屉
│   │   ├── tailoring-fix.css       # 服装剪裁与图层穿透贴合
│   │   ├── adventure.css   # 探险手帐与明信片视觉
│   │   ├── memory.css      # 长期记忆透明化管理抽屉
│   │   ├── gameplay.css    # 每日任务、商店与触感反馈
│   │   └── adoption-upgrade.css    # 森林绘本领养与性格卡片
├── backend/                # FastAPI 业务后端与 AI 编排引擎
│   ├── app.py              # 路由控制器、Lazy Tick 推演、RAG 记忆召回
│   ├── init_db.py          # 幂等 PostgreSQL DDL 与平滑迁移
│   └── requirements.txt    # 生产依赖清单
├── deploy/                 # 云服务器一键化运维
│   ├── install.sh          # Ubuntu 一键部署脚本（集成 Swap & 镜像加速）
│   └── README.md           # 详细部署与运维手册
├── docs/                   # 深度设计与交付文档
│   ├── screenshots/        # 产品高清运行截图
│   ├── PRODUCT_CASE_STUDY.md # 产品商业背景与指标体系复盘
│   ├── ARCHITECTURE.md     # 系统分层架构与时序设计
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
