import logging
from flask import (
    Flask
)

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route("/")
def index():
    logger.info("hello-word")
    return "hello-word"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
