#!/bin/bash
set -euo pipefail

REPO="https://github.com/krystofham/F1_game"
DIR="F1_game"

if [ ! -d "$DIR" ]; then
  git clone "$REPO"
fi

cd "$DIR"

echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt

echo "Installing frontend dependencies..."
cd frontend
npm install

echo "Starting MMRAC1NG (development mode)..."
npm run desktop:dev
