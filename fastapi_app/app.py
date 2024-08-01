import uvicorn
from fastapi import FastAPI

import logging
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
)

app = FastAPI()
service_name = "fastapi-app"
logging.info(f"{service_name} started, listening on port 8000")


@app.get("/")
def root_endpoint():
    logging.info("Hello World")
    return {"message": "Hello World"}


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)
