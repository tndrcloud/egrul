<h2>EGRUL (Тестовое задание)</h2>

- Программа читает файл Единого государственного реестр юридических лиц, выбирает компании, занимающиеся разработкой программного обеспечения (Группировка ОКВЭД 62), зарегистрированные в г. Хабаровск и записывает информацию о выбранных компаниях (название компании, код ОКВЭД, ИНН, КПП и место регистрации ЮЛ) в базу данных.

<h2>Требования</h2>

- python 3.11
- postgresql
- sqlalchemy
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

2. Создать файл .env в директории ./egrul по примеру (.env.example) и заполнить переменные окружения, где: 

- DB_USER={логин пользователя PostgreSQL}
- DB_PASSWORD={пароль от пользователя PostgreSQL}
- DB_NAME={название БД в PostgreSQL}
- DB_PATH={путь для доступа к БД - postgresql://login:password@ip:port/dbname}

3. Добавить архив в корневой каталог

4. Запустить команду: docker-compose -f docker-compose.yaml up -d из директории ./egrul

<h2>Эксплуатация</h2>

1. Заменить при необходимости данные в файле app/settings.py, где:
    - ARCHIVE: название архива для распаковки
    - UNPACK_FILES_COUNT: кол-во одновременно распаковываемых файлов из архива
    - NAME_CITY: нужный город для сортировки (в верхнем регистре)
    - CODE: код ОКВЭД 

2. После деплоя приложения оно автоматически добавит результат проверки архива в БД.

3. Чтобы проверить другой архив, нужно добавить его в корневую директорию проекта и выполнить следующие команды:
    (Пересборка образа и деплой)
    - docker stop app
    - docker rm app
    - docker rmi app
    - docker-compose -f docker-compose.yaml up -d

<h2>Примечания</h2>

Если разворачивать само приложение в контейнере не нужно, то можно убрать блок app из docker-compose.yaml и запускать приложение через консоль командой - python main.py (предварительно активировав виртуальное окружение командой source venv/bin/activate).
