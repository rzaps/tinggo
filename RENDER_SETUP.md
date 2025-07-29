# Настройка деплоя на Render

## Переменные окружения для Render

Добавьте следующие переменные окружения в настройках вашего сервиса на Render:

### Обязательные переменные:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-app-name.onrender.com
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
```

### Настройки безопасности:
```
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Email настройки (опционально):
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Настройки сервиса на Render

1. **Build Command**: `./build.sh`
2. **Start Command**: `gunicorn tinggo.wsgi:application`
3. **Environment**: Python 3.11

## Структура файлов для деплоя

- ✅ `requirements.txt` - зависимости Python
- ✅ `runtime.txt` - версия Python
- ✅ `build.sh` - скрипт сборки
- ✅ `Procfile` - команда запуска
- ✅ `env.example` - пример переменных окружения

## Важные моменты

1. **Supabase**: Убедитесь, что ваш Supabase проект настроен и доступен
2. **Статические файлы**: Собираются автоматически через `build.sh`
3. **Миграции**: Выполняются автоматически при деплое
4. **SSL**: Включен по умолчанию для продакшена

## Проверка деплоя

После деплоя проверьте:
- Главная страница загружается
- Регистрация работает
- Вход работает
- Переключение языков работает
- Статические файлы (CSS) загружаются 