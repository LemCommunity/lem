FROM node:14-alpine
WORKDIR /app

COPY ./package*.json ./
RUN npm ci

COPY . .

CMD [ "npm", "run", "dev" ]
