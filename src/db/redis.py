import os

from redis import Redis
from dotenv import load_dotenv


load_dotenv()

blocked_access_tokens = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    decode_responses=True,
)
