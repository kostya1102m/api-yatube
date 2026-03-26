# API Yatube

REST API для социальной сети Yatube — платформы для публикации постов,
комментирования и подписки на авторов.

## Описание

Проект предоставляет программный интерфейс для взаимодействия
с социальной сетью Yatube. Через API можно:

- Создавать, редактировать и удалять публикации
- Просматривать сообщества
- Оставлять комментарии к публикациям
- Подписываться на авторов и просматривать свои подписки

Неаутентифицированные пользователи имеют доступ к API только на чтение.
Исключение — эндпоинт подписок: он доступен только аутентифицированным
пользователям.

## Технологии

- Python 3.14

- Django 6.0

- Django REST Framework

- Djoser + Simple JWT

- drf-spectacular (документация API)

## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-username/api-yatube.git
cd api-yatube
```
2. Создать и активировать виртуальное окружение
```bash
python -m venv .venv

.venv\Scripts\activate
```

3. Установить зависимости
```bash
pip install -r requirements.txt
```
4. Создать файл .env
```bash
echo SECRET_KEY=your-secret-key-here > .env
```
5. Выполнить миграции
```bash
python manage.py migrate
```
6. Создать суперпользователя
```bash
python manage.py createsuperuser
```
7. Запустить сервер
```bash
python manage.py runserver
```
Документация API

После запуска сервера документация доступна по адресам:

```bash
Swagger UI: http://127.0.0.1:8000/swagger/
ReDoc: http://127.0.0.1:8000/redoc/
```