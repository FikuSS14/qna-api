# Q&A API

Тестовое задание: API-сервис для вопросов и ответов.  
**Полностью self-contained: достаточно `git clone && docker-compose up` — и всё работает.**

> Соответствует ТЗ: Django, ORM, PostgreSQL, Docker, миграции, тесты, каскадное удаление.  
> Работает «из коробки» - проверено на чистой машине.

---

## Структура проекта
qna-api/ 
├── .env.example # образец .env 
├── .gitignore
├── Dockerfile # сборка Django-приложения
├── docker-compose.yml # запуск БД + backend
├── requirements.txt
├── manage.py
├── qna/ # Django config
├── questions/ # Приложение: модели, views, тесты
└──tests/integration/ # Интеграционные тесты (requests)

---

## Быстрый старт (проверено на Windows)
# Установите зависимости для тестов
pip install -r requirements.txt
### Клонируйте репозиторий
git clone https://github.com/FikuSS14/qna-api.git
cd qna-api
### Создайте .env из шаблона
Copy-Item .env.example .env
### Запустите проект
docker-compose up --build

---

### При запуске docker-compose:

db создаёт БД,
qna_docker с юзером qna_user,
web наследует переменные через environment в docker-compose.yml

Миграции применяются автоматически при старте (command),
Нет необходимости вручную запускать migrate.

Проверьте, что API отвечает
В новом терминале (пока docker-compose up работает):

---

### Проверить АПИ можно: 
- Через REST Client, файл для теста api.http
- Postman
- Либо через pytest + requests, файл test_api.py, запуск pytest tests/integration/ -v
Установить REST
Зайти в файл api.http и нажимать на Send Request на каждом запросе

---

# Тестирование
### Запустить тесты в изолированной среде
docker-compose run --rm web python manage.py test
- Тесты проверяют: 
- каскадное удаление,
- валидацию несуществующего вопроса,
- UUID-формат user_id.

---

# Остановить контейнеры (данные БД сохраняются)
docker-compose down

# Полный сброс (включая БД)
docker-compose down -v

---