FROM python:3.6

EXPOSE 5000

WORKDIR /token-generator

COPY requirements.txt /token-generator
RUN pip install -r requirements.txt

COPY token-generator.py /token-generator

CMD python token-generator.py
