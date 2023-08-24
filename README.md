<h2>EGRUL (Тестовое задание)</h2>

- Программа читает файл Единого государственного реестр юридических лиц, выбирает компании, занимающиеся разработкой программного обеспечения (Группировка ОКВЭД 62), зарегистрированные в г. Хабаровск и записывает информацию о выбранных компаниях (название компании, код ОКВЭД, ИНН, КПП и место регистрации ЮЛ) в базу данных.

<h2>Требования</h2>

- python 3.11
- fastapi
- tortoise-orm
- postgresql
- uvicorn
- docker

Зависимости можно установить через: pip install -r requirements.txt 

<h2>Процесс развёртывания (деплоя) на сервере</h2>

1. Установить (для Ubuntu):

- Docker:
    - sudo apt update
    - sudo apt install apt-transport-https ca-certificates curl software-properties-common
    - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    - sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
    - sudo apt update
    - apt-cache policy docker-ce
    - sudo apt install docker-ce

- Docker-compose:
    - sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    - sudo chmod +x /usr/local/bin/docker-compose

2. Создать файл .env в директории ./insurance_cost и заполнить переменные окружения, где: 

- DB_USER={логин пользователя PostgreSQL}
- DB_PASSWORD={пароль от пользователя PostgreSQL}
- DB_NAME={название БД в PostgreSQL}
- DB_PATH={путь для доступа к БД - postgresql://login:password@ip:port/dbname}
- DB_PATH_TORTOISE={путь для Tortoise-ORM - asyncpg://login:password@ip:port/dbname}


3. Запустить команду: docker-compose -f docker-compose-app.yaml up -d из директории ./insurance_cost

<h2>Эксплуатация:</h2>

1. GET /v1/load_rates_in_database - метод для загрузки данных по тарифам из JSON файла в БД (по умолчанию БД пустая)
2. GET /v1/get_insurance_cost - метод для расчёта стоимости страховки

