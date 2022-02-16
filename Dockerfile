FROM python:latest

COPY . /

ARG SERVER_PORT
ARG SECRET_KEY

RUN env

EXPOSE $SERVER_PORT

RUN ["python3", "-m", "pip", "install", "-r", "dependencies/requirements.txt"]

CMD ["python3", "./src/Magi.py"]
