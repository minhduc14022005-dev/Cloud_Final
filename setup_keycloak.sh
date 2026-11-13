#!/bin/bash
# Script tự động cấu hình Keycloak trên Linux / AWS EC2
echo "==> Đang khởi tạo cấu hình Keycloak..."

# 1. Đăng nhập admin
sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# 2. Tạo Realm realm_523H0048 (nếu chưa có)
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get realms | grep -q "realm_523H0048"; then
    echo "==> Đang tạo Realm realm_523H0048..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create realms -s realm=realm_523H0048 -s enabled=true
else
    echo "==> Realm realm_523H0048 đã tồn tại."
fi

# 3. Tạo Client flask-app (nếu chưa có)
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients -r realm_523H0048 | grep -q "flask-app"; then
    echo "==> Đang tạo Client flask-app..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create clients -r realm_523H0048 -s clientId=flask-app -s publicClient=true -s directAccessGrantsEnabled=true -s enabled=true -s 'redirectUris=["*"]'
else
    echo "==> Client flask-app đã tồn tại."
fi

# 3b. Audience mapper: token có aud=flask-app để backend kiểm tra audience
CID=$(sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients -r realm_523H0048 -q clientId=flask-app --fields id --format csv --noquotes)
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients/$CID/protocol-mappers/models -r realm_523H0048 | grep -q "audience-flask-app"; then
    echo "==> Đang thêm audience mapper cho flask-app..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create clients/$CID/protocol-mappers/models -r realm_523H0048 -s name=audience-flask-app -s protocol=openid-connect -s protocolMapper=oidc-audience-mapper -s 'config."included.client.audience"=flask-app' -s 'config."access.token.claim"=true' -s 'config."id.token.claim"=false'
fi

# 4. Tạo User sv01
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_523H0048 -q username=sv01 | grep -q "sv01"; then
    echo "==> Đang tạo User sv01..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_523H0048 -s username=sv01 -s firstName=SinhVien -s lastName=01 -s email=sv01@cloud.local -s emailVerified=true -s enabled=true
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_523H0048 --username sv01 --new-password UBgGzzj5fmmK --temporary=false
else
    echo "==> User sv01 đã tồn tại."
fi

# 5. Tạo User sv02
if ! sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_523H0048 -q username=sv02 | grep -q "sv02"; then
    echo "==> Đang tạo User sv02..."
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_523H0048 -s username=sv02 -s firstName=SinhVien -s lastName=02 -s email=sv02@cloud.local -s emailVerified=true -s enabled=true
    sudo docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_523H0048 --username sv02 --new-password WJEuCsYV1VF0 --temporary=false
else
    echo "==> User sv02 đã tồn tại."
fi

echo "==> Hoàn tất! Keycloak đã sẵn sàng trên AWS EC2."

