import uvicorn
from fastapi import FastAPI
import os
import logging

from random import randint
from time import sleep

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = FastAPI()
service_name = "fastapi-app"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")

# https://opentelemetry-python.readthedocs.io/en/latest/exporter/otlp/otlp.html#usage
resource = Resource(attributes={"service.name": service_name})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(service_name)
otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Send test message to log
logging.info(f"{service_name} started, listening on port 8000")

def do_long_processing_job(t):
    sleep(t)


@app.get("/")
def root_endpoint():
    logging.info("Hello World")
    return {"message": "Hello World"}


@app.get("/metrics")
def metrics_endpoint():
    pass


@app.get("/sleep")
def sleep_rand():
    tracer = trace.get_tracer_provider().get_tracer(service_name)
    processing_time = randint(1, 5)
    with tracer.start_as_current_span("do_long_processing_job") as child:
        child.set_attribute("operation.name", "do_long_processing_job")

        child.add_event("Gonna try it!")
        do_long_processing_job()
        child.add_event("Did it!")

        logging.info(f"do_long_processing_job result: {processing_time}")
        child.set_attribute("processing.time", processing_time)
    return {"processing_time": processing_time}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
