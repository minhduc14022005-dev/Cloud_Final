#!/bin/bash
# Script tự động cấu hình Keycloak trên Linux / AWS EC2
echo "==> Đang khởi tạo cấu hình Keycloak..."

# 1. Đăng nhập admin
sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# 2. Tạo Realm realm_VoAnhKiet (nếu chưa có)
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get realms | grep -q "realm_VoAnhKiet"; then
    echo "==> Đang tạo Realm realm_VoAnhKiet..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create realms -s realm=realm_VoAnhKiet -s enabled=true
else
    echo "==> Realm realm_VoAnhKiet đã tồn tại."
fi

# 3. Tạo Client flask-app (nếu chưa có)
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients -r realm_VoAnhKiet | grep -q "flask-app"; then
    echo "==> Đang tạo Client flask-app..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create clients -r realm_VoAnhKiet -s clientId=flask-app -s publicClient=true -s directAccessGrantsEnabled=true -s enabled=true -s 'redirectUris=["*"]'
else
    echo "==> Client flask-app đã tồn tại."
fi

# 4. Tạo User sv01
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_VoAnhKiet -q username=sv01 | grep -q "sv01"; then
    echo "==> Đang tạo User sv01..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_VoAnhKiet -s username=sv01 -s firstName=SinhVien -s lastName=01 -s email=sv01@cloud.local -s emailVerified=true -s enabled=true
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_VoAnhKiet --username sv01 --new-password UBgGzzj5fmmK --temporary=false
else
    echo "==> User sv01 đã tồn tại."
fi

# 5. Tạo User sv02
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_VoAnhKiet -q username=sv02 | grep -q "sv02"; then
    echo "==> Đang tạo User sv02..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_VoAnhKiet -s username=sv02 -s firstName=SinhVien -s lastName=02 -s email=sv02@cloud.local -s emailVerified=true -s enabled=true
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_VoAnhKiet --username sv02 --new-password WJEuCsYV1VF0 --temporary=false
else
    echo "==> User sv02 đã tồn tại."
fi

echo "==> Hoàn tất! Keycloak đã sẵn sàng trên AWS EC2."
