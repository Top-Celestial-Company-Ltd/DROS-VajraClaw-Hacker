# DROS VajraClaw Hacker Gateway Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy project files
COPY core/ /app/core/
COPY integrations/ /app/integrations/
COPY FreeTrial-Sandbox/demo_policy.yaml /app/demo_policy.yaml
COPY docker/server.py /app/server.py

ENV PORT=8080
ENV DROS_POLICY_PATH=/app/demo_policy.yaml
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["python", "server.py"]
