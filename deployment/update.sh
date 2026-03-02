#!/bin/bash
# ============================================
# Skrypt aktualizacji - MPI-530 Przewodnik
# Uruchom po kazdym git pull
# ============================================

set -e

APP_DIR="/home/mpi530-app"

echo "Aktualizacja MPI-530 Przewodnik..."

# Pobierz najnowszy kod
cd "$APP_DIR"
git pull

# Aktualizuj backend
echo "Aktualizacja backendu..."
cd "$APP_DIR/backend"
source venv/bin/activate
pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn python-dotenv pymongo motor pydantic
deactivate

# Zbuduj frontend
echo "Budowanie frontendu..."
cd "$APP_DIR/frontend"
yarn install
yarn build

# Restart backendu
echo "Restart serwisu..."
sudo systemctl restart mpi530-backend

echo ""
echo "Aktualizacja zakonczona!"
echo "Status: $(sudo systemctl is-active mpi530-backend)"
