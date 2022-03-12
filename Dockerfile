FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

RUN useradd -U app_user \
    && install -d -m 0755 -o app_user -g app_user /app

WORKDIR /app
USER app_user:app_user

COPY --chown=app_user:app_user . .

CMD ["python","manage.py","runserver","--insecure","0.0.0.0:8000"]

