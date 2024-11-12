# Используем официальный образ Python в качестве базового
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app/

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000 для приложения
EXPOSE 8000

# Команда для запуска приложения с использованием Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
