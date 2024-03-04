from flask_swagger_ui import get_swaggerui_blueprint

from flask import Flask
from app.home import home
from app.home.config import DISABLE_JOB_MANAGER, REDIS_DISABLED
from app.home.job_manager import start_job_manager
from app.home import ip_blocklist_service

app = Flask(__name__)

# Swagger UI route
SWAGGER_URL = '/api/docs'
API_URL = '/spec'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "IP Blocklist Service"
    }
)


@home.route("/spec")
def spec():
    return open('app/swagger.yaml','r')


app.register_blueprint(home, url_prefix='')

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if not DISABLE_JOB_MANAGER:
    print("Starting Job Manager")
    if REDIS_DISABLED:
        raise Exception('Redis must be enabled in order to start the Job Manager')
    start_job_manager()



