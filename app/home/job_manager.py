from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.redis_service import redis_instance
from github import Github, Auth
import datetime
from app.home.constants import *
from app.home.ip_blocklist_service import IpBlocklistService
from app.home.config import GITHUB_TOKEN, IP_BLOCKLIST_URL, UPDATE_INTERVAL_IN_HOURS


def save_ip_blocklist(blocklist):
    redis_instance.sadd(BLOCKLIST_NAME, *blocklist)


def download_and_save_blocklist():
    blocklist = IpBlocklistService.get_ip_blocklist()
    save_ip_blocklist(blocklist)


def get_repo():
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)
    return g.get_repo(IP_BLOCKLIST_URL)


def get_current_commit_sha():
    repo = get_repo()
    return repo.get_commits(since=datetime.datetime.now() - datetime.timedelta(days=1))[0].sha


def update_last_commit(last_commit_sha):
    repo = get_repo()
    last_commit_date: datetime = repo.get_commit(last_commit_sha).commit.committer.date
    redis_instance.set(LAST_COMMIT_DATE_KEY, last_commit_date.strftime(format='str'))
    redis_instance.set(LAST_COMMIT_SHA_KEY, last_commit_sha)


def update_blocklist_if_needed():
    current_commit_sha = get_current_commit_sha()
    last_commit_sha = redis_instance.get(LAST_COMMIT_SHA_KEY)
    if current_commit_sha != last_commit_sha:
        download_and_save_blocklist()
        update_last_commit(current_commit_sha)


def start_job_manager():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(update_blocklist_if_needed, 'interval', hours=UPDATE_INTERVAL_IN_HOURS,
                      next_run_time=datetime.datetime.now() + datetime.timedelta(hours=UPDATE_INTERVAL_IN_HOURS))
    print(scheduler.get_jobs())
    scheduler.start()
    print("Scheduler successfully started")
