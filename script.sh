#!/bin/bash
cd token-generator
docker build -t dockercristinabuciu/proiect-cc-token-generator:v1 -f Dockerfile .
cd ../
cd app
docker build -t dockercristinabuciu/proiect-cc-app:v2 -f Dockerfile .
cd ../
