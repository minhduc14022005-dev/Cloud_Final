# Script tự động cấu hình Keycloak: Realm realm_523H0048, Client flask-app, Users sv01/sv02
Write-Host "Dang ket noi va khoi tao cau hinh Keycloak..." -ForegroundColor Cyan

# 1. Dang nhap admin
docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# 2. Tao Realm realm_523H0048 (neu chua co)
$realms = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get realms
if (-not ($realms -match "realm_523H0048")) {
    Write-Host "Tao Realm realm_523H0048..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create realms -s realm=realm_523H0048 -s enabled=true
} else {
    Write-Host "Realm realm_523H0048 da ton tai." -ForegroundColor Green
}

# 3. Tao Client flask-app (neu chua co)
$clients = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients -r realm_523H0048
if (-not ($clients -match "flask-app")) {
    Write-Host "Tao Client flask-app..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create clients -r realm_523H0048 -s clientId=flask-app -s publicClient=true -s directAccessGrantsEnabled=true -s enabled=true -s 'redirectUris=[\"*\"]'
} else {
    Write-Host "Client flask-app da ton tai." -ForegroundColor Green
}

# 3b. Audience mapper: token co aud=flask-app de backend kiem tra audience
$cid = (docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients -r realm_523H0048 -q clientId=flask-app --fields id --format csv --noquotes).Trim()
$mappers = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get clients/$cid/protocol-mappers/models -r realm_523H0048
if (-not ($mappers -match "audience-flask-app")) {
    Write-Host "Them audience mapper cho flask-app..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create clients/$cid/protocol-mappers/models -r realm_523H0048 -s name=audience-flask-app -s protocol=openid-connect -s protocolMapper=oidc-audience-mapper -s 'config.\"included.client.audience\"=flask-app' -s 'config.\"access.token.claim\"=true' -s 'config.\"id.token.claim\"=false'
}

# 4. Tao User sv01
$user1 = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_523H0048 -q username=sv01
if (-not ($user1 -match "sv01")) {
    Write-Host "Tao User sv01..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_523H0048 -s username=sv01 -s firstName=SinhVien -s lastName=01 -s email=sv01@cloud.local -s emailVerified=true -s enabled=true
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_523H0048 --username sv01 --new-password UBgGzzj5fmmK --temporary=false
} else {
    Write-Host "User sv01 da ton tai." -ForegroundColor Green
}

# 5. Tao User sv02
$user2 = docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh get users -r realm_523H0048 -q username=sv02
if (-not ($user2 -match "sv02")) {
    Write-Host "Tao User sv02..." -ForegroundColor Yellow
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh create users -r realm_523H0048 -s username=sv02 -s firstName=SinhVien -s lastName=02 -s email=sv02@cloud.local -s emailVerified=true -s enabled=true
    docker exec authentication-identity-server /opt/keycloak/bin/kcadm.sh set-password -r realm_523H0048 --username sv02 --new-password WJEuCsYV1VF0 --temporary=false
} else {
    Write-Host "User sv02 da ton tai." -ForegroundColor Green
}

Write-Host "`nKeycloak da san sang! Ban co the lay Token va test endpoint /secure ngay bay gio." -ForegroundColor Green

