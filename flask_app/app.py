import logging
from flask import Flask

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route("/")
def index():
    logger.info("hello-world")
    return "hello-world"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
