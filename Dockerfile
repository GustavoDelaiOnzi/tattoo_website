FROM python:3.8.3

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]