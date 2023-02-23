FROM python:3.8-alpine3.16

RUN mkdir /app

COPY . /app

EXPOSE 80
RUN pip3 install -r /app/requirements.txt

CMD ["python", "/app/main.py"]

