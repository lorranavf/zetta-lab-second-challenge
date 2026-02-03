FROM python:3.12-slim


ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
COPY requirements-test.txt .  

ARG INSTALL_TEST=false

RUN pip install --no-cache-dir -r requirements.txt && \
    if [ "$INSTALL_TEST" = "true" ] ; then \
    pip install --no-cache-dir -r requirements-test.txt ; \
    fi

ARG UID=1000

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    app

RUN mkdir -p /app && \
    chown -R app:app /app

USER app

WORKDIR /app

EXPOSE 5000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]