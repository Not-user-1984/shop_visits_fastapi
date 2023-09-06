#!/bin/bash
sleep 5
cd ..
alembic upgrade head
cd src/
python data_loading.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

