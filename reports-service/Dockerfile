FROM python:3.6

EXPOSE 5000

WORKDIR /reports-service

COPY requirements.txt /reports-service
RUN pip install -r requirements.txt
RUN pip install prometheus_client
RUN pip install uwsgi

COPY reports-service.py /reports-service
#COPY templates/* /server/templates/
#COPY static/* /server/static/

CMD python reports-service.py
#CMD uwsgi --http 0.0.0.0:8000 --wsgi-file server.py --callable app_dispatch
