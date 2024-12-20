# Api ServiceDesk

## Технологии использованные в проекте:
* FastApi
* PostgreSQL 
* SQLalchemy
* Docker-compose
____
## Установка
1. Склонировать проект к себе: `https://github.com/Pashckevich227/ServiceDesk.git`
2. В папке backend создать файл .env с содержимым, например
```
POSTGRES_USER="root"
POSTGRES_PASSWORD="root"
POSTGRES_HOST="database"
POSTGRES_DATABASE="postgres"

PGADMIN_DEFAULT_EMAIL="test_login@gmail.com"
PGADMIN_DEFAULT_PASSWORD="123123123"
```
3. Выполнить команду `docker-compose build`
4. Выполнить команду `docker-compose up -d`
5. Открыть в браузере `http://127.0.0.1:8000/docs` (убедиться, что ваши сторонние процессы не занимают порт 8000)

____
## Структура БД создается автоматически при старте проекта и заполняется тестовыми данными
![image](https://github.com/user-attachments/assets/192e0f43-a485-4653-98ef-ac8ce638da24)

____
## Примеры запросов
1. Просмотр всех обращений
![image](https://github.com/user-attachments/assets/059c1cdb-a1c2-41c7-8fc0-9cafef41efc4)

2. Создание нового обращения
![image](https://github.com/user-attachments/assets/95a487a5-8536-4d8b-9d28-3230e7cc64d1)

3. Назначить ответственного на обращение
![image](https://github.com/user-attachments/assets/dbfc46ab-ea62-4b55-b390-b3df11ea3979)

4. Написать сообщение пользователю
![image](https://github.com/user-attachments/assets/e47d9e10-3a5e-4626-af06-1e1a213a378f)

5. Закрыть обращение
![image](https://github.com/user-attachments/assets/a21f19b0-3276-4e27-a3cd-6f46623cb360)



