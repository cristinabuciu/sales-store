FROM python:3.6

EXPOSE 5000

WORKDIR /authentification-service

COPY requirements.txt /authentification-service
RUN pip install -r requirements.txt

COPY authentification-service.py /authentification-service

CMD python authentification-service.py
