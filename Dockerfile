FROM python:3

RUN apt-get update
RUN apt-get install -y libpango1.0-0 fonts-font-awesome libffi-dev libgdk-pixbuf2.0-0 libcairo2

RUN mkdir /code
WORKDIR /code
COPY . .

RUN pip install -r requirements.txt

CMD ./manage.py wait_for_db && ./manage.py migrate && ./manage.py createcachetable && gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:3000 backend.asgi
