FROM 818831340115.dkr.ecr.us-east-1.amazonaws.com/python:3.9

RUN mkdir -p /usr/share/fonts/truetype
COPY fonts/* /usr/share/fonts/truetype/

RUN fc-cache -fv

COPY . .

ENV PYTHONPATH /code

RUN poetry install

CMD poetry run ./manage.py wait_for_db && poetry run ./manage.py migrate && poetry run ./manage.py createcachetable && poetry run gunicorn -k uvicorn.workers.UvicornWorker -w 16 -b 0.0.0.0:3000 backend.asgi
