FROM python:3.9-slim-buster

COPY ./requirements.txt /requirements.txt
COPY ./src/api /src/api
COPY ./templates /templates

RUN pip install -r /requirements.txt

ENV PYTHONPATH /

EXPOSE 8000

CMD ["python3", "/src/api/api_run.py"]