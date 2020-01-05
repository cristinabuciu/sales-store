FROM python:3.6

EXPOSE 5000
EXPOSE 8000

WORKDIR /server

COPY requirements.txt /server
RUN pip install -r requirements.txt
RUN pip install prometheus_client
RUN pip install uwsgi

COPY server.py /server
COPY templates/* /server/templates/
COPY static/* /server/static/

CMD python server.py
#CMD uwsgi --http 0.0.0.0:8000 --wsgi-file server.py --callable app_dispatch