from app.home.ip_blocklist_service import IpBlocklistService
from app.home.constants import BLOCKLIST_NAME
from app.home.config import REDIS_HOST, REDIS_PORT, REDIS_DISABLED
import redis
import os

redis_test_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def test_is_blocklisted():
    service = IpBlocklistService
    redis_test_instance.sadd(BLOCKLIST_NAME,'2.2.2.2')
    print("Redis_disabled",os.getenv("REDIS_DISABLED"))
    print(service.is_blocklisted('2.2.2.2'))
    print(redis_test_instance.sismember(BLOCKLIST_NAME, '2.2.2.2'))
    assert service.is_blocklisted('2.2.2.2')


def test_is_not_blocklisted():
    service = IpBlocklistService
    redis_test_instance.srem(BLOCKLIST_NAME, '1.1.1.1')
    assert service.is_blocklisted('1.1.1.1') is False
