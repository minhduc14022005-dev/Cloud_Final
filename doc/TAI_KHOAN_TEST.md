# Tài khoản test (chỉ dùng cho môi trường local/demo)

| Dịch vụ | URL | Tài khoản | Mật khẩu |
|---|---|---|---|
| Keycloak admin | http://localhost:8081 | admin | admin |
| Keycloak realm `realm_523H0048` | http://localhost:8081/realms/realm_523H0048/account | sv01 | UBgGzzj5fmmK |
| Keycloak realm `realm_523H0048` | http://localhost:8081/realms/realm_523H0048/account | sv02 | WJEuCsYV1VF0 |
| MinIO Console | http://localhost:9001 | minioadmin | minioadmin |
| Grafana | http://localhost:3000 | admin | admin |

Client OIDC: `flask-app` (public, bật Direct access grants).

Lấy token và gọi API bảo mật (PowerShell):
```powershell
$t = (Invoke-RestMethod -Method Post -Uri http://localhost:8081/realms/realm_523H0048/protocol/openid-connect/token -Body @{client_id='flask-app';grant_type='password';username='sv01';password='<mật khẩu sv01>'}).access_token
Invoke-RestMethod -Uri http://localhost/api/secure -Headers @{Authorization="Bearer $t"}
```
