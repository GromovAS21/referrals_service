# Реферальный сервис

API приложение для управления реферальными кодами с возможностью регистрации, аутентификации и контроля срока действия кодов.

---

## Основные функции

- **Регистрация и аутентификация пользователя**  
  - Поддержка JWT и OAuth 2.0 для безопасной аутентификации.

- **Управление реферальными кодами**  
  - Создание и удаление реферальных кодов.  
  - Одновременно может быть активен только один реферальный код у пользователя.  
  - Контроль срока действия кодов и их автоматическая деактивация.  

- **Поиск реферального кода**  
  - Возможность получения реферального кода по email пользователя.

- **Регистрация по реферальному коду**  
  - Пользователи могут регистрироваться, используя реферальный код.

- **Проверка email**  
  - Интеграция с API Hunter.io для проверки действительности email.

- **Хеширование реферальных кодов**  
  - Использование in-memory БД (Redis) для хеширования реферальных кодов.

- **Получение информации о рефералах**  
  - Возможность получения списка рефералов по ID реферера.

- **Документация API**  
  - UI документация с использованием Swagger.

---

## Технологии и зависимости

- **Язык программирования:** Python 3.12
- **Фреймворк:** Django 5.1.6
- **API:** Django REST Framework 3.15.2
- **База данных:** PostgreSQL (psycopg2-binary 2.9.10)
- **Аутентификация:** JWT (djangorestframework-simplejwt 5.4.0)
- **Кеширование:** Redis (redis 5.2.1, django-redis 5.4.0)
- **Планировщик задач:** Celery (celery 5.4.0, django-celery-beat 2.7.0)
- **Документация:** Swagger (drf-yasg 1.21.8)
- **Дополнительно:**  
  - python-dotenv 1.0.1 (для работы с переменными окружения)  
  - requests 2.32.3 (для работы с внешними API)

---

## Установка и запуск

### Локальный запуск

1. **Клонирование репозитория**  
   ```bash
   git clone https://github.com/GromovAS21/referrals_service.git
   cd referrals_service
   ```
2. **Установка зависимостей**
- Установите зависимости с помощью Poetry и активируйте виртуальное окружение:
  ```bash
  poetry install
  poetry shell
  ```
3. **Настройка переменных окружения**
- Переименуйте файл [.env.sample](.env.sample) в [.env](.env.sample) и заполните необходимые данные.
- Получите API Key на HUNTER API и добавьте его в переменную `HUNTER_API_KEY`.

4. **Миграции и заполнение базы данных**
     ```bash
     python3 manage.py makemigrations
     python3 manage.py migrate
     python3 manage.py csu  # Создание суперпользователя
     python3 manage.py cu   # Создание тестовых пользователей
     python3 manage.py crc  # Создание тестовых реферальных кодов
     ```
5. **Запуск Redis и Celery**
     ```bash
   redis-server
   celery -A config worker --beat --scheduler django --loglevel=info
     ```
6. **Запуск локального сервера**
     ```bash
   python3 manage.py runserver
     ```
   
#### Приложение будет доступно по адресу: http://127.0.0.1:8000
   
### Запуск с использованием Docker

1. **Запуск контейнеров**
- Убедитесь, что Docker установлен и запущен. Затем выполните:
  ```bash
  docker-compose up -d --build
  ```
  
#### Приложение будет доступно по адресу: http://0.0.0.0:8000

---

## Валидация данных

### Создание пользователя
- **Email**: Проверка на корректность и существование.
- **Пароль**: Длина не менее 8 символов.
- **Реферальный код**: Должен быть действующим при регистрации.

### Создание реферального кода
- **Формат**: 6 цифр, без букв.
- **Срок действия**: Обязателен к указанию.
- **Дата**: Не должна быть в прошлом.

### Удаление реферального кода
- **Владелец**: Текущий пользователь должен быть владельцем кода.

---

## Документация API
Документация API доступна по эндпоинту `swagger/`.

---

## Тесты
Покрытие тестов составляет 95%

**Запуск Тестов**
```bash 
poetry run coverage run manage.py test
poetry run coverage report
```

---

## Pre-commit
В проекте присутсвует функция pre-commit, которая проверяет код на соответствие стандартам PEP8 состоящие из isort, black, flake8;

**Запуск Pre-commit**
```bash
pre-commit install
git add .pre-commit-config.yaml
```
После этого при попытке создания коммита будет запускаться проверка кода и если все проверки проходят, создается коммит.

Для ручной проверки кода необходимо выполнить команду:
```bash
pre-commit run --all-files
```

#### ВАЖНО!!! ####
Перед коммитом необходимо выполнить одну из следующих команд:
```bash
git add . # Добавляет все файлы в индекс
git add <file_name> # Добавляет указанный файл в индекс
```

---

## Цитата
>"Чтобы понять код мида, нужно быть мидом. Чтобы понять код сеньора, достаточно быть джуном."* - Гейб Логан Ньюэлл

---

Приятного использования! 🚀
  
