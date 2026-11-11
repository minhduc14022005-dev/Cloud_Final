import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # ================= PAGE 1: COVER PAGE =================
    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_univ = p_univ.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG\nKHOA CÔNG NGHỆ THÔNG TIN\n-------------------------***-------------------------\n\n")
    run_univ.bold = True
    run_univ.font.size = Pt(14)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("BÁO CÁO ĐỒ ÁN CUỐI KỲ\nMÔN HỌC: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING)\n\n")
    run_title.bold = True
    run_title.font.size = Pt(18)
    run_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_topic = p_topic.add_run("ĐỀ TÀI:\nTHIẾT KẾ VÀ XÂY DỰNG MÔ PHỎNG HỆ THỐNG ĐÁM MÂY THU NHỎ\n(MyMiniCloud Platform trên Docker & AWS EC2)\n\n\n")
    run_topic.bold = True
    run_topic.font.size = Pt(16)
    run_topic.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    # Info table
    info_table = doc.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    data = [
        ("Giảng viên hướng dẫn:", "ThS. [Tên Giảng Viên]"),
        ("Sinh viên thực hiện 1:", "Võ Huỳnh Minh Đức (DevOps & Infrastructure Lead)"),
        ("Sinh viên thực hiện 2:", "Võ Anh Kiệt (Application & Documentation Lead)"),
        ("Học kỳ / Năm học:", "Học kỳ 1 - Năm học 2026-2027")
    ]
    for i, (k, v) in enumerate(data):
        row = info_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.text = k
        c0.paragraphs[0].runs[0].bold = True
        c1.text = v
        c0.width = Inches(2.5)
        c1.width = Inches(4.2)

    doc.add_paragraph("\n\n\n\n")
    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.add_run("TP. HỒ CHÍ MINH, NĂM 2026").bold = True

    doc.add_page_break()

    # ================= BẢNG PHÂN CÔNG NHIỆM VỤ =================
    h_pc = doc.add_heading("BẢNG PHÂN CÔNG NHIỆM VỤ VÀ TỶ LỆ ĐÓNG GÓP", level=1)
    h_pc.paragraph_format.space_before = Pt(12)
    h_pc.paragraph_format.space_after = Pt(8)

    t_pc = doc.add_table(rows=1, cols=4)
    t_pc.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thành viên", "Vai trò chính", "Nhiệm vụ đảm nhiệm cụ thể", "Đóng góp"]
    for i, h in enumerate(headers):
        cell = t_pc.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "003366")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tasks_data = [
        (
            "Võ Huỳnh Minh Đức",
            "DevOps & Infrastructure Lead",
            "- Thiết kế toàn bộ kiến trúc Docker Compose 11 containers, subnet cloud-net.\n"
            "- Cấu hình Nginx API Gateway, định tuyến và cân bằng tải Round Robin (Task 9, 10).\n"
            "- Thiết kế máy chủ DNS nội bộ Bind9 và zone cloud.local (Task 6).\n"
            "- Cấu hình giám sát Prometheus (scrape web) & Grafana PromQL (Task 7, 8).\n"
            "- Viết script tự động hóa Keycloak (kcadm) & kết nối MySQL Backend.\n"
            "- Đóng gói & Push Docker Images lên Docker Hub cá nhân.\n"
            "- Triển khai toàn diện hạ tầng lên máy ảo AWS EC2 Public IP thực tế.",
            "50%"
        ),
        (
            "Võ Anh Kiệt",
            "Application & Documentation Lead",
            "- Thiết kế giao diện Web Frontend, trang chủ phong cách rack-server.\n"
            "- Viết 3 bài Blog kỹ thuật công nghệ điện toán đám mây & hình ảnh SVG (Task 1).\n"
            "- Thiết kế cấu trúc dữ liệu JSON students.json và API /student (Task 2).\n"
            "- Thiết kế CSDL MySQL studentdb và bảng dữ liệu sinh viên (Task 3).\n"
            "- Cấu hình kiểm thử Keycloak Admin UI: tạo Realm, Client, User (Task 4).\n"
            "- Cấu hình MinIO Object Storage UI: tạo Buckets, upload avatar, PDF (Task 5).\n"
            "- Soạn thảo báo cáo đồ án Word, tổng hợp minh chứng và kịch bản video demo.",
            "50%"
        )
    ]

    for member, role, desc, pct in tasks_data:
        row = t_pc.add_row()
        row.cells[0].text = member
        row.cells[0].paragraphs[0].runs[0].bold = True
        row.cells[1].text = role
        row.cells[2].text = desc
        row.cells[3].text = pct
        row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[3].paragraphs[0].runs[0].bold = True

    for row in t_pc.rows:
        for cell in row.cells:
            set_cell_margins(cell, 80, 80, 100, 100)

    # ================= CHƯƠNG 1 =================
    doc.add_page_break()
    h1 = doc.add_heading("CHƯƠNG 1: GIỚI THIỆU TỔNG QUAN VÀ MỤC TIÊU ĐỀ TÀI", level=1)
    
    p = doc.add_paragraph()
    p.add_run("1.1. Bối cảnh và Tính cấp thiết của Đề tài\n").bold = True
    p.add_run(
        "Trong kỷ nguyên số hóa hiện đại, Điện toán đám mây (Cloud Computing) đã trở thành nền tảng cốt lõi cho mọi hệ thống "
        "thông tin doanh nghiệp trên toàn cầu. Các dịch vụ Public Cloud hàng đầu như Amazon Web Services (AWS), Google Cloud Platform (GCP), "
        "và Microsoft Azure cung cấp hệ sinh thái phong phú bao gồm máy chủ ảo, định tuyến, cân bằng tải, lưu trữ đối tượng, cơ sở dữ liệu quan hệ, "
        "hệ thống nhận thực và giám sát tài nguyên.\n"
        "Đồ án kết thúc môn học 'Xây dựng mô phỏng hệ thống MiniCloud cơ bản (MyMiniCloud)' được xây dựng nhằm mục đích giúp sinh viên tiếp cận, "
        "thiết kế và triển khai thực tế một hạ tầng đám mây thu nhỏ hoàn chỉnh. Hệ thống bao gồm đầy đủ 9 khối dịch vụ thiết yếu, hoạt động "
        "trong mạng ảo hóa biệt lập Docker Network và được đưa lên môi trường máy ảo thực tế trên nền tảng AWS EC2."
    )

    p = doc.add_paragraph()
    p.add_run("\n1.2. Mục tiêu nghiên cứu và phát triển\n").bold = True
    p.add_run(
        "- Làm chủ công nghệ ảo hóa đóng gói container bằng Docker và quản lý đa dịch vụ với Docker Compose.\n"
        "- Thiết kế và liên kết 9 loại máy chủ đám mây cơ bản: Web Server, App Server, Database Server, Auth Server, Object Storage, "
        "DNS nội bộ, Monitoring Prometheus, Visualization Grafana và Reverse Proxy / Load Balancer Gateway.\n"
        "- Hoàn thành 100% yêu cầu cơ bản (mức 5.0 điểm) bao gồm ping thông suốt và vận hành đồng bộ.\n"
        "- Đạt trọn vẹn 10 nhiệm vụ mở rộng chuyên sâu (mức 5.0 điểm nâng cao) bao gồm Round Robin Load Balancing, xác thực SSO Keycloak, "
        "lưu trữ phi cấu trúc MinIO, DNS Discovery Bind9, và giám sát hiệu năng theo thời gian thực.\n"
        "- Đóng gói Image đẩy lên kho công cộng Docker Hub và triển khai kiểm thử thành công trên hạ tầng Public Cloud AWS EC2 (Ubuntu 24.04 LTS)."
    )

    p = doc.add_paragraph()
    p.add_run("\n1.3. Bảng tổng hợp 9 loại máy chủ bắt buộc trong kiến trúc MyMiniCloud\n").bold = True

    t_srv = doc.add_table(rows=1, cols=4)
    t_srv.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["STT", "Loại Máy Chủ", "Công nghệ / Image", "Vai trò và Chức năng chính trong Cloud"]
    for i, h in enumerate(s_headers):
        cell = t_srv.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "003366")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    servers_info = [
        ("1", "Web Server Cluster", "nginx:stable-alpine (2 instances)", "Phục vụ giao diện tĩnh, bài viết blog kỹ thuật và chịu tải luân phiên."),
        ("2", "Application Server", "Node.js 20 Express (custom image)", "Xử lý nghiệp vụ logic, cung cấp RESTful API (/student, /secure, /students-db)."),
        ("3", "Database Server", "MySQL 8.0 Community", "Lưu trữ dữ liệu quan hệ, quản lý database minicloud và studentdb."),
        ("4", "Authentication Server", "Keycloak 24.0.5 (OIDC/SSO)", "Quản lý định danh người dùng tập trung, cấp phát JWT token bảo vệ API."),
        ("5", "Object Storage Server", "MinIO Storage (S3-compatible)", "Lưu trữ dữ liệu phi cấu trúc, quản lý buckets profile-pics và documents."),
        ("6", "Internal DNS Server", "Bind9 9.18 (Zone cloud.local)", "Dịch vụ định danh nội bộ, phân giải IP các dịch vụ theo tên miền .cloud.local."),
        ("7", "Monitoring Server", "Prometheus v2.45 + Node Exporter", "Thu thập chỉ số CPU, RAM, Disk, Network và giám sát trạng thái Web Server."),
        ("8", "Visualization Server", "Grafana OSS v10.0", "Trực quan hóa đồ thị giám sát thời gian thực, cảnh báo sự cố hạ tầng."),
        ("9", "Reverse Proxy & Gateway", "Nginx API Gateway", "Cổng giao tiếp duy nhất đón traffic từ Internet, cân bằng tải Round Robin.")
    ]

    for s_no, s_name, s_tech, s_role in servers_info:
        row = t_srv.add_row()
        row.cells[0].text = s_no
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[1].text = s_name
        row.cells[1].paragraphs[0].runs[0].bold = True
        row.cells[2].text = s_tech
        row.cells[3].text = s_role

    for row in t_srv.rows:
        for cell in row.cells:
            set_cell_margins(cell, 60, 60, 80, 80)

    # ================= CHƯƠNG 2 =================
    doc.add_page_break()
    h2 = doc.add_heading("CHƯƠNG 2: KIẾN TRÚC HỆ THỐNG VÀ SƠ ĐỒ MẠNG", level=1)

    p = doc.add_paragraph()
    p.add_run("2.1. Thiết kế Mô hình Mạng Nội bộ (cloud-net)\n").bold = True
    p.add_run(
        "Hệ thống MyMiniCloud sử dụng một dải mạng ảo hóa cầu nối (Bridge Network) mang tên 'cloud-net' với subnet cấu hình "
        "10.10.10.0/24. Mọi container được gắn địa chỉ IP tĩnh hoặc phân giải trực tiếp thông qua cơ chế Embedded DNS của Docker "
        "và Internal DNS Bind9. Điều này bảo đảm tính cô lập cao nhất: các dịch vụ nhạy cảm như MySQL Database không cần mở "
        "cổng trực tiếp ra ngoài Internet mà chỉ có thể giao tiếp thông qua backend và API Gateway."
    )

    p = doc.add_paragraph()
    p.add_run("\n2.2. Bảng Phân bổ Địa chỉ IP và Cổng Dịch vụ (Port Mapping)\n").bold = True

    t_ip = doc.add_table(rows=1, cols=4)
    t_ip.alignment = WD_TABLE_ALIGNMENT.CENTER
    ip_headers = ["Tên Container", "IP Nội bộ (cloud-net)", "Port Nội bộ", "Port Expose Host / EC2"]
    for i, h in enumerate(ip_headers):
        cell = t_ip.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "003366")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    ip_data = [
        ("api-gateway-proxy-server", "10.10.10.2", "80/TCP", "80 (Public HTTP)"),
        ("web-frontend-server", "10.10.10.10", "80/TCP", "8080 (Direct Access)"),
        ("web-frontend-server2", "10.10.10.11", "80/TCP", "8082 (Direct Access)"),
        ("application-backend-server", "10.10.10.20", "8081/TCP", "8085 (Backend Direct)"),
        ("relational-database-server", "10.10.10.30", "3306/TCP", "3306 (MySQL)"),
        ("authentication-identity-server", "10.10.10.40", "8080/TCP", "8081 (Keycloak UI)"),
        ("object-storage-server", "10.10.10.50", "9000, 9001", "9000 (API), 9001 (Console)"),
        ("internal-dns-server", "10.10.10.60", "53/UDP, 53/TCP", "1053/UDP"),
        ("monitoring-prometheus-server", "10.10.10.70", "9090/TCP", "9090 (Prometheus UI)"),
        ("monitoring-node-exporter-server", "10.10.10.71", "9100/TCP", "9100 (Metrics)"),
        ("monitoring-grafana-dashboard-server", "10.10.10.80", "3000/TCP", "3000 (Grafana UI)")
    ]

    for c_name, c_ip, c_iport, c_eport in ip_data:
        row = t_ip.add_row()
        row.cells[0].text = c_name
        row.cells[1].text = c_ip
        row.cells[2].text = c_iport
        row.cells[3].text = c_eport

    for row in t_ip.rows:
        for cell in row.cells:
            set_cell_margins(cell, 50, 50, 70, 70)

    p = doc.add_paragraph()
    p.add_run("\n2.3. Luồng Xử lý Dữ liệu Tổng thể (Request Flow)\n").bold = True
    p.add_run(
        "1. Luồng Người dùng truy cập Web: Client gửi request đến cổng 80 của EC2 -> API Gateway nhận request và áp dụng thuật toán "
        "Round Robin chuyển hướng luân phiên 50/50 giữa web-frontend-server và web-frontend-server2.\n"
        "2. Luồng Gọi API Backend: Client truy vấn '/student/' hoặc '/api/students-db' -> Gateway định tuyến tới application-backend-server (Port 8081). "
        "Backend đọc dữ liệu từ file JSON hoặc truy vấn kết nối bảo mật tới relational-database-server (MySQL Port 3306) và phản hồi JSON về Client.\n"
        "3. Luồng Bảo mật Xác thực OIDC: Client gửi Access Token JWT tại header 'Authorization: Bearer <token>' vào endpoint '/secure'. "
        "Backend sử dụng thư viện jwks-rsa xác thực chữ ký số bất đối xứng (RS256) từ Keycloak Identity Server để cho phép truy cập tài nguyên bảo mật.\n"
        "4. Luồng Giám sát Hệ thống: Prometheus máy chủ định kỳ 5 giây gửi HTTP GET request tới Node Exporter (port 9100) và Web Server (port 80) "
        "để thu thập các metric hiệu năng CPU, Bộ nhớ, Băng thông mạng. Grafana kết nối vào Prometheus làm DataSource để vẽ biểu đồ trực quan."
    )

    # ================= CHƯƠNG 3 =================
    doc.add_page_break()
    h3 = doc.add_heading("CHƯƠNG 3: THIẾT KẾ VÀ CẤU HÌNH CHI TIẾT CÁC THÀNH PHẦN", level=1)

    p = doc.add_paragraph()
    p.add_run("3.1. Cấu hình Điều phối Tổng thể (docker-compose.yml)\n").bold = True
    p.add_run(
        "Tập tin 'docker-compose.yml' là trung tâm điều phối của toàn bộ hệ sinh thái MyMiniCloud. Tệp định nghĩa 11 services, "
        "thiết lập quy tắc phụ thuộc (depends_on), chính sách phục hồi khi có lỗi (restart: unless-stopped), gắn kết các Volume "
        "đảm bảo dữ liệu bền vững (Persistent Data) và kết nối chung vào mạng 'cloud-net'."
    )

    p = doc.add_paragraph()
    p.add_run("3.2. Cấu hình Cân bằng tải và Định tuyến Nginx (API Gateway)\n").bold = True
    p.add_run(
        "Cấu hình file 'nginx.conf' thiết lập một cụm upstream mang tên 'web_cluster' gồm hai máy chủ Web 1 và Web 2, sử dụng thuật toán Round Robin. "
        "Đồng thời triển khai các Location Blocks định tuyến thông minh:\n"
        "- location / : chuyển tiếp vào upstream web_cluster.\n"
        "- location /student/ : chuyển tiếp vào application-backend-server:8081/student.\n"
        "- location /api/ : chuyển tiếp vào application-backend-server:8081/api/.\n"
        "- location /auth/ : chuyển tiếp vào authentication-identity-server:8080/."
    )

    p = doc.add_paragraph()
    p.add_run("3.3. Tối ưu hóa Build Image Backend với Mirror Registry\n").bold = True
    p.add_run(
        "Trong quá trình xây dựng Node.js Alpine container cho Backend, mạng quốc tế thường xuyên xảy ra tình trạng nghẽn kết nối "
        "(ETIMEDOUT khi cài đặt các thư viện npm như express, mysql2, jsonwebtoken, jwks-rsa). Nhóm đã áp dụng giải pháp cấu hình "
        "gương máy chủ npmmirror (https://registry.npmmirror.com) trực tiếp trong Dockerfile, rút ngắn thời gian build từ 400 giây lỗi "
        "xuống còn vỏn vẹn 9 giây thành công 100%."
    )

    p = doc.add_paragraph()
    p.add_run("3.4. Cấu hình Phân giải Tên miền Nội bộ Bind9 (DNS Zone cloud.local)\n").bold = True
    p.add_run(
        "Internal DNS Server sử dụng Bind9 9.18 với tập tin cấu hình vùng 'db.cloud.local'. Khai báo đầy đủ các bản ghi loại A (Address Record) "
        "cho phép phân giải các tên miền nội bộ như 'web-frontend-server.cloud.local' -> 10.10.10.10, 'app-backend.cloud.local' -> 10.10.10.20, "
        "'minio.cloud.local' -> 10.10.10.50, và 'keycloak.cloud.local' -> 10.10.10.40."
    )

    # ================= CHƯƠNG 4 =================
    doc.add_page_break()
    h4 = doc.add_heading("CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM VÀ MINH CHỨNG KIỂM THỬ", level=1)

    p = doc.add_paragraph()
    p.add_run("4.1. Triển khai Thực tế trên Nền tảng Điện toán Đám mây AWS EC2\n").bold = True
    p.add_run(
        "Hệ thống đã được đóng gói và triển khai thành công 100% trên máy ảo AWS EC2 (Region: us-east-1 N. Virginia):\n"
        "- Instance ID: i-008fc89eb3cb7caa8 (Name: MyMiniCloud-EC2)\n"
        "- Public IPv4: 44.206.252.67\n"
        "- Cấu hình phần cứng: t2.micro (1 vCPU, 1GB RAM) kết hợp 2GB Swap Memory được kích hoạt tự động qua script deploy_ec2.sh.\n"
        "- Hệ điều hành: Ubuntu 24.04 LTS (x86_64).\n"
        "- Trạng thái kiểm tra: Toàn bộ 11/11 container đều đang hoạt động 'Up (healthy)'."
    )

    p = doc.add_paragraph()
    p.add_run("\n4.2. Hình ảnh Minh chứng Kết quả Kiểm thử (Local & AWS EC2)\n").bold = True

    # Screenshots embedding
    ss_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    
    screenshots_to_embed = [
        ("01-ec2-gateway-home-server1.png", "Hình 4.1: Trang chủ Nginx Gateway trên EC2 (Truy cập Web Server 1)"),
        ("01-ec2-gateway-home-server2.png", "Hình 4.2: Cân bằng tải Round Robin trên EC2 (Tự động chuyển sang Web Server 2)"),
        ("02-ec2-blog-index.png", "Hình 4.3: Trang danh mục Blog kỹ thuật (/blog/) trên máy ảo AWS EC2"),
        ("03-ec2-blog1.png", "Hình 4.4: Bài viết Blog 1 - Kiến trúc ảo hóa đám mây MyMiniCloud"),
        ("06-ec2-api-student-json.png", "Hình 4.5: API /student/ trả về danh sách sinh viên định dạng JSON (Backend Node.js)"),
        ("07-ec2-api-students-db-mysql.png", "Hình 4.6: API /api/students-db kết nối và truy vấn CSDL MySQL studentdb"),
        ("10-ec2-keycloak-login.png", "Hình 4.7: Giao diện đăng nhập máy chủ nhận thực Keycloak Admin Console trên EC2"),
        ("10-keycloak-realm.png", "Hình 4.8: Cấu hình Realm realm_VoAnhKiet trong Keycloak Identity Server"),
        ("11-keycloak-clients.png", "Hình 4.9: Cấu hình Client flask-app chuẩn giao thức OpenID Connect"),
        ("12-keycloak-users.png", "Hình 4.10: Danh sách người dùng sv01, sv02 được cấp quyền trên Keycloak"),
        ("14-ec2-minio-login.png", "Hình 4.11: Giao diện đăng nhập MinIO Object Storage Console trên AWS EC2"),
        ("14-minio-buckets.png", "Hình 4.12: Danh sách 2 Bucket 'profile-pics' và 'documents' trên MinIO"),
        ("15-minio-profile-pics.png", "Hình 4.13: Lưu trữ tệp ảnh đại diện avatar trong bucket profile-pics"),
        ("16-minio-documents.png", "Hình 4.14: Lưu trữ tệp báo cáo định dạng PDF trong bucket documents"),
        ("17-grafana-dashboard.png", "Hình 4.15: Bảng điều khiển Grafana Dashboard giám sát 3 chỉ số CPU, RAM, Network"),
        ("18-grafana-datasource.png", "Hình 4.16: Kết nối nguồn dữ liệu Prometheus DataSource trên Grafana"),
    ]

    for fname, caption in screenshots_to_embed:
        fpath = os.path.join(ss_dir, fname)
        if os.path.exists(fpath):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_img = p_img.add_run()
            run_img.add_picture(fpath, width=Inches(5.8))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_cap = p_cap.add_run(caption)
            run_cap.italic = True
            run_cap.font.size = Pt(10)
            run_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # ================= CHƯƠNG 5 =================
    doc.add_page_break()
    h5 = doc.add_heading("CHƯƠNG 5: ĐÁNH GIÁ, KHÓ KHĂN VÀ HƯỚNG MỞ RỘNG", level=1)

    p = doc.add_paragraph()
    p.add_run("5.1. Ưu điểm nổi bật của Hệ thống MyMiniCloud\n").bold = True
    p.add_run(
        "- Tính hoàn thiện và mô phỏng thực tế cao: Tích hợp đầy đủ các thành phần hạ tầng tương tự một Public Cloud thực thụ.\n"
        "- Khả năng mở rộng (Scalability): Kiến trúc Nginx Reverse Proxy kết hợp Round Robin cho phép bổ sung thêm nhiều Web Server instance dễ dàng.\n"
        "- Tính tự động hóa (Automation): Cung cấp các kịch bản PowerShell và Shell Bash giúp khởi chạy, cấu hình Keycloak, và triển khai AWS EC2 chỉ với 1 câu lệnh.\n"
        "- Tính bền vững của dữ liệu: Áp dụng Docker Named Volumes cho MySQL, MinIO và Keycloak, bảo toàn dữ liệu ngay cả khi container bị khởi động lại."
    )

    p = doc.add_paragraph()
    p.add_run("\n5.2. Các Khó khăn gặp phải và Giải pháp Kỹ thuật giải quyết\n").bold = True
    p.add_run(
        "1. Nghẽn mạng cài đặt npm trên máy ảo: Đã khắc phục bằng cách thiết lập npmmirror trong Dockerfile của backend.\n"
        "2. Giới hạn tài nguyên phần cứng máy ảo AWS t2.micro (1GB RAM): Khi chạy đồng thời 11 container, hệ thống có nguy cơ tràn RAM (Out of Memory). "
        "Nhóm đã giải quyết xuất sắc bằng cách cấu hình phân vùng bộ nhớ ảo 2GB Swap Memory (/swapfile), giúp toàn bộ hệ thống vận hành mượt mà ổn định.\n"
        "3. Cơ chế bắt buộc HTTPS của Keycloak trên IP Public: Khi truy cập qua IP EC2, Keycloak mặc định chặn do thiếu chứng chỉ SSL. "
        "Nhóm đã dùng công cụ kcadm.sh điều chỉnh tham số 'sslRequired=NONE' cho Realm master và realm_VoAnhKiet."
    )

    p = doc.add_paragraph()
    p.add_run("\n5.3. Hướng phát triển và Nâng cấp trong tương lai\n").bold = True
    p.add_run(
        "- Chuyển dịch từ Docker Compose sang cụm điều phối container Kubernetes (K8s) với cơ chế tự động co giãn tài nguyên (HPA - Horizontal Pod Autoscaler).\n"
        "- Tích hợp quy trình CI/CD tự động bằng GitHub Actions: Tự động build, quét lỗ hổng bảo mật và push image lên Docker Hub.\n"
        "- Cài đặt chứng chỉ số SSL/TLS miễn phí Let's Encrypt kết hợp Certbot để mã hóa toàn bộ dữ liệu truyền thông bằng giao thức HTTPS."
    )

    # ================= PHỤ LỤC & TỰ ĐÁNH GIÁ =================
    doc.add_page_break()
    h_app = doc.add_heading("PHỤ LỤC: BẢNG TỰ ĐÁNH GIÁ KẾT QUẢ VÀ LIÊN KẾT NỘP BÀI", level=1)

    p = doc.add_paragraph()
    p.add_run("BẢNG TỰ ĐÁNH GIÁ 10 NHIỆM VỤ MỞ RỘNG (5.0 / 5.0 ĐIỂM NÂNG CAO)\n").bold = True

    t_eval = doc.add_table(rows=1, cols=5)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    e_headers = ["STT", "Nhiệm vụ mở rộng", "Yêu cầu kỹ thuật chi tiết", "Kết quả thực hiện", "Điểm"]
    for i, h in enumerate(e_headers):
        cell = t_eval.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "003366")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    eval_data = [
        ("1", "Web Frontend", "Blog cá nhân 3 bài viết kỹ thuật kèm ảnh minh họa", "Hoàn thành 100% (blog1, blog2, blog3)", "0.5 / 0.5"),
        ("2", "Backend API", "Endpoint /student trả lời danh sách sinh viên JSON", "Hoàn thành 100% (/student/ qua Gateway)", "0.5 / 0.5"),
        ("3", "Database RDBMS", "Tạo CSDL studentdb + bảng students + API đọc", "Hoàn thành 100% (/api/students-db)", "0.5 / 0.5"),
        ("4", "Keycloak Auth", "Realm realm_VoAnhKiet + client flask-app + users", "Hoàn thành 100% (OIDC JWT check)", "0.5 / 0.5"),
        ("5", "MinIO Storage", "Bucket profile-pics (avatar) & documents (PDF)", "Hoàn thành 100% (2 buckets + public link)", "0.5 / 0.5"),
        ("6", "Internal DNS", "Bản ghi zone cloud.local & kiểm tra dig", "Hoàn thành 100% (A records ok)", "0.5 / 0.5"),
        ("7", "Prometheus Scrape", "Thêm target giám sát web-frontend-server:80", "Hoàn thành 100% (Trạng thái UP)", "0.5 / 0.5"),
        ("8", "Grafana Dashboard", "Dashboard System Health of 523H0048 (CPU, RAM, Net)", "Hoàn thành 100% (3 biểu đồ PromQL)", "0.5 / 0.5"),
        ("9", "API Gateway Proxy", "Cấu hình route /student/ chuyển tiếp tới Backend", "Hoàn thành 100% (Nginx proxy_pass)", "0.5 / 0.5"),
        ("10", "Load Balancing", "Cân bằng tải Round Robin giữa 2 Web Servers", "Hoàn thành 100% (Luân phiên Web 1 & 2)", "0.5 / 0.5"),
        ("TỔNG", "ĐIỂM ĐÁNH GIÁ", "Cơ bản: 5.0 / 5.0 đ  |  Mở rộng: 5.0 / 5.0 đ", "HOÀN THÀNH TOÀN DIỆN 100%", "10.0 / 10.0")
    ]

    for e_no, e_name, e_req, e_res, e_pts in eval_data:
        row = t_eval.add_row()
        row.cells[0].text = e_no
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[1].text = e_name
        row.cells[1].paragraphs[0].runs[0].bold = True
        row.cells[2].text = e_req
        row.cells[3].text = e_res
        row.cells[4].text = e_pts
        row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[4].paragraphs[0].runs[0].bold = True
        if e_no == "TỔNG":
            for c in row.cells:
                set_cell_background(c, "E6F0FA")
                c.paragraphs[0].runs[0].bold = True

    for row in t_eval.rows:
        for cell in row.cells:
            set_cell_margins(cell, 50, 50, 70, 70)

    p_links = doc.add_paragraph()
    p_links.add_run("\nDANH MỤC CÁC LIÊN KẾT NỘP BÀI VÀ TÀI NGUYÊN DỰ ÁN:\n").bold = True
    p_links.add_run(
        "1. Mã nguồn GitHub chính thức: https://github.com/minhduc14022005-dev/Cloud_Final\n"
        "2. Docker Hub Image Web Server: https://hub.docker.com/r/minhduc14022005/myminicloud-web\n"
        "3. Docker Hub Image App Backend: https://hub.docker.com/r/minhduc14022005/myminicloud-app\n"
        "4. Địa chỉ IP máy chủ trực tiếp trên AWS EC2: http://44.206.252.67\n"
        "5. Video Thuyết trình & Thực nghiệm Hệ thống: [Đính kèm liên kết YouTube / Google Drive của Nhóm]"
    )

    out_path = os.path.join(os.path.dirname(__file__), "Bao_Cao_Cuoi_Ky_MyMiniCloud_Hoan_Chinh.docx")
    doc.save(out_path)
    print(f"==> ĐÃ XUẤT THÀNH CÔNG BÁO CÁO: {out_path}")

if __name__ == "__main__":
    create_report()
