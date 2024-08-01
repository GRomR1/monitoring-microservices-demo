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

Traces out to console
```sh
OTEL_SERVICE_NAME=flask-app \
OTEL_TRACES_EXPORTER=console \
opentelemetry-instrument \
    python3 app.py
```

Only logs out to console
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

Console and otel-collector
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
