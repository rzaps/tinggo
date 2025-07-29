# TingGo - Культурная платформа мероприятий

TingGo — это культурно насыщенная платформа мероприятий, объединяющая и продвигающая карибские и латиноамериканские сообщества за пределами границ.

## 🚀 Быстрый старт

### Локальная разработка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd tinggo
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения:**
Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

5. **Отредактируйте файл `.env` и укажите ваши реальные значения:**
- `SECRET_KEY` - сгенерируйте новый ключ: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `SUPABASE_URL` и `SUPABASE_KEY` - из вашего проекта Supabase (это основная база данных)
- Остальные настройки оставьте по умолчанию для разработки

6. **Выполните миграции:**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Создайте суперпользователя:**
```bash
python manage.py createsuperuser
```

8. **Соберите статические файлы:**
```bash
python manage.py tailwind build
```

9. **Запустите сервер:**
```bash
python manage.py runserver
```

### Деплой на Render

1. **Создайте аккаунт на [Render](https://render.com/)**

2. **Подключите репозиторий GitHub**

3. **Создайте новый Web Service**

4. **Настройте переменные окружения:**
   - `DEBUG`: `False`
   - `SECRET_KEY`: сгенерируйте новый секретный ключ
   - `ALLOWED_HOSTS`: ваш домен на Render
   - `SUPABASE_URL`: ваш URL Supabase
   - `SUPABASE_KEY`: ваш ключ Supabase

5. **Настройте Build Command:**
```bash
chmod +x build.sh && ./build.sh
```

6. **Настройте Start Command:**
```bash
gunicorn tinggo.wsgi:application
```

**Примечание:** Проект автоматически использует `build.sh` для установки зависимостей и сборки статических файлов.

## 🏗️ Структура проекта

```
tinggo/
├── accounts/          # Пользователи и аутентификация
├── theme/            # Tailwind CSS тема
├── templates/        # HTML шаблоны
├── tinggo/           # Основные настройки Django
├── static/           # Статические файлы
├── media/            # Загружаемые файлы
└── requirements.txt  # Зависимости Python
```

## 🌍 Мультиязычность

Проект поддерживает 3 языка:
- **English** (en) - основной язык
- **Español** (es) - испанский
- **Kreyòl Ayisyen** (ht) - гаитянский креольский

### Структура переводов
```
locale/
├── en/LC_MESSAGES/django.po  # Английский
├── es/LC_MESSAGES/django.po  # Испанский
└── ht/LC_MESSAGES/django.po  # Гаитянский креольский
```

### Переключение языков
- Используйте переключатель языков в навигации
- Или добавьте параметр `?lang=es` к URL

### Компиляция переводов (для продакшена)
```bash
# Установите gettext
# Windows: скачайте с https://mlocati.github.io/articles/gettext-iconv-windows.html
# Linux: sudo apt-get install gettext
# Mac: brew install gettext

# Скомпилируйте переводы
python manage.py compilemessages
```

## 🎨 Технологии

- **Backend**: Django 5.2
- **Frontend**: Tailwind CSS + DaisyUI
- **База данных**: Supabase (PostgreSQL)
- **Аутентификация**: Django Allauth
- **Деплой**: Render

## 🔄 Supabase Интеграция

Платформа использует Supabase для аутентификации и хранения данных:

- **Регистрация** - пользователь создается в Supabase Auth и Django
- **Вход** - аутентификация через Supabase Auth
- **Сброс пароля** - отправка email через Supabase
- **Профили** - синхронизация с таблицей user_profiles в Supabase

### Настройка Supabase

1. Создайте таблицу `user_profiles` в Supabase:
```sql
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    role VARCHAR(20),
    country VARCHAR(100),
    city VARCHAR(100),
    language VARCHAR(10),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

2. Укажите `SUPABASE_URL` и `SUPABASE_KEY` в файле `.env`

## 👥 Роли пользователей

- **Admin**: Администратор платформы
- **Organizer**: Организатор мероприятий
- **Participant**: Участник мероприятий
- **Vendor**: Поставщик товаров/услуг
- **Host**: Хост впечатлений

## 🌐 Мультиязычность

Поддерживаемые языки:
- English
- Español
- Kreyòl Ayisyen

## 🔧 Разработка

### Сборка CSS
```bash
python manage.py tailwind build
```

### Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание переводов
```bash
python manage.py makemessages -l es
python manage.py makemessages -l ht
python manage.py compilemessages
```

## 📝 Лицензия

MIT License

