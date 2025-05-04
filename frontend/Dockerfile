FROM node:20

WORKDIR /app

COPY package*.json jsconfig.json vite.config.js ./
RUN npm ci

COPY . .

CMD ["npm", "run", "dev", "--", "--host"]
