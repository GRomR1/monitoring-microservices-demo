import uvicorn
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
import os
import logging

from random import randint
from time import sleep
import time

from instrumentation import (
    instrument_logging,
    instrument_tracing,
    instrument_metrics,
    instrument_database,
    instrument_profiling,
)

from sqlmodel import select
from db import engine, Session, create_db_and_tables
from models import Users
import pyroscope
from opentelemetry import trace
from opentelemetry.trace import format_trace_id

service_name = "fastapi-app"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")
pyroscope_endpoint = os.environ.get("PYROSCOPE_ENDPOINT", "http://localhost:4040")


class PyroscopeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        trace_id = format_trace_id(trace.get_current_span().get_span_context().trace_id)
        with pyroscope.tag_wrapper({"endpoint": path, "trace_id": trace_id}):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
        return response


app = FastAPI()
app.add_middleware(PyroscopeMiddleware)

pyroscope.configure(
    application_name=service_name,
    server_address=pyroscope_endpoint,
    enable_logging=True,
)

# Instrument tracing
tracer = instrument_tracing(
    app=app,
    service_name=service_name,
    otlp_endpoint=otlp_endpoint,
    excluded_urls="/metrics",
)

# Instrument profiling
tracer = instrument_profiling(tracer=tracer)

# Instrument logging
handler = instrument_logging(service_name=service_name, otlp_endpoint=otlp_endpoint)

# Attach OTLP handler to root logger
logging.getLogger().addHandler(handler)

# Send test message to log
logging.info(f"{service_name} started, listening on port 8000")

# Instrument metrics
instrument_metrics(app=app)

# Instrument database
instrument_database(engine=engine, tracer=tracer)

# Create database and tables in database
create_db_and_tables()


@app.get("/")
def root_endpoint():
    logging.info("Hello World")
    return {"message": "Hello World"}


@app.get("/users", response_model=list[Users])
def read_users():
    a = randint(1, 10)

    ### sleep 10 seconds in 10% of cases
    if a == 10:
        logging.warning("this is a long long operation")
        do_long_work(10)

    ### emit HTTPException in 10% of cases
    if a == 9:
        logging.error("error")
        raise HTTPException(
            status_code=500, detail="HTTPException emmited in read_users method"
        )

    #### get users
    with Session(engine) as session:
        users = session.exec(select(Users)).all()
        return users


@app.get("/do_long_work")  # /do_long_work?sec=10
def do_long_work(sec: int = 0):
    x = randint(1000, 10000)
    timeout = time.time() + float(sec)
    while True:
        if time.time() > timeout:
            break
        x * x
    return {"worked_seconds": sec}


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)
