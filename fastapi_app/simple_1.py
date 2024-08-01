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


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
