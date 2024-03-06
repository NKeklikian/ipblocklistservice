from app.home.ip_blocklist_service import IpBlocklistService
from app.home.constants import BLOCKLIST_NAME

from tests.redis_instance_test import redis_test_instance


def test_is_blocklisted():
    service = IpBlocklistService
    redis_test_instance.sadd(BLOCKLIST_NAME, '2.2.2.2')
    assert service.is_blocklisted('2.2.2.2')


def test_is_not_blocklisted():
    service = IpBlocklistService
    redis_test_instance.srem(BLOCKLIST_NAME, '1.1.1.1')
    assert not service.is_blocklisted('1.1.1.1')
