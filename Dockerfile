FROM python:3

RUN mkdir /code
WORKDIR /code
COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "backend.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:3000"]
