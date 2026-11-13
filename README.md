# MyMiniCloud Platform ☁️
> **Hệ sinh thái Điện toán Đám mây Thu nhỏ (MiniCloud Simulation Platform)**  
> Đồ án Cuối kỳ môn **Điện toán Đám mây (Cloud Computing)** — Khoa Công nghệ Thông tin, Trường Đại học Tôn Đức Thắng (TDTU).

---

## 👨‍💻 Thông Tin Nhóm Sinh Viên & Giảng Viên

* **Giảng viên hướng dẫn:** TS. Bùi Quy Anh
* **Thành viên thực hiện:**
  1. **Võ Huỳnh Minh Đức** — MSSV: `523H0014` (*DevOps & Infrastructure Lead*)
  2. **Võ Anh Kiệt** — MSSV: `523H0048` (*Application & Documentation Lead*)

---

## 🌐 Thông Tin Triển Khai Thực Tế

* **Máy chủ Đám mây thực tế (AWS EC2):** [http://44.206.252.67/](http://44.206.252.67/)
* **Kho lưu trữ Docker Hub Registry:** [https://hub.docker.com/u/minhduc14022005](https://hub.docker.com/u/minhduc14022005)
* **Kho mã nguồn GitHub:** [https://github.com/minhduc14022005-dev/Cloud_Final](https://github.com/minhduc14022005-dev/Cloud_Final)

---

## 🏛️ Kiến Trúc Hệ Thống & Danh Mục 11 Máy Chủ

Toàn bộ hệ thống được cô lập và liên lạc nội bộ thông qua mạng ảo cầu nối **`cloud-net`** (Subnet `10.10.10.0/24`), được điều phối tự động bởi Docker Compose.

| STT | Tên Container | Vai trò Dịch vụ | Công nghệ / Image | Port Mạng Host | Địa chỉ IP Nội bộ |
| :---: | :--- | :--- | :--- | :---: | :---: |
| 1 | `api-gateway-proxy-server` | Cổng duy nhất, định tuyến & cân bằng tải | Nginx (`nginx:stable`) | `80:80` | `10.10.10.80` |
| 2 | `web-frontend-server` | Máy chủ Web tĩnh 1 | Nginx (`minhduc14022005/myminicloud-web:v1`) | `8080:80` | `10.10.10.10` |
| 3 | `web-frontend-server2` | Máy chủ Web tĩnh 2 (Round Robin) | Nginx (`minhduc14022005/myminicloud-web2:v1`) | `8082:80` | `10.10.10.11` |
| 4 | `application-backend-server` | REST API (/hello, /student, /students-db, /secure) | Node.js Express (`minhduc14022005/myminicloud-app:v1`) | `8085:8081` | `10.10.10.20` |
| 5 | `relational-database-server` | Cơ sở dữ liệu quan hệ | MySQL 8.0 (`mysql:8.0`) | `3306:3306` | `10.10.10.50` |
| 6 | `authentication-identity-server`| Định danh & xác thực OIDC | Keycloak 26.8.1 | `8081:8080` | `10.10.10.40` |
| 7 | `object-storage-server` | Lưu trữ đối tượng S3 | MinIO (`elestio/minio`, ghim digest) | `9000:9000`, `9001:9001` | `10.10.10.30` |
| 8 | `internal-dns-server` | Phân giải tên miền nội bộ `cloud.local` | Bind9 (`internetsystemsconsortium/bind9:9.18`) | `1053:53/udp` | `10.10.10.53` |
| 9 | `monitoring-prometheus-server` | Thu thập chỉ số | Prometheus v3.15.1 | `9090:9090` | `10.10.10.70` |
| 10 | `monitoring-node-exporter-server` | Đo tài nguyên máy chủ | Node Exporter v1.12.1 | `9100:9100` | `10.10.10.71` |
| 11 | `monitoring-grafana-dashboard-server`| Dashboard giám sát | Grafana 13.3.0 | `3000:3000` | `10.10.10.72` |

Mỗi container còn có tên ngắn (alias) trong `cloud-net` để chạy y nguyên lệnh của đề: `web`, `web2`, `app-server`, `db`, `keycloak`, `minio`, `dns-server`, `prometheus`, `node-exporter`, `grafana`, `proxy` (ví dụ `ping -c 3 db`, `mysql -h db ...`).

---

## 🚀 Hoàn Thành Trọn Vẹn 10/10 Mục Tiêu Mở Rộng

1. **Mục mở rộng 1 (Web Blog):** Xây dựng Blog kỹ thuật tại `/blog/` kèm **Sơ đồ kiến trúc dạng vector SVG** và 3 bài viết chuyên sâu.
2. **Mục mở rộng 2 (API JSON Sinh viên):** Endpoint `/student/` trả về định dạng chuẩn JSON thông tin các thành viên trong nhóm.
3. **Mục mở rộng 3 (MySQL Database):** Cơ sở dữ liệu `studentdb` với bảng `students`, cung cấp endpoint `/api/students-db` truy vấn động từ CSDL.
4. **Mục mở rộng 4 (IAM Keycloak):** Realm `realm_523H0048`, user `sv01`/`sv02`, client public `flask-app`; audience mapper cho token `aud=flask-app`; backend kiểm tra chữ ký, issuer và audience khi gọi `/api/secure`.
5. **Mục mở rộng 5 (MinIO S3):** Khởi tạo 2 bucket `profile-pics` (ảnh đại diện) và `documents` (tài liệu PDF) kiểm thử upload/download.
6. **Mục mở rộng 6 (Internal DNS Bind9):** Cấu hình zone `cloud.local`, phân giải tên miền `web.cloud.local` và `api.cloud.local` qua lệnh `dig`.
7. **Mục mở rộng 7 (Prometheus Targets):** Tự động cào chỉ số giám sát từ `node-exporter` và `web-frontend-server` (Target UP 1/1).
8. **Mục mở rộng 8 (Grafana Dashboard):** Thiết kế Dashboard *System Health* gồm 3 biểu đồ trực quan sóng dữ liệu: CPU Usage, RAM Usage, Network Traffic.
9. **Mục mở rộng 9 (API Gateway Routing):** Nginx tiếp nhận toàn bộ lưu lượng qua cổng 80, định tuyến an toàn tới Web và API Backend.
10. **Mục mở rộng 10 (Cân bằng tải Round Robin):** Nginx phân phối tải luân phiên giữa `web-frontend-server` và `web-frontend-server2`.

---

## 🛠️ Hướng Dẫn Khởi Động & Triển Khai

### 1. Yêu cầu Tiên quyết
* Docker Engine (>= 24.0.0)
* Docker Compose (>= 2.20.0)
* Git

### 2. Triển khai Nhanh bằng Docker Compose
```bash
# 1. Clone repository
git clone https://github.com/minhduc14022005-dev/Cloud_Final.git
cd Cloud_Final

# 2. Khởi chạy toàn bộ 11 containers vi dịch vụ
sudo docker compose up -d --build

# 3. Kiểm tra trạng thái sức khỏe các containers
sudo docker compose ps
```

### 3. Kiểm thử Kiểm tra Dịch vụ (Health Check)
```bash
# Kiểm tra trang chủ Web & Cân bằng tải
curl -i http://localhost/

# Kiểm tra API danh sách sinh viên
curl http://localhost/student/

# Kiểm tra API kết nối MySQL
curl http://localhost/api/students-db

# Kiểm tra phân giải tên miền Bind9 DNS
dig @127.0.0.1 -p 1053 web.cloud.local +short
```

---

## 🎥 PHÂN CÔNG THỰC HIỆN & TRÌNH BÀY VIDEO DEMO (50 / 50)

| Thành viên | Trách nhiệm Đồ án | Phần trình bày trong Video Demo | Thời lượng |
| :--- | :--- | :--- | :---: |
| **Võ Huỳnh Minh Đức**<br>*(MSSV: 523H0014)* | **Hạ tầng & Vận hành (DevOps):**<br>• Triển khai máy ảo AWS EC2.<br>• Viết `docker-compose.yml`, mạng `cloud-net`.<br>• Cấu hình Nginx API Gateway & Cân bằng tải Round Robin.<br>• Cấu hình Keycloak OIDC, DNS Bind9, Prometheus, Grafana.<br>• Build & Push images lên Docker Hub. | **Phần 1: Khởi đầu & Hạ tầng Cloud (00:00 – 02:45)**<br>1. Giới thiệu tên, đề tài, chào GVHD.<br>2. Show AWS Console (EC2 running, Public IP `44.206.252.67`).<br>3. Terminal SSH gõ `docker compose ps` show 11 containers `Up`.<br>4. Trình duyệt F5 liên tục show Cân bằng tải Round Robin (Task 10).<br><br>**Phần 3: Quản trị & Giám sát (05:15 – 07:15)**<br>1. Show Keycloak Admin Console (Realm, Client, User - Task 4).<br>2. Terminal gõ lệnh `dig` phân giải DNS Bind9 (Task 6).<br>3. Show Prometheus targets `UP 1/1` (Task 7).<br>4. Show Grafana Dashboard 3 biểu đồ CPU, RAM, Network (Task 8). | **~4.5 phút** |
| **Võ Anh Kiệt**<br>*(MSSV: 523H0048)* | **Ứng dụng & Dữ liệu (Fullstack/Data):**<br>• Xây dựng Web Blog HTML/CSS tĩnh.<br>• Thiết kế Sơ đồ Kiến trúc hệ thống dạng vector SVG.<br>• Lập trình Node.js Express REST API (`/student`).<br>• Thiết kế CSDL MySQL 8 (`studentdb`, bảng `students`).<br>• Cấu hình MinIO S3 Object Storage, upload avatar và PDF.<br>• Biên soạn Báo cáo học thuật cuối kỳ `CK_523H0014_523H0048.docx`. | **Phần 2: Ứng dụng, API & Lưu trữ S3 (02:45 – 05:15)**<br>1. Show trang `/blog/`, thuyết minh sơ đồ SVG và 3 bài blog (Task 1).<br>2. Show API `/student/` trả về JSON danh sách sinh viên (Task 2 & 9).<br>3. Show API `/api/students-db` chứng minh đọc dữ liệu từ MySQL (Task 3).<br>4. Đăng nhập MinIO `:9001`, show 2 bucket `profile-pics` & `documents`, mở xem avatar và PDF (Task 5).<br><br>**Phần 4: Kết thúc nghiệm thu (07:15 – 08:00)**<br>1. Cùng Đức mở trang Docker Hub & GitHub.<br>2. Kết luận hoàn thành 10/10 mục mở rộng và cảm ơn thầy. | **~3.5 phút** |

---

## 📄 Tài Liệu Báo Cáo
Báo cáo kỹ thuật chi tiết theo chuẩn học thuật được lưu trữ tại:
* [Báo cáo đồ án định dạng Word](file:///doc/CK_523H0014_523H0048.docx)

