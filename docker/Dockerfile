FROM python:3.13-slim AS builder
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y build-essential graphviz libgraphviz-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y graphviz libgraphviz-dev && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -r appuser && \
    mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY bcs/ .

RUN chmod +x entrypoint.sh

USER appuser

EXPOSE 8000
CMD ["./entrypoint.sh"]
