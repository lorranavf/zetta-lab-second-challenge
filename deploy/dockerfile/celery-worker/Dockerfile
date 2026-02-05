FROM python:3.12-slim

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

USER app

WORKDIR /app

CMD ["celery", "-A", "app", "worker", "--loglevel=info", "-Q", "app_queue", "--concurrency=1", "-n", "worker.app"]
