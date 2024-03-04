from app.redis_service import redis_instance
import requests
from app.home.config import RETRY_CONNECTIONS, RETRY_READS, RETRY_REDIRECTS, URL, REDIS_DISABLED
from app.home.constants import ENCODING, BLOCKLIST_NAME
from requests.adapters import HTTPAdapter, Retry

s = requests.Session()
s.mount(URL, HTTPAdapter(max_retries=Retry(connect=RETRY_CONNECTIONS, read=RETRY_READS,
                                           redirect=RETRY_REDIRECTS)))
# With more time I could do a backoff factor to try in a few minutes
# (change dynamically the job schedule)

# Test with a first successful attempt and a fail right after
# Test job manager service functions and move them to another file


def singleton(cls):
    return cls()


@singleton
class IpBlocklistService:

    def is_blocklisted(self, ip):
        if REDIS_DISABLED:
            print("Redis is disabled")
            my_blocklist = self.get_ip_blocklist()
            return ip in my_blocklist
        return bool(redis_instance.sismember(BLOCKLIST_NAME, ip))


    @staticmethod
    def get_ip_blocklist():
        try:
            print("Downloading Blocklist")
            response = s.get(URL)
            blocklist = response.content.decode(ENCODING).strip('\n').split('\n')
            # logging.info('Downloaded blocklist')
            return blocklist
        except Exception as e:
            print('Error downloading blocklist', e)
#            if self.redis.r.scard(BLOCKLIST_NAME) > 0:
#                return list(self.redis.r.smembers(BLOCKLIST_NAME))
            return []


