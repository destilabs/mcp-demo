FROM python:3.10-slim

ARG FASTMCP_PORT=8080

ENV FASTMCP_PORT=${FASTMCP_PORT}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "server.py"]
