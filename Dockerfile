FROM python:3.10-slim

WORKDIR /code
COPY . /code/

EXPOSE 5000

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"] 