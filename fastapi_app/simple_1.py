import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check():
    return {"message": "Hello World"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
