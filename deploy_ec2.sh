#!/bin/bash
# ====================================================================
# Script tự động triển khai toàn diện MyMiniCloud trên AWS EC2 (Ubuntu)
# ====================================================================

echo "=========================================================="
echo "   TRIỂN KHAI HỆ THỐNG MYMINICLOUD TRÊN AWS EC2           "
echo "=========================================================="

# 1. Tự động lấy Public IP của máy ảo EC2
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com || curl -s ifconfig.me)
if [ -z "$PUBLIC_IP" ]; then
    read -p "Không tự động lấy được Public IP, vui lòng nhập Public IP của EC2: " PUBLIC_IP
fi
echo "==> Public IP của máy ảo EC2: $PUBLIC_IP"

# 2. Cấu hình Swap 2GB (Đặc biệt quan trọng cho t2.micro để không bị tràn RAM)
if [ $(swapon --show | wc -l) -le 1 ]; then
    echo "==> Đang kích hoạt 2GB Swap Memory để chạy mượt 10 container..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# 3. Cài đặt Docker & Docker Compose nếu chưa có
if ! command -v docker &> /dev/null; then
    echo "==> Đang cài đặt Docker và Docker Compose..."
    sudo apt-get update -y
    sudo apt-get install -y ca-certificates curl gnupg lsb-release
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $USER
fi

# 4. Cập nhật Public IP vào docker-compose.yml
echo "==> Đang cấu hình Public IP ($PUBLIC_IP) cho Keycloak và Backend..."
sed -i "s|KC_HOSTNAME: \"localhost\"|KC_HOSTNAME: \"$PUBLIC_IP\"|g" docker-compose.yml
sed -i "s|OIDC_ISSUER: \"http://localhost:8081/realms/realm_VoAnhKiet\"|OIDC_ISSUER: \"http://$PUBLIC_IP:8081/realms/realm_VoAnhKiet\"|g" docker-compose.yml

# 5. Khởi động toàn bộ 10 container
echo "==> Đang build và khởi động toàn bộ container..."
sudo docker compose up -d --build

# 6. Chờ Keycloak khởi động hoàn tất và cấu hình Realm
echo "==> Đang chờ Keycloak khởi động (khoảng 35 giây)..."
sleep 35

chmod +x setup_keycloak.sh
./setup_keycloak.sh

echo "=========================================================="
echo "   TRIỂN KHAI THÀNH CÔNG LÊN AWS EC2!                    "
echo "=========================================================="
echo "Các đường link truy cập hệ thống của bạn:"
echo "  1. Trang chủ (Gateway Port 80): http://$PUBLIC_IP/"
echo "  2. Blog cá nhân:               http://$PUBLIC_IP/blog/"
echo "  3. API Sinh viên (JSON):        http://$PUBLIC_IP/student/"
echo "  4. API Sinh viên (MySQL):       http://$PUBLIC_IP/api/students-db"
echo "  5. Keycloak Admin Console:      http://$PUBLIC_IP:8081/ (admin / admin)"
echo "  6. MinIO Storage Console:       http://$PUBLIC_IP:9001/ (minioadmin / minioadmin)"
echo "  7. Grafana Monitoring:          http://$PUBLIC_IP:3000/ (admin / admin)"
echo "=========================================================="
