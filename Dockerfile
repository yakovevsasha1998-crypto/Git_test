# Dockerfile
FROM python:3.14

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY ./app /app

# Открываем порт
EXPOSE 8000

# Команда для запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]