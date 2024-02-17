FROM python:latest

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=PyInMemStore.py

CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:5000", "PyInMemStore:app"]