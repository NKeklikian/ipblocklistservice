from app.redis_service import redis_instance
import requests
from app.home.config import RETRY_CONNECTIONS, RETRY_READS, RETRY_REDIRECTS, URL, REDIS_DISABLED
from app.home.constants import ENCODING, BLOCKLIST_NAME
from requests.adapters import HTTPAdapter, Retry

s = requests.Session()
s.mount(URL, HTTPAdapter(max_retries=Retry(connect=RETRY_CONNECTIONS, read=RETRY_READS,
                                           redirect=RETRY_REDIRECTS)))
# In case the URL is down for some minutes, a backoff factor can be implemented
# to change dynamically the job schedule


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
            return blocklist
        except Exception as e:
            print('Error downloading blocklist', e)
            return []


