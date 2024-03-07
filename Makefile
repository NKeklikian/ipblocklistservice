.PHONY: install test run

install:
	pyenv local
	pyenv exec pip install poetry
	pyenv exec poetry install

test:
	docker compose up -d redis
	pyenv exec poetry run pytest tests/
	docker compose down

docker-run:
	docker compose up --build

run:
	docker compose up -d redis
	pyenv exec poetry run gunicorn -b 0.0.0.0:8000 runner:app
	docker compose down
