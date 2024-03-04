from apscheduler.schedulers.background import BackgroundScheduler

from app.redis_service import RedisService
import time
import logging
from github import Github, Auth
import datetime
from app.home.constants import *
from injector import Injector
from app.home.ip_blocklist_service import IpBlocklistService

# Refactor injector
# injector = Injector()
# service = injector.get(IpBlocklistService)

redis = RedisService()


def check_commit_sha_updated():
    logging.info("Checking SHA")
    auth = Auth.Token("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")
    g = Github(auth=auth)
    repo = g.get_repo("stamparm/ipsum")
    current_commit_sha = repo.get_commits(since=datetime.datetime.now() - datetime.timedelta(days=1))[0].sha
    last_commit_sha = redis.r.get('last_commit_sha')
    if current_commit_sha != last_commit_sha:
        redis.r.set('last_commit_sha', current_commit_sha.strftime())
        IpBlocklistService.download_and_save_blocklist()
        last_commit_date = repo.get_commit(current_commit_sha).commit.committer.date
        redis.r.set('last_commit_date', last_commit_date.strftime())


def start_job_manager():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(check_commit_sha_updated, 'interval', hours=1, next_run_time=datetime.datetime.now()+datetime.timedelta(hours=1))
    print(scheduler.get_jobs())
    scheduler.start()
    print("Scheduler successfully started")
