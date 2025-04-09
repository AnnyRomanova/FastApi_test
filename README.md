<div id="header" align="left">
  <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExemQyMTlwcXByN3pybWNleWFoZG9tMnVucDYwMmFwMTQyb3R5aWxqdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1Sylk43T3fTSB3pGd0/giphy.gif" width="100"/>
</div>

# PostKeeper - мини-API для хранения и управления статьями

### :pencil2: Быстрый и удобный сервис на FastAPI для работы с текстовыми материалами.  
### :incoming_envelope: Позволяет создавать, читать, обновлять и удалять статьи.

### :hammer_and_wrench: Технологии:
<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original-wordmark.svg" title="FastAPI" alt="FastAPI" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pytest/pytest-original-wordmark.svg" title="Pytest" alt="Pytest" width="40" height="40"/>&nbsp;  
  <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="PostgreSQL" alt="PostgreSQL" width="40" height="40"/>&nbsp;  
  <img src="https://github.com/devicons/devicon/blob/master/icons/sqlalchemy/sqlalchemy-original-wordmark.svg" title="SQLAlchemy" alt="SQLAlchemy" width="40" height="40"/>&nbsp;  
  <img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original-wordmark.svg" title="Git" alt="Git" width="40" height="40"/>
</div>

## Установка:
### 1. `pip install -r requirements.txt`


### 2. Необходимо создать файл .env c содержимым:


####   Postgres

`POSTGRES_DB=FAT_db4`

`POSTGRES_USER=your_username`

`POSTGRES_PASSWORD=your_password`

####  Service

`APP_NAME=Magazine articles`

`DB__HOST=localhost`

`DB__PORT=5431`

`DB__USER=your_username`

`DB__PASSWORD=your_password`

`DB__DB=FAT_db4`



### 3. Для запуска в Docker
#### `docker-compose build`

#### `docker-compose up -d`


### 4. Для заполнения базы данных
#### В проекте есть файлы миграций для создания и заполнения таблиц в БД
`alembic upgrade head`