FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python","manage.py","runserver","--insecure","0.0.0.0:8000"]

