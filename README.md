# Проект «API для Yamdb»

## Описание проекта

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории и жанры.

Пользователи оставляют к произведениям текстовые отзывы и ставят оценку. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
Пользователи могут оставлять комментарии к отзывам.

## Технологии

* Python 3.9.12
* Django 3.2.18
* Django REST framework 3.12.4
* SQLite

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:RocketCookie/api_yamdb.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры эндпойтнов

* /api/v1/auth/signup/ (POST): *регистрация нового пользователя.*
* /api/v1/auth/token/ (POST): *получение jwt-токена.*
* /api/v1/categories/ (GET): *Получение списка всех категорий.*
* /api/v1/genres/ (GET, POST): *получение списка всех жанров или создание нового жанра.*
* /api/v1/genres/ (GET, PUT, PATCH, DELETE): *получение, редактирование или удаление произведения.*
* /api/v1/titles/{title_id}/reviews/ (GET): *Получение списка всех отзывов.*
* /api/v1/titles/{title_id}/reviews/ (POST): Добавление нового отзыва*
* /api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, POST): *получение списка всех комментариев к отзыву по id или создание нового комментария.*
* /api/v1/users/ (GET): *Получение списка всех пользователей.*

Более подробная документация доступна в Redoc

```
/redoc/
```

## Примеры ответа от сервера

* POST-запрос: Регистрация нового пользователя. Получить код подтверждения на переданный email.

```
{
    "email": "user@example.com",
    "username": "string"
} 
```

Ответ:

```
{
    "email": "string",
    "username": "string"
}
```

* GET-запрос: Получение списка всех категорий.

Ответ:

```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
    + {}
    ]
} 

```

* POST-запрос: Добавление произведения.

```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

Ответ:

```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

### Авторы

Олег Гуров  
Марина Богатырева  
Анастасия Ладыгина
