# 国内云服务器部署指南（阿里云 / 腾讯云）

适用于没有海外卡、希望把 MeowLog 部署成可公开访问作品集的情形。

## 一、准备工作：买 1 台服务器

学生党优先搜索自己云厂商的「学生机 / 校园优惠」，选入门配置即可：

- 系统：**Ubuntu 22.04 / 24.04**
- 配置：2 核 2G ~ 2 核 4G 足够
- 地域：选离目标用户近的（投国内就国内地域）

买完拿到三样东西：

1. 公网 IP
2. root 密码（或密钥）
3. 控制台地址

## 二、放行端口（重要）

在云厂商控制台找到「安全组」（阿里云）或「防火墙」（腾讯云），添加入站规则，放行：

- 端口 `8000`（MeowLog）
- 来源 `0.0.0.0/0`

不放行这个端口，外部访问会被挡住。

## 三、登录服务器并一键部署

本地终端用 SSH 连上服务器：

```bash
ssh root@你的公网IP
```

然后复制粘贴这一条命令：

```bash
curl -fsSL https://raw.githubusercontent.com/Sinera-kiki/meowlog-ai-companion/main/deploy/install.sh | sudo bash
```

脚本会自动：装 Docker → 拉代码 → 初始化环境 → 构建并启动。

完成后终端会打印访问地址 `http://<公网IP>:8000`。

## 四、（可选）启用真实 AI 对话

不配置 AI Key 也能玩，只是小猫回复用的是内置的简单文案。要真实 AI：

```bash
cd /opt/meowlog
vi .env    # 填写 LLM_API_KEY，并可改 LLM_BASE_URL / LLM_MODEL
docker compose up -d --build
```

DeepSeek 等兼容 OpenAI 的接口也能直接填：

```bash
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
LLM_API_KEY=sk-xxx
```

## 五、日常维护

```bash
cd /opt/meowlog
git pull                      # 拉取最新代码
docker compose up -d --build  # 重启并更新
docker compose logs -f app    # 查看日志
```

## 六、（可选）绑定域名 + HTTPS

有域名的话，可以用 Caddy 或 Nginx 反代到本机 8000 端口，并自动申请免费 HTTPS 证书。这一步可以让部署体验更专业，需要时再单独配置。