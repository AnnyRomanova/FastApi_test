# FastApi - Учебный проект

## Установка:
### 1. `pip install -r my_requirements.txt`


### 2. Необходимо создать файл .env c содержимым:
####   `APP_NAME=Magazine articles`
####   `POSTGRES_DB_USER=Anna`
####   `POSTGRES_DB_PASSWORD=12345`


### 3. Для запуска в Docker
#### `docker run --rm --env APP_NAME='Magazine articles' --name mycontainer -p 8000:8000 myimage`