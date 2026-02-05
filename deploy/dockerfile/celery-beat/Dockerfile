FROM python:3.12-slim

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

RUN groupadd -r app && useradd -r -g app app

RUN mkdir -p /data && \
    chown -R app:app /data && \
    chmod -R 777 /data

USER app

WORKDIR /app

CMD ["celery", "-A", "app", "beat", "--loglevel=info", "-s", "/data/celerybeat-schedule"]
