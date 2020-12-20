FROM python:3.7-alpine

RUN pip install paho-mqtt requests

COPY ./main.py /app/main.py

WORKDIR /app

CMD ["python3", "main.py"]