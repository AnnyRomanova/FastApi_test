# FastApi - Учебный проект

## Установка:
### 1. `pip install -r requirements.txt`


### 2. Необходимо создать файл .env c содержимым:


####   Postgres

`POSTGRES_DB=FAT_db4`

`POSTGRES_USER=user`

`POSTGRES_PASSWORD=password`

####  Service

`APP_NAME=Magazine articles`

`DB__HOST=localhost`

`DB__PORT=5431`

`DB__USER=user`

`DB__PASSWORD=password`

`DB__DB=FAT_db4`



### 3. Для запуска в Docker
#### `docker-compose build`

#### `docker-compose up -d`


### 4. Для заполнения базы данных

`alembic upgrade head`