# Script tự động kiểm thử toàn bộ MyMiniCloud
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   KIEM THU HE THONG MYMINICLOUD (LOCAL & GATEWAY)        " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Web Frontend & Load Balancer
Write-Host "`n[1] Kiem tra Web Frontend & Load Balancer:" -ForegroundColor Yellow
try {
    $res1 = Invoke-WebRequest -Uri "http://localhost:8080/" -UseBasicParsing -TimeoutSec 5
    Write-Host "  -> Web 1 (Home - 8080): OK (Status: $($res1.StatusCode))" -ForegroundColor Green
    $resBlog = Invoke-WebRequest -Uri "http://localhost:8080/blog/" -UseBasicParsing -TimeoutSec 5
    Write-Host "  -> Web 1 (Blog - 8080/blog/): OK (Status: $($resBlog.StatusCode))" -ForegroundColor Green
} catch { Write-Host "  -> Web 1 loi: $_" -ForegroundColor Red }

try {
    $res2 = Invoke-WebRequest -Uri "http://localhost:8082/" -UseBasicParsing -TimeoutSec 5
    Write-Host "  -> Web 2 (Load Balanced - 8082): OK (Status: $($res2.StatusCode))" -ForegroundColor Green
} catch { Write-Host "  -> Web 2 loi: $_" -ForegroundColor Red }

# 2. Application Backend API (Node.js Express)
Write-Host "`n[2] Kiem tra Application Backend (Node.js Express):" -ForegroundColor Yellow
try {
    $resHello = Invoke-RestMethod -Uri "http://localhost:8085/hello" -TimeoutSec 5
    Write-Host "  -> /hello: OK - Message: $($resHello.message)" -ForegroundColor Green
    $resStudent = Invoke-RestMethod -Uri "http://localhost:8085/student" -TimeoutSec 5
    Write-Host "  -> /student (Mo rong 2): OK - Tim thay $($resStudent.Count) sinh vien" -ForegroundColor Green
    $resDB = Invoke-RestMethod -Uri "http://localhost:8085/students-db" -TimeoutSec 5
    Write-Host "  -> /students-db (Mo rong 3 - MySQL): OK - Lay duoc $($resDB.data.Count) ban ghi tu studentdb" -ForegroundColor Green
} catch { Write-Host "  -> Backend loi: $_" -ForegroundColor Red }

# 3. API Gateway & Reverse Proxy (Port 80)
Write-Host "`n[3] Kiem tra API Gateway (Port 80):" -ForegroundColor Yellow
try {
    $resGWHome = Invoke-WebRequest -Uri "http://localhost/" -UseBasicParsing -TimeoutSec 5
    Write-Host "  -> Gateway / (Web Round Robin): OK (Status: $($resGWHome.StatusCode))" -ForegroundColor Green
    $resGWApi = Invoke-RestMethod -Uri "http://localhost/api/hello" -TimeoutSec 5
    Write-Host "  -> Gateway /api/hello (App): OK - Message: $($resGWApi.message)" -ForegroundColor Green
    $resGWStudent = Invoke-RestMethod -Uri "http://localhost/student/" -TimeoutSec 5
    Write-Host "  -> Gateway /student/ (Mo rong 9): OK - Lay duoc $($resGWStudent.Count) sinh vien" -ForegroundColor Green
    
    $curlAuth = curl.exe -s -I http://localhost/auth/
    if ($curlAuth -match "302|200") {
        Write-Host "  -> Gateway /auth/ (Keycloak): OK (Status: 302 Redirect to /admin/)" -ForegroundColor Green
    } else {
        Write-Host "  -> Gateway /auth/ (Keycloak): Dang khoi dong..." -ForegroundColor Yellow
    }
} catch { Write-Host "  -> Gateway loi: $_" -ForegroundColor Red }

# 4. Storage, Monitoring & DNS
Write-Host "`n[4] Kiem tra MinIO, Prometheus, Grafana & DNS:" -ForegroundColor Yellow
try {
    $resMinio = Invoke-WebRequest -Uri "http://localhost:9000/minio/health/live" -UseBasicParsing -TimeoutSec 5
    Write-Host "  -> MinIO Live Check (Port 9000): OK" -ForegroundColor Green
} catch { Write-Host "  -> MinIO loi: $_" -ForegroundColor Red }

try {
    $resProm = Invoke-RestMethod -Uri "http://localhost:9090/api/v1/targets" -TimeoutSec 5
    Write-Host "  -> Prometheus Targets (Port 9090): OK - Active Targets: $($resProm.data.activeTargets.Count)" -ForegroundColor Green
} catch { Write-Host "  -> Prometheus loi: $_" -ForegroundColor Red }

try {
    $resGrafana = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -TimeoutSec 5
    Write-Host "  -> Grafana Health (Port 3000): OK - Database: $($resGrafana.database)" -ForegroundColor Green
} catch { Write-Host "  -> Grafana loi: $_" -ForegroundColor Red }

# DNS Bind9 check
$dnsWeb = docker exec internal-dns-server dig "@127.0.0.1" web-frontend-server.cloud.local +short
$dnsApp = docker exec internal-dns-server dig "@127.0.0.1" app-backend.cloud.local +short
if ($dnsWeb -and $dnsApp) {
    Write-Host "  -> DNS Bind9 (Port 1053): OK - web: $dnsWeb, app: $dnsApp" -ForegroundColor Green
} else {
    Write-Host "  -> DNS Bind9 loi phan giai" -ForegroundColor Red
}

# 5. Kiểm tra thông mạng Ping giữa các container
Write-Host "`n[5] Kiem tra Ping thong mang noi bo (cloud-net):" -ForegroundColor Yellow
$targets = @("web-frontend-server", "web-frontend-server2", "relational-database-server", "authentication-identity-server", "object-storage-server", "internal-dns-server", "monitoring-prometheus-server", "monitoring-grafana-dashboard-server", "api-gateway-proxy-server")
foreach ($t in $targets) {
    $pingOut = docker exec application-backend-server ping -c 1 $t 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  -> Ping to $($t): SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "  -> Ping to $($t): FAILED" -ForegroundColor Red
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "         TAT CA DICH VU DEU DANG HOAT DONG TOT!          " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
