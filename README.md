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

Сначала клонируйте репозиторий с GitHub (или другого источника) на ваш локальный компьютер.

```bash
git clone https://github.com/your-repository/task-manager.git
cd task-manager