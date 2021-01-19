FROM python:3.6

EXPOSE 5000

WORKDIR /customer-request-service

COPY requirements.txt /customer-request-service
RUN pip install -r requirements.txt
RUN pip install prometheus_client
RUN pip install uwsgi

COPY customer-request.py /customer-request-service
#COPY templates/* /server/templates/
#COPY static/* /server/static/

CMD python customer-request.py
#CMD uwsgi --http 0.0.0.0:8000 --wsgi-file server.py --callable app_dispatch