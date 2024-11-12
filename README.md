# Task Manager Application

Это приложение для управления задачами с возможностью создания, удаления и получения задач через API. Приложение использует FastAPI для веб-сервиса, PostgreSQL для хранения данных, и SQLAlchemy для работы с базой данных.

## Структура проекта

- **app** - основное приложение на FastAPI.
- **database** - база данных с моделями и Redis
- **docker-compose.yml** - файл для запуска контейнеров через Docker Compose.
- **Dockerfile** - файл для создания Docker-образа приложения.

## Технологии

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose

## Развертывание проекта с Docker Compose

Для запуска проекта с помощью Docker Compose выполните следующие шаги.

### 1. Клонирование репозитория

Сначала клонируйте репозиторий с GitHub на ваш локальный компьютер.

```bash
git clone https://github.com/NikolayBogachev/task-manager.git
cd task-manager
```

### 2. Создание образов и запуск контейнеров

Убедитесь, что у вас установлен Docker и Docker Compose. Для запуска приложения с использованием Docker Compose выполните команду:


```bash
docker-compose up --build
```

### 3. Доступ к приложению

После запуска контейнеров ваше приложение будет доступно по адресу:

http://localhost:8000