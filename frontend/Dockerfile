# frontend

FROM node:20 AS builder

# Set work directory
WORKDIR /app

COPY package*.json jsconfig.json vite.config.js ./
RUN npm ci

COPY src ./src
COPY public ./public

CMD ["npm", "run", "dev"]
