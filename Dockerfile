FROM python:latest

COPY . /

EXPOSE 2407

RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]

CMD ["python3", "./src/Magi.py"]
