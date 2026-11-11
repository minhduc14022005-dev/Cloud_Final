# Script tự động cấu hình Keycloak: Realm realm_VoAnhKiet, Client flask-app, Users sv01/sv02
Write-Host "Dang ket noi va khoi tao cau hinh Keycloak..." -ForegroundColor Cyan

# 1. Dang nhap admin
docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# 2. Tao Realm realm_VoAnhKiet (neu chua co)
$realms = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get realms
if ($realms -notmatch "realm_VoAnhKiet") {
    Write-Host "Tao Realm realm_VoAnhKiet..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create realms -s realm=realm_VoAnhKiet -s enabled=true
} else {
    Write-Host "Realm realm_VoAnhKiet da ton tai." -ForegroundColor Green
}

# 3. Tao Client flask-app (neu chua co)
$clients = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients -r realm_VoAnhKiet
if ($clients -notmatch "flask-app") {
    Write-Host "Tao Client flask-app..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create clients -r realm_VoAnhKiet -s clientId=flask-app -s publicClient=true -s directAccessGrantsEnabled=true -s enabled=true -s "redirectUris=[`"*`"]"
} else {
    Write-Host "Client flask-app da ton tai." -ForegroundColor Green
}

# 4. Tao User sv01
$user1 = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_VoAnhKiet -q username=sv01
if ($user1 -notmatch "sv01") {
    Write-Host "Tao User sv01..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_VoAnhKiet -s username=sv01 -s firstName=SinhVien -s lastName=01 -s email=sv01@cloud.local -s emailVerified=true -s enabled=true
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_VoAnhKiet --username sv01 --new-password UBgGzzj5fmmK --temporary=false
} else {
    Write-Host "User sv01 da ton tai." -ForegroundColor Green
}

# 5. Tao User sv02
$user2 = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_VoAnhKiet -q username=sv02
if ($user2 -notmatch "sv02") {
    Write-Host "Tao User sv02..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_VoAnhKiet -s username=sv02 -s firstName=SinhVien -s lastName=02 -s email=sv02@cloud.local -s emailVerified=true -s enabled=true
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_VoAnhKiet --username sv02 --new-password WJEuCsYV1VF0 --temporary=false
} else {
    Write-Host "User sv02 da ton tai." -ForegroundColor Green
}

Write-Host "`nKeycloak da san sang! Ban co the lay Token va test endpoint /secure ngay bay gio." -ForegroundColor Green

