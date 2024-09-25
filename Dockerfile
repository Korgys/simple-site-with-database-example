FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install Flask

EXPOSE 5100

CMD ["python", "app.py"]
