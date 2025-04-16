# Базовый образ Python
FROM python:3.11-slim-bookworm

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Точка входа
COPY .deployment/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]