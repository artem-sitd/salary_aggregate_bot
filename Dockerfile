FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

# Установка переменной окружения для использования .env.docker
ENV USE_DOCKER=1

WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
