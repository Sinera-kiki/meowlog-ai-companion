#!/usr/bin/env bash
# MeowLog 云服务器一键部署脚本
# 适用：Ubuntu 20.04/22.04/24.04（阿里云 / 腾讯云通用）
# 用法：
#   sudo bash install.sh                      # 不带 AI Key，使用内置演示回复
#   sudo LLM_API_KEY=sk-xxx bash install.sh   # 可选：填 AI Key 启用真实对话
set -euo pipefail

REPO_URL="https://github.com/Sinera-kiki/meowlog-ai-companion.git"
APP_DIR="/opt/meowlog"

echo "==> [0/6] 准备基础环境与交换空间"
apt-get update -y
apt-get install -y curl git ca-certificates
if [ "$(swapon --show | wc -l)" -eq 0 ] && [ "$(awk '/MemTotal/{print int($2/1024)}' /proc/meminfo)" -le 2200 ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  grep -q '^/swapfile ' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

echo "==> [1/6] 安装 Docker"
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
fi

echo "==> [2/6] 安装 docker compose 插件"
if ! docker compose version >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y docker-compose-plugin
fi

echo "==> [3/6] 拉取代码"
if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR"
  git pull --ff-only
else
  rm -rf "$APP_DIR"
  git clone "$REPO_URL" "$APP_DIR"
  cd "$APP_DIR"
fi

echo "==> [4/6] 准备环境变量"
[ -f .env ] || cp .env.example .env
if [ -n "${LLM_API_KEY:-}" ]; then
  sed -i "s|^LLM_API_KEY=.*|LLM_API_KEY=${LLM_API_KEY}|" .env
  sed -i "s|^LLM_BASE_URL=.*|LLM_BASE_URL=${LLM_BASE_URL:-https://api.openai.com/v1}|" .env
fi

echo "==> [5/6] 构建并启动"
docker compose up -d --build

echo "==> [6/6] 检查服务状态"
docker compose ps

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ 部署完成！访问地址：http://${IP}:8000"
echo "   首次打开会自动初始化数据库。"
echo ""
echo "🔔 提醒：请在云厂商控制台的「安全组/防火墙」放行 8000 端口。"