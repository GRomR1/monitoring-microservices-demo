# Auto-инструментирование Flask приложения

## Описание

Приложение Flask с автоматической инструментацией OpenTelemetry. Использует автоматическую инструментацию для сбора трассировок, метрик и логов без изменения кода приложения.

## Файлы приложения

### `app.py`
Базовое приложение Flask с единственным эндпоинтом `/`, возвращающим строку "hello-world". Используется как простой пример без внешних зависимостей.

### `app_client.py`
Основное приложение Flask с несколькими эндпоинтами:
- `/` - возвращает "hello-world"
- `/users` - вызывает эндпоинт `/users` сервиса FastAPI для получения списка пользователей
- `/albums` - вызывает эндпоинт `/albums` сервиса Golang для получения списка альбомов
- `/user/<username>` - вызывает сервис FastAPI для получения профиля конкретного пользователя

Использует библиотеку `requests` для выполнения HTTP-запросов к другим сервисам.

## Переменные окружения

Приложение использует следующие переменные окружения:

| Переменная | Описание | Значение по умолчанию |
|------------|----------|------------------------|
| `FASTAPI_URL` | URL сервиса FastAPI | `http://localhost:8000` |
| `GOLANG_URL` | URL сервиса Golang | `http://localhost:8002` |
| `OTEL_SERVICE_NAME` | Имя сервиса для телеметрии | Не задано |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Эндпоинт OTLP для экспорта телеметрии | Не задано |

## Зависимости

Зависимости приложения определены в `requirements.txt`:

- `flask==3.0.3` - веб-фреймворк
- `requests==2.32.3` - HTTP-клиент для выполнения запросов к другим сервисам
- `opentelemetry-distro==0.46b0` - дистрибутив OpenTelemetry
- `opentelemetry-instrumentation==0.46b0` - базовые инструменты инструментации
- `opentelemetry-exporter-otlp==1.25.0` - экспорт телеметрии через OTLP
- `opentelemetry-instrumentation-flask==0.46b0` - инструментация для Flask
- `opentelemetry-instrumentation-requests==0.46b0` - инструментация для requests
- `opentelemetry-instrumentation-logging==0.46b0` - инструментация для логирования
- `opentelemetry-exporter-prometheus==0.46b0` - экспорт метрик в Prometheus

## Docker

Приложение упаковано в Docker-контейнер с использованием Python 3.12 slim в качестве базового образа.

## Инструментация

Приложение использует автоматическую инструментацию OpenTelemetry через команду `opentelemetry-instrument`, которая автоматически инструментирует Flask-приложение и библиотеку requests без изменения кода.

### Примеры запуска

1. Запуск без инструментации:
```sh
python3 app_client.py
```

2. Запуск с инструментацией и выводом трассировок в консоль:
```sh
OTEL_SERVICE_NAME=flask-app \\
OTEL_TRACES_EXPORTER=console \\
opentelemetry-instrument \\
    python3 app_client.py
```

3. Запуск с инструментацией и отправкой телеметрии в OTLP-коллектор:
```sh
OTEL_SERVICE_NAME=flask-app \\
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \\
OTEL_TRACES_EXPORTER=otlp \\
OTEL_METRICS_EXPORTER=otlp \\
OTEL_LOGS_EXPORTER=otlp \\
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \\
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \\
OTEL_PYTHON_LOG_CORRELATION=true \\
opentelemetry-instrument \\
    python3 app_client.py
```

## Тестирование

После запуска приложения можно выполнить тестовый запрос:
```sh
curl localhost:8001
```

Ответ должен быть: `hello-world`

Для тестирования других эндпоинтов:
```sh
# Получение списка пользователей
curl localhost:8001/users

# Получение списка альбомов
curl localhost:8001/albums
```