import uvicorn
from fastapi import FastAPI, HTTPException
import os
import logging

from random import randint
from time import sleep

from instrumentation import instrument_logging, instrument_tracing, instrument_metrics, instrument_database

from sqlmodel import select
from db import engine, Session, create_db_and_tables
from models import Users

app = FastAPI()
service_name = "fastapi-app"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")

# Instrument tracing
tracer = instrument_tracing(app=app, service_name=service_name, otlp_endpoint=otlp_endpoint, excluded_urls="/metrics")

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
        logging.info("wait 10")
        sleep(10)

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


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)
