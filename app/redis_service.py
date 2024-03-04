import redis
from app.home.config import REDIS_HOST, REDIS_PORT


class RedisService:

    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
