FROM python:3

RUN mkdir -p /usr/share/fonts/truetype
COPY fonts/* /usr/share/fonts/truetype/

RUN fc-cache -fv

RUN mkdir /code
WORKDIR /code
COPY . .

RUN pip install -r requirements.txt

CMD ./manage.py wait_for_db && ./manage.py migrate && ./manage.py createcachetable && gunicorn -k uvicorn.workers.UvicornWorker -w 16 -b 0.0.0.0:3000 backend.asgi
