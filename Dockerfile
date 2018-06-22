FROM python:3.6

RUN mkdir /app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY app.py /app
COPY titanic-lr.sav /app

WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["-u","app.py"]
