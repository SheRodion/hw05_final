# Проект "Yatube" (учебный проект)

### Описание
Социальная сеть Yatube, дающая пользователям возможность создать учетную запись, публиковать записи, подписываться на любимых авторов и отмечать понравившиеся записи.
В проекте реализована регистрация пользователей с верификацией данных, сменой и восстановлением пароля через email. Построены пагинация постов, кеширование, возможность публикации записей в различных группах, редактирование записей. 
## Сервис позволяет:

- регистрироваться, восстанавливать пароль по почте
- создавать личную страницу, для публикации записей
- создавать и редактировать свои записи
- просматривать страницы других авторов
- комментировать записи других авторов
- подписываться на авторов
- записи можно отправлять в определённую группу
- модерация записей, работа с пользователями, создание групп осуществляется через панель администратора
### Технологии
* Django==2.2.19
* pytz==2021.3
* sqlparse==0.4.2
### Запуск проекта в dev-режиме
- Слонируйте проект из github
- Установите и активируйте виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate
``` 
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```
