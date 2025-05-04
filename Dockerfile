FROM python:3.12.10-alpine3.21 AS builddependencies

ADD . /projectbase
WORKDIR /projectbase
RUN pip3 install poetry poetry-plugin-export && \
    poetry sync --without test && \
    poetry export --without-hashes --format=requirements.txt --only main --output src/requirements.txt

FROM python:3.12.10-alpine3.21 AS builder
COPY --from=builddependencies /projectbase/src /app
RUN rm -rf /app/__pycache__ && \
    rm -rf /app/.pytest_cache && \
    pip3 install --target /app -r /app/requirements.txt && \
    chmod 755 /app/app.py

FROM python:3.12.10-alpine3.21 AS final
RUN apk add --update git
COPY --from=builder /app /app
ENV PYTHONPATH=/app

ENTRYPOINT ["/app/app.py"]
