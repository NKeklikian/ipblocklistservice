import redis
from app.home.config import REDIS_HOST, REDIS_PORT

redis_test_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
