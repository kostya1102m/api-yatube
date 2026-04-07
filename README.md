## Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/kostyam1102/api-yatube.git
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
SECRET_KEY=your-secret-key-here
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