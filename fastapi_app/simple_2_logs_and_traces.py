import uvicorn
from fastapi import FastAPI
import os

import logging
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace, _logs

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import \
    OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

app = FastAPI()
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")

# set the tracer provider
resource = Resource.create(attributes={"service.name": "fastapi_app"})
tracer = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer)

# trace_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace_processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=OTLP_GRPC_ENDPOINT, insecure=True)
)
tracer.add_span_processor(trace_processor)

# instrument
FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer, excluded_urls="/metrics")

# Initialize Logs
# set the logger provider
logger_provider = LoggerProvider(resource=resource)
_logs.set_logger_provider(logger_provider)
log_processor = BatchLogRecordProcessor(
    OTLPLogExporter(endpoint=OTLP_GRPC_ENDPOINT, insecure=True)
)
logger_provider.add_log_record_processor(log_processor)

# Attach OTLP handler to logger
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
logger = logging.getLogger("main")
logger.addHandler(handler)
logger.info(f"Recommendation service started, listening on port 8000")

# instrument
LoggingInstrumentor().instrument(set_logging_format=True)

@app.get("/")
def health_check():
    logger.info("Hello World")
    return {"message": "Hello World"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
