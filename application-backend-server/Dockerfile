FROM node:20-alpine
WORKDIR /app

# Cài đặt thư viện npm
COPY package*.json ./
RUN npm install --production

# Sao chép mã nguồn
COPY . .

EXPOSE 8081
CMD ["node", "server.js"]
