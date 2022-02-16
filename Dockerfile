FROM python:latest

COPY . /

ARG SERVER_PORT
EXPOSE $SERVER_PORT

RUN ["python3", "-m", "pip", "install", "-r", "dependencies/requirements.txt"]
CMD ["python3", "./src/Magi.py"]
