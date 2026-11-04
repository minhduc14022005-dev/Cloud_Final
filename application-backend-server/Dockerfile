FROM node:20-alpine
WORKDIR /app

# Cài đặt thư viện npm qua mirror tốc độ cao để tránh ETIMEDOUT
COPY package*.json ./
RUN npm config set registry https://registry.npmmirror.com \
    && npm config set fetch-retry-maxtimeout 120000 \
    && npm config set fetch-timeout 120000 \
    && npm install --omit=dev

# Sao chép mã nguồn
COPY . .

EXPOSE 8081
CMD ["node", "server.js"]
