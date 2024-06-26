FROM python:3.10-slim

WORKDIR /code
COPY . /code/

EXPOSE 5000

RUN apt-get update
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"] 