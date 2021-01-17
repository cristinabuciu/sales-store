FROM python:3.6

EXPOSE 5000
EXPOSE 8000

WORKDIR /order-service

COPY requirements.txt /order-service
RUN pip install -r requirements.txt
RUN pip install prometheus_client
RUN pip install uwsgi

COPY order-service.py /order-service
#COPY templates/* /server/templates/
#COPY static/* /server/static/

CMD python order-service.py
#CMD uwsgi --http 0.0.0.0:8000 --wsgi-file server.py --callable app_dispatch