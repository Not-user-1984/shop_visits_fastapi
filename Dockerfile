FROM python:3.11

RUN mkdir /shop_visits_fastapi

WORKDIR /shop_visits_fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# RUN alembic upgrade head



WORKDIR src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
