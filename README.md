# MeowLog · 喵喵日记 🐾

> 一个结合长效记忆、自主状态模拟与轻量换装养成的 AI 虚拟宠物网页游戏。

[![CI](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml/badge.svg)](https://github.com/Sinera-kiki/meowlog-ai-companion/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-718263.svg)](LICENSE)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

**[🎮 在线体验游戏 (Live Game)](http://154.8.153.135:8000)** · **[📖 产品设计复盘](docs/PRODUCT_CASE_STUDY.md)** · **[🏗️ 架构与时序设计](docs/ARCHITECTURE.md)** · **[🎮 数值与玩法设计](docs/GAME_DESIGN.md)**

---

## 页面功能展示

<table>
  <tr>
    <td width="25%" align="center">
      <img src="docs/screenshots/onboarding.png" alt="森林绘本领养" width="100%" />
      <br />
      <sub><b>1. 领养流程与人格定制</b></sub>
    </td>
    <td width="25%" align="center">
      <img src="docs/screenshots/home-room.png" alt="森系小屋互动" width="100%" />
      <br />
      <sub><b>2. 房间主场景与动作反馈</b></sub>
    </td>
    <td width="25%" align="center">
      <img src="docs/screenshots/wardrobe-shop.png" alt="双槽位换装与商店" width="100%" />
      <br />
      <sub><b>3. 双槽位换装与装扮商店</b></sub>
    </td>
    <td width="25%" align="center">
      <img src="docs/screenshots/journal-memory.png" alt="探险手帐与记忆管理" width="100%" />
      <br />
      <sub><b>4. 离线探险手帐与记忆抽屉</b></sub>
    </td>
  </tr>
</table>

---

## 背景与痛点分析

在情感陪伴与虚拟宠物领域，现有产品通常面临两类问题：

1. **传统虚拟宠物**（如电子鸡、各类放置类小游戏）：具备收集与养成体系，但交互逻辑固定，无法真正理解用户的倾诉与日常情绪；
2. **常规 AI 对话 Bot**：能够进行自然语言交流，但缺乏游戏化目标支撑，且 NPC 处于被动应答状态，用户容易产生交互疲劳。

| 核心痛点 | 常见缺陷 | MeowLog 的解法 |
|---|---|---|
| 记忆断层 | 对话窗口有限，历史很快丢失 | 分层记忆库配合相关性检索，提取偏好、情绪与关键事件 |
| 交互被动 | NPC 缺乏时间感知与独立状态 | 引入时间差状态推演（Lazy Tick），模拟离线生活与随机探险 |
| 缺乏目标 | 聊完即走，缺少持续打开的动力 | 建立每日任务、叶子币经济、服饰解锁与双槽换装 |
| 对话沉重 | 纯文字陪伴容易带来沟通压力 | 六种猫咪性格设定配合触觉与声音反馈，提供轻松的陪伴体验 |

---

## 核心玩法与系统闭环

系统由两个相互联动的闭环构成：

```mermaid
flowchart LR
    subgraph CoreLoop["游戏玩法循环"]
        A[日常陪伴互动\n喂食 · 抚摸 · 玩耍 · 倾诉] --> B[任务进度与签到]
        B --> C[获取叶子币 🍃]
        C --> D[商店兑换服饰]
        D --> E[双槽位换装与收藏]
        A --> F[积累亲密度]
        F --> G[解锁高阶探险与服饰]
        G --> H[派遣外出探险]
        H --> I[生成探险故事手帐]
        I --> C
    end

    subgraph MemoryLoop["认知记忆流转"]
        A --> J[自然语言对话]
        J --> K[提取关键事实与情绪\n偏好 · 事件 · 情绪]
        K --> L[(PostgreSQL 长期记忆)]
        L --> M[计算相关度与权重检索]
        M --> N[组装猫咪上下文 Prompt]
        N --> J
    end
```

### 1. 领养与个性定制（Onboarding）
- 提供 6 种预设性格：傲娇、黏人、哲学、探险、摆烂、护短；
- 领养即赠送 4 件基础服饰（赤豆围巾、林间雏菊、苔藓斗篷、野餐围裙）与 30 叶子币，降低初始体验门槛。

### 2. 状态推演与离线模拟（Lazy Tick）
- 包含饱食度、心情值、亲密度与实时状态；
- 根据用户离线时长一次性推演状态变化（如饥饿、睡觉、发呆），避免依赖后台定时任务。

### 3. 双槽位森系换装系统（Wardrobe）
- 分离服装槽（斗篷/雨衣/针织衫/礼服）与配饰槽（围巾/帽子/挎包/领结），支持自由叠穿；
- 支持单品收藏，方便在专属页面分类查看。

### 4. 探险手帐与故事生成（Adventure Journal）
- 派遣猫咪外出探险，归来后根据猫咪性格与目的地生成 80 至 120 字第一人称日记，并结算战利品与代币。

### 5. 记忆沉淀与透明管理（Memory Management）
- 自动提取对话中的重要事件与情绪，提供独立的回忆抽屉，用户可查看提取结果并自主删除。

---

## 技术架构与数据流

```mermaid
flowchart TB
    subgraph Client["前端 (React 18 + TypeScript + Vite)"]
        UI[场景渲染 · 绘本领养 · 双槽衣橱 · 手帐 · 聊天]
        Sensory[Web Audio 音效 & Vibration 触觉反馈]
        Guest[Guest UUID 游客会话隔离]
    end

    subgraph Server["后端与业务逻辑 (FastAPI)"]
        Router[API 路由]
        Auth[游客会话管理]
        StateEngine[Lazy Tick 状态推演]
        QuestEngine[签到 · 任务 · 商店结算]
        AdventureEngine[探险与故事生成]
        MemoryEngine[记忆提取与相关性检索]
    end

    subgraph Storage["数据存储 (PostgreSQL 16)"]
        CatsTable[(cats: 状态 · 货币 · 资产 · 穿搭)]
        MemsTable[(memories: 记忆 · 情绪 · 重要度)]
        LogsTable[(chat_logs: 对话流)]
        AdvTable[(adventures: 探险 · 手帐 · 战利品)]
    end

    subgraph LLM["大模型推理 (OpenAI-compatible)"]
        ChatModel[DeepSeek / OpenAI 文本模型]
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

## 关键技术决策与权衡

### 1. 离线状态推演：按需计算替代后台常驻进程
- **考量**：若为每个用户在后台启动定时器执行状态轮询，随着用户量增长，服务器资源与数据库连接会被迅速占满；
- **实现**：在用户每次发起请求时，读取 `last_interact_time` 与当前时间对比，计算时间差并一次性完成状态结算与衰减，在零后台开销的前提下实现状态流转。

### 2. 长期记忆管理：结构化提取与按需召回替代全量上下文
- **考量**：将全部历史对话塞入上下文会导致 Token 消耗剧增、接口响应变慢，且大模型容易忽略早期关键信息；
- **实现**：在对话后置处理中提取结构化事实（偏好、事件、情绪），在后续交互中根据输入内容计算文本相关度与重要度，仅召回 Top-K 记忆，平衡了对话准确度与接口成本。

### 3. 可靠性设计：确定性降级机制保障可用性
- **实现**：在未配置 API Key 或外部接口异常时，系统自动切换至内置的确定性规则逻辑，确保领养、换装、任务与探险等核心流程正常运行。

### 4. 移动端体验：独立分层容器解决定位与滑动异常
- **实现**：采用 Flex 弹性分层布局，顶部导航固定吸顶，中间主体区域独立滚动并隐藏滚动条，底部菜单与浮层抽屉精准贴底，避免了 H5 页面中常见的定位漂移问题。

---

## 游戏数值与经济循环

```text
日常收益测算：每日签到 (12~24 🍃) + 4项任务 (45 🍃) + 探险奖励 (8~18 🍃) ≈ 每日产出 65~87 叶子币
```

| 服饰档位 | 价格区间 (🍃) | 解锁等级 | 代表单品 | 设计考量 |
|---|---|---|---|---|
| 新手赠送 | 0 (领养送4件) | Lv.1 | 赤豆围巾、林间雏菊、苔藓斗篷、野餐围裙 | 确保进入游戏即可体验基础搭配 |
| 普通单品 | 38 ~ 58 | Lv.1 ~ Lv.2 | 森林探险挎包、云朵睡帽、青柠雨衣 | 1 天日常收益即可兑换，建立正向反馈 |
| 进阶单品 | 68 ~ 78 | Lv.2 ~ Lv.3 | 海盐领结、橡果针织衫 | 鼓励连续 2 至 3 天参与日常任务 |
| 稀有典藏 | 98 ~ 108 | Lv.3 ~ Lv.4 | 莓果小礼服、神秘纸箱、月光睡袍 | 作为阶段性目标，提供长期收集动力 |

---

## 本地运行与部署

### 方式一：国内云服务器一键安装（推荐）

在 Ubuntu 云服务器终端执行：

```bash
curl -fsSL https://raw.githubusercontent.com/Sinera-kiki/meowlog-ai-companion/main/deploy/install.sh | sudo bash
```

脚本自动配置基础依赖、Swap 内存交换区、Docker 与国内镜像加速。

### 方式二：Docker Compose 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/Sinera-kiki/meowlog-ai-companion.git
cd meowlog-ai-companion

# 2. 配置环境变量
cp .env.example .env

# 3. 启动服务
docker compose up --build
```

访问 `http://localhost:8000` 即可开始体验。

### 方式三：Render Blueprint 一键部署

点击仓库顶部的 **Deploy to Render**，根据 `render.yaml` 自动创建 Web Service 与 PostgreSQL 实例。

---

## 自动化测试与 CI 门禁

项目已集成 GitHub Actions 持续集成流水线：

```bash
# 本地运行测试
pip install -r backend/requirements-dev.txt
export DATABASE_URL=postgresql://meowlog:meowlog@localhost:5432/meowlog_test
python -m backend.init_db
pytest -q
```

- **测试范围**：覆盖领养状态流转、双槽换装、任务核销、探险故事生成、记忆检索权重计算；
- **CI 门禁**：每次提交自动执行 TypeScript 类型检查、前端生产构建、Python 语法编译与 Docker 镜像构建。

---

## 代码目录结构

```text
meowlog-ai-companion/
├── frontend/               # React 18 + TypeScript + Vite 前端
│   ├── src/
│   │   ├── App.tsx         # 状态流转与交互组件
│   │   ├── index.css       # 基础布局规范
│   │   ├── forest-upgrade.css      # 森系小屋场景样式
│   │   ├── closet-tabs-upgrade.css # 换装与收藏样式
│   │   ├── tailoring-fix.css       # 服饰图层贴合样式
│   │   ├── adventure.css   # 探险手帐与明信片样式
│   │   ├── memory.css      # 记忆抽屉样式
│   │   ├── gameplay.css    # 任务与商店样式
│   │   └── adoption-upgrade.css    # 领养引导页样式
├── backend/                # FastAPI 后端服务
│   ├── app.py              # 路由控制器、推演算法、记忆召回
│   ├── init_db.py          # PostgreSQL 表结构初始化与迁移
│   └── requirements.txt    # 依赖声明
├── deploy/                 # 部署脚本与运维说明
│   ├── install.sh          # Linux 一键部署脚本
│   └── README.md           # 部署指南
├── docs/                   # 产品与架构文档
│   ├── screenshots/        # 实机演示截图
│   ├── PRODUCT_CASE_STUDY.md # 产品案例复盘
│   ├── ARCHITECTURE.md     # 系统架构设计
│   └── GAME_DESIGN.md      # 游戏数值设计
├── tests/                  # 自动化测试用例
├── Dockerfile              # 生产镜像构建文件
├── docker-compose.yml      # 全栈容器编排
└── render.yaml             # Render 配置文件
```

---

## 后续规划

- 支持动态天气与昼夜光影变化；
- 接入图片生成模型生成探险实况明信片；
- 支持 PWA 离线运行与主动消息提醒。

---

## License

MIT License © 2026 Deng Wanting.
