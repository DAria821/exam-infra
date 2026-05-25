#!/bin/bash
# ============================================================
#  EXAM BOOTSTRAP — 1 command to full grade 10
#  Usage: curl -fsSL https://raw.githubusercontent.com/USER/exam-infra/main/bootstrap.sh | sudo bash
# ============================================================
set -e

echo "==> [1/5] Installing system dependencies..."
apt-get update -qq
apt-get install -y git curl ca-certificates gnupg lsb-release

echo "==> [2/5] Installing Docker..."
if ! command -v docker &>/dev/null; then
    curl -fsSL https://get.docker.com | sh
fi
systemctl enable --now docker

echo "==> [3/5] Cloning repository..."
rm -rf /opt/exam-infra
git clone https://github.com/DAria821/exam-infra.git /opt/exam-infra
cd /opt/exam-infra

echo "==> [4/5] Starting all services..."
docker compose up -d --build

echo "==> [5/5] Waiting for Vault and storing secret..."
until docker exec exam-vault vault status > /dev/null 2>&1; do
    echo "    Waiting for Vault to initialize..."
    sleep 2
done

docker exec \
  -e VAULT_ADDR=http://127.0.0.1:8200 \
  -e VAULT_TOKEN=root \
  exam-vault \
  vault kv put secret/app api_key="ExamSecretKey-2025-Infrastructure"

echo ""
echo "============================================"
echo "  DEPLOYMENT COMPLETE — All systems UP"
echo "============================================"
echo "  App (via Nginx):  http://$(hostname -I | awk '{print $1}')"
echo "  Grafana:          http://$(hostname -I | awk '{print $1}'):3000  (admin/admin)"
echo "  Vault UI:         http://$(hostname -I | awk '{print $1}'):8200  (token: root)"
echo "============================================"
