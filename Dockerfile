FROM python:3.11-slim

ENV SQS_QUEUE_URL_P2=""
ENV AWS_REGION=""
ENV JIRA_SERVER=""
ENV JIRA_API_TOKEN=""
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "worker.py"]
