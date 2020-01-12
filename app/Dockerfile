FROM node:8

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . /app


CMD [ "npm", "start" ]