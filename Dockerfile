FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose HTTP gateway & MCP port
EXPOSE 8080

CMD ["python", "tools/mcp_server.py"]
