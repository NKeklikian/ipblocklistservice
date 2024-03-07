# IP Blocklist Service

## Description

This microservice manages a list of IPs that are known to be used for malicious purposes and allows
the user to check if a specific IP is in the list.

## Getting Started

### Prerequisites

- [Pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
-
A [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens),
which should be configured in [the configuration file](/app/home/config.py)
- Python 3.10.4, which can be installed by running `pyenv install 3.10.4`

### Local installation

    make install

## Local deployment

    pyenv exec poetry run gunicorn -b 0.0.0.0:8000 runner:app

## Docker deployment

    make run

## Usage

    curl localhost:8000/api/ips/<ipv4>

#### Example

    curl localhost:8000/api/ips/0.0.0.0    
    {"is_in_blocklist":true}

## Running the tests

Tests can be run inside a docker container by running

    make test

To test locally, run

    pyenv exec poetry run pytest tests/

Reminder: An active Redis service is needed for this to work, which can be done by running

    docker compose up -d redis

### Sample Test

The following test's goal is to check that if an IP was added
to the redis service, then it should return `true`

    def test_blocklisted_ip(client):
        redis_test_instance.sadd(BLOCKLIST_NAME, '103.251.167.20')
        response = client.get("/api/ips/103.251.167.20")
        assert response.data == b'{"is_in_blocklist":true}\n'
        assert response.status_code == 200

## Interactive documentation

Check Swagger's interactive documentation by running

    curl localhost:8000/api/docs/

## Technical Documentation

For more information on technical decisions taken, tradeoffs and functional and non-functional requirements read through
the [documentation](DOCS.md)

## Dependencies

- [Redis](https://redis.io/) - Memory management
- [Poetry](https://python-poetry.org/) - Dependency management
- [Gunicorn](https://gunicorn.org/) - HTTP web server
- [Flask](https://flask.palletsprojects.com/) - Web application framework
- [APScheduler](https://apscheduler.readthedocs.io/) - Library for scheduling python code
- [Pytest](https://pytest.org/) - Testing framework
- [Docker](https://www.docker.com/) - Container platform
- [Swagger](https://swagger.io/) - Interactive documentation
