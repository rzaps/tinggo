# Исправление проблемы с деплоем на Render

## Проблема
Render пытается запустить `gunicorn app:app` вместо правильной команды.

## Решение

### Вариант 1: Использовать render.yaml (рекомендуется)
1. Убедитесь, что файл `render.yaml` есть в репозитории
2. В настройках Render выберите "Use render.yaml"
3. Render автоматически использует правильные команды

### Вариант 2: Настроить вручную
В настройках сервиса на Render:

**Build Command:**
```
./build.sh
```

**Start Command:**
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

### Вариант 3: Использовать wsgi.py
Альтернативная команда:
```
gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

## Переменные окружения
Убедитесь, что добавлены все необходимые переменные:

```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-app-name.onrender.com
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
```

## Проверка
После исправления:
1. Деплой должен пройти успешно
2. Приложение должно запуститься
3. Статические файлы должны загружаться 