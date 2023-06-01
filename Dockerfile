FROM python:3.9

RUN pip install --upgrade pip poetry

RUN mkdir -p /usr/share/fonts/truetype
COPY fonts/* /usr/share/fonts/truetype/

RUN fc-cache -fv

RUN mkdir /code
WORKDIR /code
COPY . .

ENV PYTHONPATH /code

RUN poetry install

CMD poetry run python ./manage.py wait_for_db && poetry run python ./manage.py migrate && poetry run python ./manage.py createcachetable && poetry run gunicorn -b 0.0.0.0:3000 backend.wsgi
