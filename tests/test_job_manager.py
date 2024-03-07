from app.home.ip_blocklist_service import s
from app.home.constants import BLOCKLIST_NAME, LAST_COMMIT_SHA_KEY
from app.home.config import URL
from app.redis_service import redis_instance
from app.home.job_manager import (save_ip_blocklist, download_and_save_blocklist,
                                  update_last_commit, get_current_commit_sha, update_blocklist_if_needed)
from tests.redis_instance_test import redis_test_instance
import requests_mock


def test_save_ip_blocklist():
    save_ip_blocklist(['5.5.5.5'])
    assert redis_test_instance.sismember(BLOCKLIST_NAME, '5.5.5.5')


def test_download_and_save_blocklist():
    download_and_save_blocklist()
    assert redis_test_instance.sismember(BLOCKLIST_NAME, '213.109.202.127')


def test_mocked_download_and_save_blocklist():
    adapter = requests_mock.Adapter()
    s.mount(URL, adapter)
    adapter.register_uri('GET', URL, text='1.2.3.4')
    download_and_save_blocklist()
    assert redis_test_instance.sismember(BLOCKLIST_NAME, '1.2.3.4')


def test_update_last_commit():
    commit_sha = get_current_commit_sha()
    update_last_commit(commit_sha)
    assert redis_test_instance.get(LAST_COMMIT_SHA_KEY) == commit_sha


def test_update_blocklist_if_needed():
    redis_instance.set(LAST_COMMIT_SHA_KEY,'')
    update_blocklist_if_needed()
    assert redis_test_instance.get(LAST_COMMIT_SHA_KEY) == get_current_commit_sha()
