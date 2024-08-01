import uvicorn
from fastapi import FastAPI
import os

import logging
from instrumentation import instrument_logging, instrument_tracing, instrument_metrics


app = FastAPI()
service_name = "fastapi-app"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")

# Instrument tracing
instrument_tracing(app=app, service_name=service_name, otlp_endpoint=otlp_endpoint, excluded_urls="/metrics")

# Instrument logging
handler = instrument_logging(service_name=service_name, otlp_endpoint=otlp_endpoint)

# Attach OTLP handler to root logger
logging.getLogger().addHandler(handler)

# Send test message to log
logging.info(f"{service_name} started, listening on port 8000")

# Instrument metrics
instrument_metrics(app=app)

@app.get("/")
def root_endpoint():
    logging.info("Hello World")
    return {"message": "Hello World"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
