# DROS VajraClaw Hacker Gateway Dockerfile (DWGR-8 Self-Contained Edition)
FROM python:3.11-slim

WORKDIR /app

# Install basic health check tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy declarative config and server script
COPY dros.personal.config.json /app/dros.personal.config.json
COPY docker/server.py /app/server.py

ENV PORT=8080
ENV DROS_POLICY_PATH=/app/dros.personal.config.json
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["python", "server.py"]
