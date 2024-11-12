import aiohttp
import asyncio

async def register_user():
    url = "http://localhost:8000/auth/register"
    user_data = {
        "username": "test_user",
        "password": "password123"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=user_data) as response:
            if response.status == 200:
                data = await response.json()
                access_token = data.get('access_token')
                print(f"Access Token: {access_token}")
                return access_token
            else:
                print(f"Failed to register: {response.status}")
                return None


async def login_user():
    url = "http://localhost:8000/auth/login"
    login_data = {
        "username": "test_user",
        "password": "password123"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=login_data) as response:
            if response.status == 200:
                data = await response.json()
                access_token = data['access_token']
                refresh_token = data['refresh_token']
                print(f"Access Token: {access_token}")
                print(f"Refresh Token: {refresh_token}")
                return access_token, refresh_token
            else:
                print(f"Failed to login: {response.status}")
                return None, None


async def refresh_token(refresh_token):
    url = "http://localhost:8000/auth/refresh"
    payload = {"refresh_token": refresh_token}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                new_access_token = data['access_token']
                new_refresh_token = data['refresh_token']
                print(f"New Access Token: {new_access_token}")
                print(f"New Refresh Token: {new_refresh_token}")
                return new_access_token, new_refresh_token
            else:
                print(f"Failed to refresh token: {response.status}")
                return None, None


async def create_task(access_token):
    url = "http://localhost:8000/tasks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": False
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=task_data, headers=headers) as response:
            if response.status == 201:
                data = await response.json()
                print(f"Task created: {data}")
            else:
                print(f"Failed to create task: {response.status}")

async def get_tasks(access_token):
    url = "http://localhost:8000/tasks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(f"Tasks: {data}")
            else:
                print(f"Failed to get tasks: {response.status}")


async def update_task(task_id, access_token):
    url = f"http://localhost:8000/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    updated_task_data = {
        "title": "Updated Test Task",
        "description": "Updated task description",
        "status": True
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=updated_task_data, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(f"Task updated: {data}")
            else:
                print(f"Failed to update task: {response.status}")


async def delete_task(task_id, access_token):
    url = f"http://localhost:8000/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Failed to delete task: {response.status}")

async def main():
    access_token = await register_user()
    if access_token:
        # Используем полученный токен для других запросов
        await create_task(access_token)
        await get_tasks(access_token)
        # Допустим, task_id = 1
        await update_task(1, access_token)
        await delete_task(1, access_token)

# Запуск всех запросов
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
