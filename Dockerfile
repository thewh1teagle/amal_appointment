FROM python:3.8-alpine
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY src/* /app/
CMD ["python", "-u", "main.py"]