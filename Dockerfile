FROM python:3

RUN pip install --upgrade pip poetry

RUN mkdir -p /usr/share/fonts/truetype
COPY fonts/* /usr/share/fonts/truetype/

RUN fc-cache -fv

RUN mkdir /code
WORKDIR /code
COPY . .

RUN poetry install

CMD poetry run ./manage.py wait_for_db && poetry run ./manage.py migrate && poetry run ./manage.py createcachetable && poetry run gunicorn -k uvicorn.workers.UvicornWorker -w 16 -b 0.0.0.0:3000 backend.asgi
