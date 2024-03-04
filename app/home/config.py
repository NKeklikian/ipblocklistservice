import os

REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
URL = os.getenv("URL", 'https://raw.githubusercontent.com/stamparm/ipsum/master/levels/1.txt')
RETRY_CONNECTIONS = os.getenv("RETRY_CONNECTIONS", 5)
RETRY_READS = os.getenv("RETRY_READS", 2)
RETRY_REDIRECTS = os.getenv("RETRY_REDIRECTS", 5)
UPDATE_INTERVAL_IN_SECONDS = os.getenv("UPDATE_INTERVAL_IN_SECONDS", 15)
REDIS_DISABLED = os.getenv("REDIS_DISABLED", 'False').lower() in ('true', '1', 't')
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
DISABLE_JOB_MANAGER = os.getenv("DISABLE_JOB_MANAGER", 'True').lower() == 'true'
