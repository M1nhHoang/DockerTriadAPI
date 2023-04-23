FROM python:3.10-slim-buster

WORKDIR /api

COPY ./main.py /api
COPY ./index.html /api

RUN pip install fastapi uvicorn requests

CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 1717 --reload"]
