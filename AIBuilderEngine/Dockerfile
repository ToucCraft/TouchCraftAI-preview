# AlBuilderEngine/Dockerfile

# Используем легкий Python
FROM python:3.11-slim

# Отключаем создание .pyc и буферизацию (чтобы логи шли сразу)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая папка ВНУТРИ контейнера
WORKDIR /app

# --- ВАЖНОЕ ДОБАВЛЕНИЕ ---
# Устанавливаем Docker CLI.
# Это позволит скрипту deployer.py выполнять команды "docker build" и "docker run".
# Благодаря пробросу сокета в docker-compose, этот CLI будет управлять Докером на хосте.
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*
# -------------------------

# Сначала копируем зависимости (для кэша Docker)
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код из AlBuilderEngine внутрь контейнера
COPY . .

# Говорим, какой порт будет слушать контейнер
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]