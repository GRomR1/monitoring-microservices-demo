# Auto-instrumentation Flask App

## Packages

Install pip reqired packages. Create `requirements.txt`:
```
flask==3.0.3
requests==2.32.3
opentelemetry-distro==0.46b0
opentelemetry-instrumentation==0.46b0
opentelemetry-exporter-otlp==1.25.0
opentelemetry-instrumentation-flask==0.46b0
opentelemetry-instrumentation-requests==0.46b0
opentelemetry-instrumentation-logging==0.46b0
opentelemetry-exporter-prometheus==0.46b0
```

## Environment vars

`OTEL_SERVICE_NAME`: The name of the service generating the telemetry data.

`OTEL_LOGS_EXPORTER`: The logs exporter to use, In this doc we're using the console exporter. If you have an opentelemetry collector set up, you can change this variable's value to console,otlp or just otlp. You will also have to set the OTEL_EXPORTER_OTLP_ENDPOINT variable to the endpoint of your opentelemetry collector.

`OTEL_TRACES_EXPORTER`: The traces exporter to use, In this doc we're using the console exporter. If you have an opentelemetry collector set up, you can change this variable's value to console,otlp or just otlp. You will also have to set the OTEL_EXPORTER_OTLP_ENDPOINT variable to the endpoint of your opentelemetry collector.

`OTEL_METRICS_EXPORTER`: The metrics exporter to use, In this doc we're using the console exporter. If you have an opentelemetry collector set up, you can change this variable's value to console,otlp or just otlp. You will also have to set the OTEL_EXPORTER_OTLP_ENDPOINT variable to the endpoint of your opentelemetry collector.

`OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED`: This variable enables auto-instrumentation for the logging module.

# Running


Simple running only web-server (without instrumentation)
```sh
python3 app.py
```

## Instrumentate application

Use some different methods to control what information need to be returned.

1. Only traces out to console
```sh
OTEL_SERVICE_NAME=flask-app \
OTEL_TRACES_EXPORTER=console \
opentelemetry-instrument \
    python3 app.py
```

2. Only logs out to console
```sh
OTEL_SERVICE_NAME=flask-app \
OTEL_TRACES_EXPORTER=none \
OTEL_METRICS_EXPORTER=none \
OTEL_LOGS_EXPORTER=console \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
OTEL_PYTHON_LOG_CORRELATION=true \
OTEL_PYTHON_LOG_LEVEL=debug \
opentelemetry-instrument \
    python3 app.py
```

3. Logs and traces out to console
```sh
OTEL_SERVICE_NAME=flask-app \
OTEL_TRACES_EXPORTER=console \
OTEL_METRICS_EXPORTER=none \
OTEL_LOGS_EXPORTER=console \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
OTEL_PYTHON_LOG_CORRELATION=true \
OTEL_PYTHON_LOG_LEVEL=debug \
opentelemetry-instrument \
    python3 app.py
```

4. Console and otel-collector
```sh
OTEL_SERVICE_NAME=flask-app \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
OTEL_TRACES_EXPORTER=console,otlp \
OTEL_METRICS_EXPORTER=console,otlp \
OTEL_LOGS_EXPORTER=console,otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
OTEL_PYTHON_LOG_CORRELATION=true \
opentelemetry-instrument \
    python3 app.py
```

# Testing

Run http-request via curl command after running application.
```sh
❯ curl localhost:8001
hello-world%
```

You will see the log on aplication about requested endpoint:
```json
{
    "body": "127.0.0.1 - - [24/Aug/2024 21:47:20] \"GET / HTTP/1.1\" 200 -",
    "severity_number": "<SeverityNumber.INFO: 9>",
    "severity_text": "INFO",
    "attributes": {
        "otelSpanID": "0",
        "otelTraceID": "0",
        "otelTraceSampled": false,
        "otelServiceName": "flask-app",
        "code.filepath": "./docker-tracing-demo/flask_app/.venv/lib/python3.12/site-packages/werkzeug/_internal.py",
        "code.function": "_log",
        "code.lineno": 97
    },
    "dropped_attributes": 0,
    "timestamp": "2024-08-24T18:47:20.480531Z",
    "observed_timestamp": "2024-08-24T18:47:20.480546Z",
    "trace_id": "0x00000000000000000000000000000000",
    "span_id": "0x0000000000000000",
    "trace_flags": 0,
    "resource": "{'telemetry.sdk.language': 'python', 'telemetry.sdk.name': 'opentelemetry', 'telemetry.sdk.version': '1.25.0', 'service.name': 'flask-app', 'telemetry.auto.version': '0.46b0'}"
}
```

Or this result if application will run with traces enabled:
```json
{
    "body": "hello-world",
    "severity_number": "<SeverityNumber.INFO: 9>",
    "severity_text": "INFO",
    "attributes": {
        "otelSpanID": "f296a5fd627ea074",
        "otelTraceID": "7ea0f1afc744150ffc7bb451d1906cf0",
        "otelTraceSampled": true,
        "otelServiceName": "flask-app",
        "code.filepath": "./docker-tracing-demo/flask_app/app.py",
        "code.function": "index",
        "code.lineno": 11
    },
    "dropped_attributes": 0,
    "timestamp": "2024-08-24T18:52:11.966384Z",
    "observed_timestamp": "2024-08-24T18:52:11.966427Z",
    "trace_id": "0x7ea0f1afc744150ffc7bb451d1906cf0",
    "span_id": "0xf296a5fd627ea074",
    "trace_flags": 1,
    "resource": "{'telemetry.sdk.language': 'python', 'telemetry.sdk.name': 'opentelemetry', 'telemetry.sdk.version': '1.25.0', 'service.name': 'flask-app', 'telemetry.auto.version': '0.46b0'}"
}
```