import json
import logging
import os
import sys
import warnings

# import logging_loki
from dotenv import find_dotenv, load_dotenv
import aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# load environment variables
load_dotenv(find_dotenv(), verbose=True)
sql_uri = os.environ.get("sql_uri")
splitwise_url = os.environ.get("splitwise_url")
splitwise_api_key = os.environ.get("splitwise_api_key")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Splitwise URL: {splitwise_url}")


# create application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


file_handler = logging.FileHandler(filename="logs/error.log", mode="a")
stream_handler = logging.StreamHandler(sys.stdout)

# log formatting
formatter = logging.Formatter(
    json.dumps(
        {
            "ts": "%(asctime)s",
            "name": "%(name)s",
            "function": "%(funcName)s",
            "level": "%(levelname)s",
            "msg": json.dumps("%(message)s"),
        }
    )
)


file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

handlers = [file_handler, stream_handler]

logging.basicConfig(level=logging.DEBUG, handlers=handlers)

# set imported loggers to warning
logging.getLogger("requests").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("uvicorn").setLevel(logging.DEBUG)

logging.getLogger("apscheduler").setLevel(logging.WARNING)
logging.getLogger("aiomysql").setLevel(logging.ERROR)

logging.getLogger("uvicorn.error").propagate = False


# https://github.com/aio-libs/aiomysql/issues/103
# https://github.com/coleifer/peewee/issues/2229
warnings.filterwarnings("ignore", ".*Duplicate entry.*")
