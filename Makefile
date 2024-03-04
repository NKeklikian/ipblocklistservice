.PHONY: install test run

install:
	pyenv local
	pyenv exec pip install poetry
	pyenv exec poetry install

test:
	docker compose up -d redis
	pyenv exec poetry run pytest tests/
	docker compose down

run:
	docker compose up --build
