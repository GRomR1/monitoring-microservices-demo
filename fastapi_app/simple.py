import logging
import uvicorn
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
)

logging.info("Run FastAPI app")

app = FastAPI()

@app.get("/")
def health_check():
    logging.info("health_check called")
    return {"message": "Hello World"}


@app.get("/error")
def health_check():
    logging.error("error")
    raise HTTPException(status_code=500)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
