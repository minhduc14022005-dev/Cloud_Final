# Script tự động kiểm thử toàn bộ MyMiniCloud
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   KIỂM THỬ HỆ THỐNG MYMINICLOUD (LOCAL & PROXY)         " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Web Frontend & Blog
Write-Host "`n[1] Kiểm thử Web Frontend:" -ForegroundColor Yellow
try {
    $res1 = Invoke-WebRequest -Uri "http://localhost:8080/" -UseBasicParsing
    Write-Host "  -> Web 1 (Home - 8080): OK (Status: $($res1.StatusCode))" -ForegroundColor Green
    $resBlog = Invoke-WebRequest -Uri "http://localhost:8080/blog/" -UseBasicParsing
    Write-Host "  -> Web 1 (Blog - 8080/blog/): OK (Status: $($resBlog.StatusCode))" -ForegroundColor Green
} catch { Write-Host "  -> Web 1 lỗi: $_" -ForegroundColor Red }

try {
    $res2 = Invoke-WebRequest -Uri "http://localhost:8082/" -UseBasicParsing
    Write-Host "  -> Web 2 (Load Balanced - 8082): OK (Status: $($res2.StatusCode))" -ForegroundColor Green
} catch { Write-Host "  -> Web 2 lỗi: $_" -ForegroundColor Red }

# 2. Application Backend API
Write-Host "`n[2] Kiểm thử Application Backend (Node.js Express):" -ForegroundColor Yellow
try {
    $resHello = Invoke-RestMethod -Uri "http://localhost:8085/hello"
    Write-Host "  -> /hello: OK - Message: $($resHello.message)" -ForegroundColor Green
    $resStudent = Invoke-RestMethod -Uri "http://localhost:8085/student"
    Write-Host "  -> /student (JSON): OK - Tìm thấy $($resStudent.Count) sinh viên" -ForegroundColor Green
    $resDB = Invoke-RestMethod -Uri "http://localhost:8085/students-db"
    Write-Host "  -> /students-db (MySQL): OK - Lấy được $($resDB.data.Count) bản ghi từ CSDL studentdb" -ForegroundColor Green
} catch { Write-Host "  -> Backend lỗi: $_" -ForegroundColor Red }

# 3. API Gateway & Reverse Proxy
Write-Host "`n[3] Kiểm thử API Gateway & Reverse Proxy (Port 80):" -ForegroundColor Yellow
try {
    $resGWHome = Invoke-WebRequest -Uri "http://localhost/" -UseBasicParsing
    Write-Host "  -> Gateway / (Web): OK (Status: $($resGWHome.StatusCode))" -ForegroundColor Green
    $resGWApi = Invoke-RestMethod -Uri "http://localhost/api/hello"
    Write-Host "  -> Gateway /api/hello (App): OK - Message: $($resGWApi.message)" -ForegroundColor Green
    $resGWStudent = Invoke-RestMethod -Uri "http://localhost/student/"
    Write-Host "  -> Gateway /student/ (Mở rộng 9): OK - Lấy được $($resGWStudent.Count) sinh viên" -ForegroundColor Green
    $resGWAuth = Invoke-WebRequest -Uri "http://localhost/auth/" -MaximumRedirection 0 -ErrorAction SilentlyContinue
    Write-Host "  -> Gateway /auth/ (Keycloak): OK (Status: $($resGWAuth.StatusCode))" -ForegroundColor Green
} catch { Write-Host "  -> Gateway lỗi: $_" -ForegroundColor Red }

# 4. Kiểm tra MinIO, Prometheus, Grafana
Write-Host "`n[4] Kiểm thử MinIO, Prometheus, Grafana:" -ForegroundColor Yellow
try {
    $resMinio = Invoke-WebRequest -Uri "http://localhost:9000/minio/health/live" -UseBasicParsing
    Write-Host "  -> MinIO Live Check (9000): OK" -ForegroundColor Green
} catch { Write-Host "  -> MinIO lỗi: $_" -ForegroundColor Red }

try {
    $resProm = Invoke-RestMethod -Uri "http://localhost:9090/api/v1/targets"
    Write-Host "  -> Prometheus Targets (9090): OK - Active Targets: $($resProm.data.activeTargets.Count)" -ForegroundColor Green
} catch { Write-Host "  -> Prometheus lỗi: $_" -ForegroundColor Red }

try {
    $resGrafana = Invoke-RestMethod -Uri "http://localhost:3000/api/health"
    Write-Host "  -> Grafana Health (3000): OK - Database: $($resGrafana.database)" -ForegroundColor Green
} catch { Write-Host "  -> Grafana lỗi: $_" -ForegroundColor Red }

# 5. Kiểm tra thông mạng Ping giữa các container
Write-Host "`n[5] Kiểm thử Ping thông mạng (cloud-net):" -ForegroundColor Yellow
$targets = @("web-frontend-server", "web-frontend-server2", "application-backend-server", "relational-database-server", "authentication-identity-server", "object-storage-server", "internal-dns-server", "monitoring-prometheus-server", "monitoring-grafana-dashboard-server")
foreach ($t in $targets) {
    $pingOut = docker exec api-gateway-proxy-server ping -c 1 $t 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  -> Ping to $t: SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "  -> Ping to $t: FAILED" -ForegroundColor Red
    }
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "                HOÀN TẤT KIỂM THỬ                         " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

