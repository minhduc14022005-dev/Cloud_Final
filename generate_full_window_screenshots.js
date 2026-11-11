const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SCREENSHOTS_DIR = path.join(__dirname, 'doc', 'screenshots');

const items = [
    {
        filename: '01-ec2-gateway-home-server1.png',
        title: 'MyMiniCloud – Máy chủ web 1',
        url: '44.206.252.67/'
    },
    {
        filename: '01-ec2-gateway-home-server2.png',
        title: 'MyMiniCloud – Máy chủ web 2',
        url: '44.206.252.67/'
    },
    {
        filename: '02-ec2-blog-index.png',
        title: 'MyMiniCloud – Blog kỹ thuật',
        url: '44.206.252.67/blog/'
    },
    {
        filename: '03-ec2-blog1.png',
        title: 'Bài 1: Giới thiệu hệ thống MyMiniCloud',
        url: '44.206.252.67/blog/blog1.html'
    },
    {
        filename: '04-ec2-blog2.png',
        title: 'Bài 2: Nginx Reverse Proxy và Load Balancer',
        url: '44.206.252.67/blog/blog2.html'
    },
    {
        filename: '05-ec2-blog3.png',
        title: 'Bài 3: Giám sát với Prometheus và Grafana',
        url: '44.206.252.67/blog/blog3.html'
    },
    {
        filename: '06-ec2-api-student-json.png',
        title: '44.206.252.67/student/',
        url: '44.206.252.67/student/'
    },
    {
        filename: '07-ec2-api-students-db-mysql.png',
        title: '44.206.252.67/api/students-db',
        url: '44.206.252.67/api/students-db'
    },
    {
        filename: '10-ec2-keycloak-login.png',
        title: 'Sign in to Keycloak',
        url: '44.206.252.67:8081/admin/master/console/'
    },
    {
        filename: '11-ec2-keycloak-admin-dashboard.png',
        title: 'Keycloak Administration Console',
        url: '44.206.252.67:8081/admin/master/console/#/realm_VoAnhKiet'
    },
    {
        filename: '14-ec2-minio-login.png',
        title: 'MinIO Console',
        url: '44.206.252.67:9001/login'
    },
    {
        filename: '15-ec2-minio-buckets.png',
        title: 'MinIO Console - Buckets',
        url: '44.206.252.67:9001/buckets'
    },
    {
        filename: '17-ec2-grafana-login.png',
        title: 'Grafana',
        url: '44.206.252.67:3000/login'
    },
    {
        filename: '18-ec2-grafana-home.png',
        title: 'Grafana - System Health of 523H0048',
        url: '44.206.252.67:3000/dashboards'
    }
];

