import uvicorn
from fastapi import FastAPI, HTTPException
import os

from random import randint
from time import sleep

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace, _logs

import logging
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import \
    OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from opentelemetry import metrics
from prometheus_fastapi_instrumentator import Instrumentator as MetricsInstrumentator

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db import engine, Session, create_db_and_tables
from models import Users
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

app = FastAPI()
service_name = "fastapi-app"
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")

# set the tracer provider
resource = Resource.create(attributes={"service.name": service_name})
tracer = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer)

# trace_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace_processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=OTLP_GRPC_ENDPOINT, insecure=True)
)
tracer.add_span_processor(trace_processor)

# instrument
FastAPIInstrumentor.instrument_app(
    app, tracer_provider=tracer, excluded_urls="/metrics"
)


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
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Attach OTLP handler to root logger
logging.getLogger().addHandler(handler)

# Send test message to log
logger.info(f"{service_name} started, listening on port 8000")

# instrument
LoggingInstrumentor().instrument(set_logging_format=True)

# metrics
meter = metrics.get_meter_provider().get_meter(service_name)
MetricsInstrumentator(excluded_handlers=["/metrics"]).instrument(app).expose(app)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

# Database connect
create_db_and_tables()
SQLAlchemyInstrumentor().instrument(
    engine=engine, enable_commenter=True, commenter_options={}
)

@app.get("/")
def health_check():
    logger.info("Hello World")
    return {"message": "Hello World"}

def do_long_processing_job():
    t = randint(1, 5)
    sleep(t)
    return t

@app.get("/sleep")
def sleep_rand():
    tracer = trace.get_tracer_provider().get_tracer(service_name)
    processing_time = None
    with tracer.start_as_current_span("sleep"):
        processing_time = do_long_processing_job()
        logger.info(f"do_long_processing_job result: {processing_time}")
        current_span = trace.get_current_span()
        current_span.set_attribute("processing.time", processing_time)
    return {"processing_time": processing_time}


@app.get("/users", response_model=list[Users])
def read_users():
    # # in 20% of cases
    # if randint(1, 5) == 5:
    #     # wait 30 seconds
    #     r = randint(1, 2)
    #     if r == 2:
    #         # sleep(10) in 10% of cases
    #         sleep(10)
    #     else:
    #         # emit HTTPException in 10% of cases
    #         raise HTTPException(status_code=500)
    # emit HTTPException in 10% of cases
    if randint(1, 10) == 10:
        logging.error("error")
        raise HTTPException(
            status_code=500, detail="HTTPException emmited in read_users method"
        )
    # get users
    with Session(engine) as session:
        users = session.exec(select(Users)).all()
        return users


@app.get("/users/")
def get_users_by_name(name: str):
    with Session(engine) as session:
        users = session.exec(select(Users).where(Users.name == name)).all()
        return users


@app.get("/users/{user_id}")
def get_users_by_id(user_id: int):
    with Session(engine) as session:
        users = session.exec(select(Users).where(Users.id == user_id)).all()
        return users


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
