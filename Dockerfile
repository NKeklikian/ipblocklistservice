# Use official Python runtime as a parent image
FROM python:3.10.4-slim as poetry

RUN apt-get update -yqq && apt-get install -yqq \
    cron \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install poetry

FROM poetry as poetry-deps

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to /app in the container
ADD . /app

COPY poetry.lock pyproject.toml ./

# Use poetry to install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Set the startup command to run your flask app
#CMD ["exec", "gunicorn", "runner:app" "--host=0.0.0.0", "--port=8000"]
#COPY . /app

CMD [ "poetry", "run", "gunicorn", "-b", "0.0.0.0:8000", "runner:app" ]

