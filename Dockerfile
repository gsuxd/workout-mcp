FROM python:3.12-slim AS builder
 
WORKDIR /app
 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
 
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

#RUNTINE STAGE

FROM python:3.12-slim AS runtime
 
RUN useradd --create-home --shell /bin/bash appuser
 
WORKDIR /app
 
COPY --from=builder /install /usr/local
 
COPY --chown=appuser:appuser . .
 
USER appuser
 
EXPOSE 8001
 
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8001
 
CMD ["python", "main.py"]
