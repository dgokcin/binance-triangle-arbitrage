FROM python:3.7
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .

CMD [ "python", "./main.py" ]
