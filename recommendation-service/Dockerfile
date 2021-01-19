FROM python:3.6

EXPOSE 5000

WORKDIR /recommendation-service

COPY requirements.txt /recommendation-service
RUN pip install -r requirements.txt
RUN pip install prometheus_client
RUN pip install uwsgi

COPY recommendation.py /recommendation-service
#COPY templates/* /server/templates/
#COPY static/* /server/static/

CMD python recommendation.py
#CMD uwsgi --http 0.0.0.0:8000 --wsgi-file server.py --callable app_dispatch