# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=SmartZona.settings

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы (добавил curl для healthchecks)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python (копируем отдельно для лучшего кэширования)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем проект (исключаем ненужные файлы через .dockerignore)
COPY . .

# Порт, который будет использовать приложение
EXPOSE 8000

# Команда для запуска приложения (добавил таймауты для gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "--workers", "4", "SmartZona.wsgi:application"]