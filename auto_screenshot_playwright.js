const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.join(__dirname, 'doc', 'screenshots');
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const EC2_IP = '44.206.252.67';

async function main() {
    console.log('==> Khởi động Chromium tự động hóa...');
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1440, height: 900 }
    });
    const page = await context.newPage();

    // 1. Home Server 1
    console.log('==> [1/9] Chụp Trang chủ Server 1 (Port 80)...');
    await page.goto(`http://${EC2_IP}/`, { waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, '01-ec2-gateway-home-server1.png') });

    // 2. Home Server 2 (Reload để Round Robin đổi server)
    console.log('==> [2/9] Tải lại trang chụp Server 2 (Round Robin Load Balancer)...');
    await page.reload({ waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, '01-ec2-gateway-home-server2.png') });

    // 3. Blog Index
    console.log('==> [3/9] Chụp trang danh sách Blog...');
    await page.goto(`http://${EC2_IP}/blog/`, { waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, '02-ec2-blog-index.png') });

    // 4. Blog Bài 1
    console.log('==> [4/9] Chụp Blog Bài 1 (Kiến trúc Cloud)...');
    await page.goto(`http://${EC2_IP}/blog/blog1.html`, { waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, '03-ec2-blog1.png') });

    // 5. API Student JSON
    console.log('==> [5/9] Chụp API /student (JSON)...');
    await page.goto(`http://${EC2_IP}/student/`, { waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, '06-ec2-api-student-json.png') });

    // 6. API MySQL DB
    console.log('==> [6/9] Chụp API /api/students-db (MySQL Database)...');
    await page.goto(`http://${EC2_IP}/api/students-db`, { waitUntil: 'load', timeout: 15000 });
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(OUTPUT_DIR, '07-ec2-api-students-db-mysql.png') });

    // 7. Keycloak Login
    console.log('==> [7/9] Chụp Keycloak Authentication Server...');
    try {
        await page.goto(`http://${EC2_IP}:8081/`, { waitUntil: 'load', timeout: 15000 });
        await page.waitForTimeout(2000);
        await page.screenshot({ path: path.join(OUTPUT_DIR, '10-ec2-keycloak-login.png') });
    } catch (e) {
        console.log('  Lỗi Keycloak:', e.message);
    }

    // 8. MinIO Console
    console.log('==> [8/9] Chụp MinIO Object Storage Console...');
    try {
        await page.goto(`http://${EC2_IP}:9001/`, { waitUntil: 'load', timeout: 15000 });
        await page.waitForTimeout(2000);
        await page.screenshot({ path: path.join(OUTPUT_DIR, '14-ec2-minio-login.png') });
    } catch (e) {
        console.log('  Lỗi MinIO:', e.message);
    }

    // 9. Grafana Dashboard
    console.log('==> [9/9] Chụp Grafana Monitoring Dashboard...');
    try {
        await page.goto(`http://${EC2_IP}:3000/`, { waitUntil: 'load', timeout: 15000 });
        await page.waitForTimeout(2000);
        await page.screenshot({ path: path.join(OUTPUT_DIR, '17-ec2-grafana-login.png') });
    } catch (e) {
        console.log('  Lỗi Grafana:', e.message);
    }

    await browser.close();
    console.log('==> HOÀN TẤT TỰ ĐỘNG CHỤP MÀN HÌNH 100%! Đã lưu vào doc/screenshots/');
}

main().catch(console.error);