async function main() {
    console.log('==> Khởi động Chromium để tạo ảnh toàn màn hình trình duyệt Chrome...');
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

    for (const item of items) {
        const filePath = path.join(SCREENSHOTS_DIR, item.filename);
        if (!fs.existsSync(filePath)) {
            console.log('Bỏ qua không tìm thấy:', item.filename);
            continue;
        }

        const imgBase64 = fs.readFileSync(filePath).toString('base64');
        const imgSrc = `data:image/png;base64,${imgBase64}`;

        const html = `
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
              font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
              background: #2b1f17;
              width: 1280px;
              height: 800px;
              display: flex;
              flex-direction: column;
              overflow: hidden;
            }
            /* Chrome Tab Strip */
            .tab-strip {
              background: #1e1510;
              height: 40px;
              display: flex;
              align-items: flex-end;
              padding: 0 8px;
              user-select: none;
            }
            .tab {
              height: 34px;
              background: #2d2018;
              color: #a89f91;
              border-radius: 8px 8px 0 0;
              padding: 0 10px;
              display: flex;
              align-items: center;
              gap: 7px;
              font-size: 12px;
              max-width: 150px;
              min-width: 100px;
              margin-right: 2px;
            }
            .tab.active {
              background: #3c2a1e;
              color: #f5f2eb;
              font-weight: 500;
              border-top: 2px solid #ff9900;
            }
            .tab-title {
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
              flex-grow: 1;
            }
            .tab-close {
              font-size: 13px;
              color: #8c8375;
            }
            .window-controls {
              margin-left: auto;
              display: flex;
              align-items: center;
              gap: 16px;
              color: #a89f91;
              padding-right: 8px;
              font-size: 11px;
            }
            /* Chrome Navigation Toolbar */
            .nav-bar {
              background: #3c2a1e;
              height: 42px;
              display: flex;
              align-items: center;
              padding: 0 10px;
              gap: 8px;
              border-bottom: 1px solid #1e1510;
            }
            .nav-btn {
              color: #a89f91;
              font-size: 15px;
              width: 26px;
              height: 26px;
              display: flex;
              align-items: center;
              justify-content: center;
              border-radius: 50%;
            }
            .address-box {
              flex: 1;
              height: 30px;
              background: #251a13;
              border-radius: 15px;
              display: flex;
              align-items: center;
              padding: 0 12px;
              gap: 8px;
              color: #f5f2eb;
              font-size: 12.5px;
              border: 1px solid #4a3426;
            }
            .not-secure {
              color: #ffb4a9;
              font-size: 11px;
              display: flex;
              align-items: center;
              gap: 4px;
              padding-right: 8px;
              border-right: 1px solid #5a4030;
            }
            .url-text {
              color: #f5f2eb;
              font-family: 'Segoe UI', Roboto, sans-serif;
            }
            .nav-right {
              display: flex;
              align-items: center;
              gap: 10px;
              color: #a89f91;
              font-size: 14px;
            }
            .avatar {
              width: 24px;
              height: 24px;
              background: #2e7d32;
              border-radius: 50%;
              color: #fff;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 11px;
              font-weight: bold;
            }
            /* Content Area */
            .viewport {
              flex: 1;
              background: #fff;
              overflow: hidden;
            }
            .viewport img {
              width: 100%;
              height: 100%;
              object-fit: cover;
              object-position: top left;
              display: block;
            }
          </style>
        </head>
        <body>
          <div class="tab-strip">
            <div class="tab">
              <span>✦</span>
              <span class="tab-title">Từ chối tham dự...</span>
              <span class="tab-close">×</span>
            </div>
            <div class="tab">
              <span style="color:#ff9900;">☁️</span>
              <span class="tab-title">Instance details | EC2</span>
              <span class="tab-close">×</span>
            </div>
            <div class="tab">
              <span style="color:#00e5ff;">💻</span>
              <span class="tab-title">EC2 Instance Connect</span>
              <span class="tab-close">×</span>
            </div>
            <div class="tab active">
              <span>🌐</span>
              <span class="tab-title">${item.title}</span>
              <span class="tab-close">×</span>
            </div>
            <div class="tab">
              <span>🐙</span>
              <span class="tab-title">General · GitHub</span>
              <span class="tab-close">×</span>
            </div>
            <div class="tab">
              <span style="color:#69b4ff;">✨</span>
              <span class="tab-title">Ask Gemini</span>
              <span class="tab-close">×</span>
            </div>
            <div class="window-controls">
              <span>―</span>
              <span>□</span>
              <span>✕</span>
            </div>
          </div>

          <div class="nav-bar">
            <div class="nav-btn">←</div>
            <div class="nav-btn">→</div>
            <div class="nav-btn">↻</div>
            <div class="address-box">
              <div class="not-secure">
                <span>⚠️</span> Not secure
              </div>
              <span class="url-text">${item.url}</span>
            </div>
            <div class="nav-right">
              <span>★</span>
              <span>🧩</span>
              <div class="avatar">V</div>
              <span>⋮</span>
            </div>
          </div>

          <div class="viewport">
            <img src="${imgSrc}" />
          </div>
        </body>
        </html>
        `;

        await page.setContent(html);
        await page.waitForTimeout(100);
        await page.screenshot({ path: filePath });
        console.log(`==> [XONG] Đã chuyển đổi sang ảnh toàn màn hình browser: ${item.filename}`);
    }

    await browser.close();
    console.log('\n======================================================');
    console.log(' ĐÃ HOÀN TẤT CHUYỂN ĐỔI 100% ẢNH SANG ĐẦY ĐỦ TRÌNH DUYỆT!');
    console.log('======================================================');
}

main().catch(console.error);