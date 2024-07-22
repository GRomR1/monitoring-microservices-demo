# Auto-instrumentation Flask App

# Links
https://github.com/rutu-sh/otel-k8s-experiments/tree/main/common-applications/auto-instrumented/python/simple-fastapi-app/docs

# Environment vars

OTEL_SERVICE_NAME: The name of the service generating the telemetry data.

OTEL_LOGS_EXPORTER: The logs exporter to use, In this doc we're using the console exporter. If you have an opentelemetry collector set up, you can change this variable's value to console,otlp or just otlp. You will also have to set the OTEL_EXPORTER_OTLP_ENDPOINT variable to the endpoint of your opentelemetry collector.

OTEL_TRACES_EXPORTER: The traces exporter to use, In this doc we're using the console exporter. If you have an opentelemetry collector set up, you can change this variable's value to console,otlp or just otlp. You will also have to set the OTEL_EXPORTER_OTLP_ENDPOINT variable to the endpoint of your opentelemetry collector.

OTEL_METRICS_EXPORTER: The metrics exporter to use, In this doc we're using the console exporter. If you have an opentelemetry collector set up, you can change this variable's value to console,otlp or just otlp. You will also have to set the OTEL_EXPORTER_OTLP_ENDPOINT variable to the endpoint of your opentelemetry collector.

OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED: This variable enables auto-instrumentation for the logging module.

Capture HTTP request and response headers
You can capture predefined HTTP headers as span attributes, according to the semantic convention.

To define which HTTP headers you want to capture, provide a comma-separated list of HTTP header names via the environment variables OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST and OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE, e.g.:

export OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST="Accept-Encoding,User-Agent,Referer"

# Running

Traces,logs,metrics out to console
```sh
OTEL_SERVICE_NAME=demo-application \
OTEL_TRACES_EXPORTER=console \
OTEL_METRICS_EXPORTER=console \
OTEL_LOGS_EXPORTER=console \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
opentelemetry-instrument \
    python3 simple.py
```

Only logs out to console
```sh
OTEL_SERVICE_NAME=demo-application \
OTEL_TRACES_EXPORTER=none \
OTEL_METRICS_EXPORTER=none \
OTEL_LOGS_EXPORTER=console \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
OTEL_PYTHON_LOG_CORRELATION=true \
OTEL_PYTHON_LOG_LEVEL=debug \
opentelemetry-instrument \
    python3 simple.py
```

Console and otel-collector
```sh
OTEL_SERVICE_NAME=demo-application \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
OTEL_TRACES_EXPORTER=console,otlp \
OTEL_METRICS_EXPORTER=console,otlp \
OTEL_LOGS_EXPORTER=console,otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
OTEL_PYTHON_LOG_CORRELATION=true \
opentelemetry-instrument \
    python3 simple.py
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
    python3 simple.py
```


OTEL_PYTHON_FASTAPI_EXCLUDED_URLS": "/healthzz"