#!/bin/bash
cd authentification-service
docker build -t dockercristinabuciu/proiect-cc-authentification-service:v1 -f Dockerfile .
cd ../

cd app
docker build -t dockercristinabuciu/proiect-cc-app:v2 -f Dockerfile .
cd ../

cd stock-service
docker build -t dockercristinabuciu/proiect-cc-stock-service:latest -f Dockerfile .
cd ../

cd reports-service
docker build -t dockercristinabuciu/proiect-cc-reports-service:latest -f Dockerfile .
cd ../

cd order-service
docker build -t dockercristinabuciu/proiect-cc-order-service:latest -f Dockerfile .
cd ../

cd customer-request-service
docker build -t dockercristinabuciu/proiect-cc-customer-request-service:latest -f Dockerfile .
cd ../

cd recommendation-service
docker build -t dockercristinabuciu/proiect-cc-recommendation-service:latest -f Dockerfile .
cd ../
