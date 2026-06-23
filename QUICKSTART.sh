#!/bin/bash

git clone https://github.com/krystofham/F1_game
cd F1_game

pip install -r requirements.txt --break-system-packages

cd engine
uvicorn app:app --port 8000 &
cd ..

cd frontend
npm install 
npm run desktop:dev