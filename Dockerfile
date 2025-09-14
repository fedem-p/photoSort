# PhotoSort Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install poetry && poetry install --no-root

CMD ["poetry", "run", "python", "-m", "photosort.main"]
