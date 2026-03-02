#!/bin/bash
# ============================================================
# Skrypt instalacyjny - MPI-530 Przewodnik
# VPS Hostinger, Ubuntu 24.04
# ============================================================

set -e

echo "============================================"
echo "  MPI-530 Przewodnik - Instalacja"
echo "============================================"

APP_DIR="/home/mpi530-app"

# Sprawdz czy jestesmy w katalogu aplikacji
if [ ! -f "$APP_DIR/backend/server.py" ]; then
    echo "BLAD: Uruchom skrypt z katalogu /home/mpi530-app"
    echo "Uzyj: cd /home/mpi530-app && bash deployment/setup.sh"
    exit 1
fi

# ============================================
# 1. Aktualizacja systemu
# ============================================
echo ""
echo "[1/7] Aktualizacja systemu..."
apt update -y
apt upgrade -y

# ============================================
# 2. Instalacja Python 3 i narzedzi
# ============================================
echo ""
echo "[2/7] Instalacja Python 3..."
apt install -y python3 python3-pip python3-venv curl git

# ============================================
# 3. Instalacja Node.js 20 i Yarn
# ============================================
echo ""
echo "[3/7] Instalacja Node.js 20..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs
fi
npm install -g yarn

echo "Node.js: $(node -v)"
echo "Yarn: $(yarn -v)"

# ============================================
# 4. Instalacja MongoDB
# ============================================
echo ""
echo "[4/7] Instalacja MongoDB..."
if ! command -v mongod &> /dev/null; then
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
        gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
    echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
        tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    apt update
    apt install -y mongodb-org
    systemctl start mongod
    systemctl enable mongod
fi
echo "MongoDB status: $(systemctl is-active mongod)"

# ============================================
# 5. Konfiguracja backendu
# ============================================
echo ""
echo "[5/7] Konfiguracja backendu Python..."
cd "$APP_DIR/backend"

# Utworz srodowisko wirtualne
python3 -m venv venv
source venv/bin/activate

# Zainstaluj zaleznosci (bez emergentintegrations i jq ktore nie sa potrzebne na produkcji)
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv pymongo motor pydantic gunicorn

# Utworz plik .env
cat > .env << 'ENVFILE'
MONGO_URL=mongodb://localhost:27017
DB_NAME=mpi530_guide
ENVFILE

echo "Backend skonfigurowany."
deactivate

# ============================================
# 6. Budowanie frontendu
# ============================================
echo ""
echo "[6/7] Budowanie frontendu React..."
cd "$APP_DIR/frontend"

# Ustaw URL backendu (wzgledny - na tym samym serwerze)
cat > .env << 'ENVFILE'
REACT_APP_BACKEND_URL=
ENVFILE

yarn install
yarn build

echo "Frontend zbudowany w: $APP_DIR/frontend/build"

# ============================================
# 7. Konfiguracja systemd
# ============================================
echo ""
echo "[7/7] Konfiguracja serwisu systemd..."

cat > /etc/systemd/system/mpi530-backend.service << SERVICEFILE
[Unit]
Description=MPI-530 Przewodnik - FastAPI Backend
After=network.target mongod.service

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR/backend
Environment=PATH=$APP_DIR/backend/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
ExecStart=$APP_DIR/backend/venv/bin/uvicorn server:app --host 127.0.0.1 --port 8001
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEFILE

systemctl daemon-reload
systemctl enable mpi530-backend
systemctl start mpi530-backend

echo ""
echo "============================================"
echo "  INSTALACJA ZAKONCZONA!"
echo "============================================"
echo ""
echo "Status backendu:"
systemctl status mpi530-backend --no-pager -l
echo ""
echo "Nastepne kroki:"
echo "1. Skonfiguruj domene w CloudPanel (patrz INSTRUKCJA_WDROZENIA.md)"
echo "2. Dodaj konfiguracje Nginx"
echo "3. Wlacz SSL (HTTPS)"
echo ""
echo "Test API: curl http://localhost:8001/api/health"
echo ""
