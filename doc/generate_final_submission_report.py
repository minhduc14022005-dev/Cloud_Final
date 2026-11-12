import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
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

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.italic = True
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(8)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.bold = True
    run.font.size = Pt(15)
    run.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.bold = True
    run.font.size = Pt(12)
    return h

def add_body_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.25
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
    p.add_run(text)
    return p

def add_bullet_item(doc, bold_title, content):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.2
    r_b = p.add_run(bold_title + ": ")
    r_b.bold = True
    p.add_run(content)
    return p

def main():
    doc = docx.Document()

    # TDTU Standard Page Margins (cm to inches: Top 3.5cm=1.38, Bottom 3.0cm=1.18, Left 3.5cm=1.38, Right 2.0cm=0.79)
    for s in doc.sections:
        s.top_margin = Inches(1.38)
        s.bottom_margin = Inches(1.18)
        s.left_margin = Inches(1.38)
        s.right_margin = Inches(0.79)

    # Base Font
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    logo_path = os.path.join(os.path.dirname(__file__), 'extracted_assets', 'image1.png')
    ss_ec2_dir = os.path.join(os.path.dirname(__file__), 'screenshots-ec2')

    # ================= 1. TRANG BÌA CHÍNH (COVER 1) =================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("TỔNG LIÊN ĐOÀN LAO ĐỘNG VIỆT NAM\nTRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG\nKHOA CÔNG NGHỆ THÔNG TIN")
    r.bold = True
    r.font.size = Pt(13)

    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(18)
        p_logo.paragraph_format.space_after = Pt(18)
        p_logo.add_run().add_picture(logo_path, width=Inches(2.2))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BÁO CÁO CUỐI KỲ\n")
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("MÔN HỌC: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING)\n\n")
    r_sub.bold = True
    r_sub.font.size = Pt(13)

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_topic.add_run("ĐỀ TÀI:\nTHIẾT KẾ VÀ XÂY DỰNG MÔ PHỎNG HỆ THỐNG ĐÁM MÂY THU NHỎ\n(MyMiniCloud Platform trên Docker & AWS EC2)\n\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    p_sv = doc.add_paragraph()
    p_sv.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sv.paragraph_format.space_before = Pt(24)
    r_sv_title = p_sv.add_run("Sinh viên thực hiện:\n")
    r_sv_title.bold = True
    r_sv_title.font.size = Pt(13)
    
    r_sv1 = p_sv.add_run("1. Võ Huỳnh Minh Đức – MSSV: 523H0014\n")
    r_sv1.bold = True
    r_sv1.font.size = Pt(13)
    r_sv2 = p_sv.add_run("2. Võ Anh Kiệt – MSSV: 523H0048\n")
    r_sv2.bold = True
    r_sv2.font.size = Pt(13)

    doc.add_paragraph("\n\n")
    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.add_run("TP. HỒ CHÍ MINH, NĂM 2026").bold = True

    # ================= 2. TRANG PHỤ BÌA (COVER 2) =================
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("TỔNG LIÊN ĐOÀN LAO ĐỘNG VIỆT NAM\nTRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG\nKHOA CÔNG NGHỆ THÔNG TIN")
    r.bold = True
    r.font.size = Pt(13)

    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(16)
        p_logo.paragraph_format.space_after = Pt(16)
        p_logo.add_run().add_picture(logo_path, width=Inches(2.0))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BÁO CÁO CUỐI KỲ\n")
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("MÔN HỌC: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING)\n\n")
    r_sub.bold = True
    r_sub.font.size = Pt(13)

    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_topic.add_run("ĐỀ TÀI:\nTHIẾT KẾ VÀ XÂY DỰNG MÔ PHỎNG HỆ THỐNG ĐÁM MÂY THU NHỎ\n(MyMiniCloud Platform trên Docker & AWS EC2)\n\n")
    r_t1.bold = True
    r_t1.font.size = Pt(14)
    r_t1.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    p_gv = doc.add_paragraph()
    p_gv.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gv.paragraph_format.space_before = Pt(20)
    p_gv.add_run("Giảng viên hướng dẫn:\n").font.size = Pt(13)
    r_gv = p_gv.add_run("TS. Bùi Quy Anh\n\n")
    r_gv.bold = True
    r_gv.font.size = Pt(14)

    p_sv = doc.add_paragraph()
    p_sv.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sv_title = p_sv.add_run("Sinh viên thực hiện:\n")
    r_sv_title.bold = True
    r_sv_title.font.size = Pt(13)
    r_sv1 = p_sv.add_run("1. Võ Huỳnh Minh Đức – MSSV: 523H0014\n")
    r_sv1.bold = True
    r_sv1.font.size = Pt(13)
    r_sv2 = p_sv.add_run("2. Võ Anh Kiệt – MSSV: 523H0048\n")
    r_sv2.bold = True
    r_sv2.font.size = Pt(13)

    doc.add_paragraph("\n")
    p_loc = doc.add_paragraph()
    p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.add_run("TP. HỒ CHÍ MINH, NĂM 2026").bold = True

    # ================= 3. LỜI CẢM ƠN =================
    doc.add_page_break()
    h_cm = doc.add_paragraph()
    h_cm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h_cm.paragraph_format.space_before = Pt(12)
    h_cm.paragraph_format.space_after = Pt(16)
    r = h_cm.add_run("LỜI CẢM ƠN")
    r.bold = True
    r.font.size = Pt(16)

    add_body_p(doc, "Trước hết, nhóm chúng em xin được bày tỏ lòng biết ơn sâu sắc và chân thành nhất đến Thầy TS. Bùi Quy Anh – Giảng viên phụ trách học phần Điện toán đám mây (Cloud Computing). Trong suốt học kỳ vừa qua, Thầy đã tận tình truyền đạt những kiến thức chuyên môn cốt lõi, sâu sắc và mang tính cập nhật cao về công nghệ ảo hóa, kiến trúc microservices, mạng ảo hóa và các giải pháp triển khai đám mây hiện đại.")
    add_body_p(doc, "Những bài giảng nhiệt huyết, sự hướng dẫn tận tâm và những yêu cầu kiểm thử thực tiễn từ Thầy đã giúp chúng em không chỉ nắm vững lý thuyết mà còn làm chủ được quy trình triển khai một hệ sinh thái Cloud hoàn chỉnh trên nền tảng Docker và máy ảo AWS EC2 thực tế.")
    add_body_p(doc, "Mặc dù nhóm đã nỗ lực hết mình để hiện thực hóa toàn bộ các khối chức năng và hoàn thiện bản báo cáo này một cách khoa học nhất, song do sự phức tạp của hạ tầng đa dịch vụ nên bài làm khó tránh khỏi những thiếu sót nhất định. Nhóm rất mong nhận được những nhận xét, góp ý quý báu của Thầy để chúng em tiếp tục hoàn thiện kiến thức và kỹ năng thực tế trong tương lai.")

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(20)
    p_sign.add_run("TP. Hồ Chí Minh, ngày 12 tháng 11 năm 2026\n").font.size = Pt(12)
    r_grp = p_sign.add_run("Tập thể sinh viên thực hiện\n")
    r_grp.bold = True
    p_sign.add_run("(Ký và ghi rõ họ tên)\n\n\n")
    r_names = p_sign.add_run("Võ Huỳnh Minh Đức          Võ Anh Kiệt")
    r_names.bold = True

    # ================= 4. LỜI CAM ĐOAN =================
    doc.add_page_break()
    h_cd = doc.add_paragraph()
    h_cd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h_cd.paragraph_format.space_before = Pt(12)
    h_cd.paragraph_format.space_after = Pt(16)
    r = h_cd.add_run("LỜI CAM ĐOAN")
    r.bold = True
    r.font.size = Pt(16)

    add_body_p(doc, "Nhóm chúng em xin cam đoan rằng toàn bộ nội dung trong bản báo cáo cuối kỳ này là công trình nghiên cứu và triển khai thực tế do chính các thành viên trong nhóm thực hiện dưới sự giảng dạy và hướng dẫn của Thầy TS. Bùi Quy Anh.")
    add_body_p(doc, "Tất cả các kết quả thực nghiệm, dữ liệu cấu hình, mã nguồn Dockerfile, Docker Compose, cũng như toàn bộ hình ảnh minh chứng kiểm thử được trình bày trong báo cáo đều được chụp trực tiếp từ hệ thống đang vận hành thực tế trên môi trường máy ảo AWS EC2 (Public IP: 44.206.252.67), không sao chép hay giả mạo dưới bất kỳ hình thức nào.")
    add_body_p(doc, "Nhóm xin hoàn toàn chịu trách nhiệm trước Bộ môn và Khoa Công nghệ Thông tin – Trường Đại học Tôn Đức Thắng về tính trung thực của công trình này.")

    p_sign2 = doc.add_paragraph()
    p_sign2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign2.paragraph_format.space_before = Pt(20)
    p_sign2.add_run("TP. Hồ Chí Minh, ngày 12 tháng 11 năm 2026\n").font.size = Pt(12)
    r_grp = p_sign2.add_run("Xác nhận của các thành viên\n")
    r_grp.bold = True
    p_sign2.add_run("(Ký và ghi rõ họ tên)\n\n\n")
    r_names = p_sign2.add_run("Võ Huỳnh Minh Đức          Võ Anh Kiệt")
    r_names.bold = True

    # ================= 5. TÓM TẮT ĐỀ TÀI =================
    doc.add_page_break()
    h_tt = doc.add_paragraph()
    h_tt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h_tt.paragraph_format.space_before = Pt(12)
    h_tt.paragraph_format.space_after = Pt(16)
    r = h_tt.add_run("TÓM TẮT ĐỀ TÀI")
    r.bold = True
    r.font.size = Pt(16)

    add_body_p(doc, "Báo cáo cuối kỳ này trình bày toàn diện quá trình nghiên cứu, thiết kế, triển khai và kiểm thử thực tế đề tài: 'Xây dựng mô phỏng hệ thống MiniCloud cơ bản (MyMiniCloud)'. Mục tiêu trọng tâm là mô phỏng một hệ sinh thái điện toán đám mây thu nhỏ tương tự kiến trúc của các nhà cung cấp dịch vụ Cloud hàng đầu thế giới (như AWS, Google Cloud, Azure).")
    add_body_p(doc, "Hệ thống bao gồm đầy đủ 9 khối dịch vụ cốt lõi hoạt động độc lập trong 11 container trên dải mạng ảo hóa cầu nối biệt lập 'cloud-net' (Subnet: 10.10.10.0/24): Cụm Web Frontend Server (Nginx) phục vụ nội dung tĩnh và blog kỹ thuật; Application Backend Server (Node.js Express) cung cấp RESTful API; Relational Database Server (MySQL 8) lưu trữ dữ liệu quan hệ; Authentication Identity Server (Keycloak 24) quản lý danh tính OIDC/SSO; Object Storage Server (MinIO) lưu trữ dữ liệu phi cấu trúc chuẩn S3; Internal DNS Server (Bind9) phân giải tên miền vùng nội bộ cloud.local; Cụm giám sát hiệu năng thời gian thực (Prometheus & Node Exporter); Visualization Server (Grafana) biểu diễn trực quan các đồ thị chỉ số; và API Gateway / Reverse Proxy (Nginx) điều phối lưu lượng mạng từ Internet, hỗ trợ cân bằng tải Round Robin.")
    add_body_p(doc, "Hệ thống được đóng gói tự động hóa, phát hành các custom container image lên Docker Hub công cộng, và triển khai thành công 100% trên nền tảng Public Cloud thực tế của máy ảo AWS EC2 (Ubuntu 24.04 LTS, Public IPv4: 44.206.252.67). Toàn bộ 10 nhiệm vụ mở rộng chuyên sâu đều được kiểm thử và đáp ứng trọn vẹn.")
    add_body_p(doc, "Từ khóa: Điện toán đám mây (Cloud Computing), Docker, Docker Compose, Microservices, API Gateway, Round Robin Load Balancing, OpenID Connect (OIDC), Keycloak, MinIO S3 Object Storage, Bind9 DNS, Prometheus, Grafana, AWS EC2.", bold_prefix="Từ khóa chính: ")

    # ================= 6. BẢNG PHÂN CÔNG NHIỆM VỤ =================
    doc.add_page_break()
    add_heading_1(doc, "BẢNG PHÂN CÔNG NHIỆM VỤ VÀ TỶ LỆ ĐÓNG GÓP")
    
    t_pc = doc.add_table(rows=1, cols=4)
    t_pc.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thành viên", "Vai trò đảm nhiệm", "Nhiệm vụ kỹ thuật cụ thể", "Đóng góp"]
    for i, h in enumerate(headers):
        cell = t_pc.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "002060")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tasks_data = [
        (
            "Võ Huỳnh Minh Đức\nMSSV: 523H0014",
            "DevOps & Infrastructure Lead",
            "- Thiết kế toàn bộ kiến trúc Docker Compose 11 containers, dải mạng cloud-net (10.10.10.0/24).\n"
            "- Cấu hình Nginx API Gateway, định tuyến và cân bằng tải Round Robin (Task 9, 10).\n"
            "- Thiết kế máy chủ DNS nội bộ Bind9 và zone cloud.local (Task 6).\n"
            "- Cấu hình giám sát Prometheus (scrape web) & Grafana PromQL (Task 7, 8).\n"
            "- Viết script tự động hóa Keycloak (kcadm) & kết nối MySQL Backend.\n"
            "- Đóng gói & Push Docker Images lên Docker Hub (minhduc14022005).\n"
            "- Triển khai toàn diện hạ tầng lên máy ảo AWS EC2 Public IP thực tế (44.206.252.67).",
            "50%"
        ),
        (
            "Võ Anh Kiệt\nMSSV: 523H0048",
            "Application & Documentation Lead",
            "- Thiết kế giao diện Web Frontend, trang chủ phong cách rack-server sinh động.\n"
            "- Viết 3 bài Blog kỹ thuật công nghệ điện toán đám mây & sơ đồ SVG (Task 1).\n"
            "- Thiết kế cấu trúc dữ liệu JSON students.json và API /student (Task 2).\n"
            "- Thiết kế CSDL MySQL studentdb và bảng dữ liệu sinh viên (Task 3).\n"
            "- Cấu hình kiểm thử Keycloak Admin UI: tạo Realm, Client, User (Task 4).\n"
            "- Cấu hình MinIO Object Storage UI: tạo Buckets, upload avatar, PDF (Task 5).\n"
            "- Soạn thảo báo cáo đồ án Word chuẩn mẫu, tổng hợp minh chứng thực tế trên EC2.",
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
            set_cell_margins(cell, 100, 100, 120, 120)

    # ================= 7. CHƯƠNG 1 =================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 1. GIỚI THIỆU TỔNG QUAN VÀ MỤC TIÊU ĐỀ TÀI")

    add_heading_2(doc, "1.1 Bối cảnh và Tính cấp thiết của Đề tài")
    add_body_p(doc, "Trong thời đại chuyển đổi số mạnh mẽ, Điện toán đám mây (Cloud Computing) đã trở thành hạ tầng xương sống cho hầu hết các tổ chức và doanh nghiệp công nghệ trên thế giới. Việc tiếp cận và làm chủ các mô hình đám mây lớn (như Amazon Web Services, Google Cloud Platform, Microsoft Azure) đòi hỏi sinh viên phải nắm vững bản chất kiến trúc của các thành phần hạ tầng: máy chủ web, xử lý ứng dụng microservices, cơ sở dữ liệu quan hệ, quản lý định danh và bảo mật tập trung, lưu trữ đối tượng phi cấu trúc, phân giải tên miền nội bộ và hệ thống giám sát phân tán.")
    add_body_p(doc, "Đề tài 'Xây dựng mô phỏng hệ thống MiniCloud cơ bản (MyMiniCloud)' được hình thành nhằm mang lại cho sinh viên trải nghiệm thực hành thực tế và trực quan nhất. Thông qua việc đóng gói các thành phần độc lập trong các container Docker, kết nối chúng qua một mạng ảo hóa biệt lập và triển khai trực tiếp lên môi trường Public Cloud AWS EC2, sinh viên có thể giải quyết các bài toán kỹ thuật phức tạp như cân bằng tải lưu lượng, xác thực phân quyền dựa trên chuẩn mở OIDC, định danh dịch vụ và phân tích hiệu năng hệ thống theo thời gian thực.")

    add_heading_2(doc, "1.2 Mục tiêu Đề tài")
    add_bullet_item(doc, "Làm chủ công nghệ ảo hóa Container", "Sử dụng Docker để đóng gói các môi trường máy chủ độc lập và Docker Compose để điều phối, quản lý vòng đời của cụm 11 containers.")
    add_bullet_item(doc, "Hiện thực hóa 9 khối dịch vụ đám mây tiêu chuẩn", "Triển khai đầy đủ các khối chức năng tương ứng với các dịch vụ của AWS: Web Hosting (S3/EC2), Application API (ECS/Lambda), RDS MySQL, IAM/Cognito (Keycloak), Object Storage (S3/MinIO), Route 53 (Bind9 DNS), CloudWatch (Prometheus & Grafana) và Application Load Balancer (Nginx API Gateway).")
    add_bullet_item(doc, "Hoàn thành 100% yêu cầu cơ bản (5.0 điểm)", "Đảm bảo tính thông suốt của mạng ảo hóa nội bộ (ping connectivity) và tính sẵn sàng của toàn bộ 11 container.")
    add_bullet_item(doc, "Chinh phục toàn diện 10 nhiệm vụ mở rộng chuyên sâu (5.0 điểm)", "Tích hợp cân bằng tải Round Robin, xác thực phân quyền qua Access Token OIDC, lưu trữ bucket MinIO, phân giải tên miền Bind9, và hệ thống đo lường PromQL thời gian thực.")
    add_bullet_item(doc, "Triển khai thực tế trên Public Cloud", "Đóng gói image đẩy lên Docker Hub và vận hành toàn diện trên máy ảo AWS EC2 Ubuntu với Public IP thực tế.")

    add_heading_2(doc, "1.3 Kiến trúc 9 Loại Máy chủ trong Hệ sinh thái MyMiniCloud")
    
    t_srv = doc.add_table(rows=1, cols=4)
    t_srv.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["STT", "Khối Dịch vụ", "Công nghệ / Container Image", "Vai trò và Chức năng Chính"]
    for i, h in enumerate(s_headers):
        cell = t_srv.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "002060")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    servers_info = [
        ("1", "Web Server Cluster", "nginx:stable-alpine (2 instances)", "Phục vụ giao diện web tĩnh, 3 bài viết blog kỹ thuật; chịu tải luân phiên."),
        ("2", "Application Server", "Node.js 20 Express (Custom build)", "Xử lý logic nghiệp vụ, cung cấp RESTful API (/student, /secure, /students-db)."),
        ("3", "Database Server", "MySQL 8.0 Community", "Lưu trữ dữ liệu quan hệ, quản lý schema minicloud và studentdb."),
        ("4", "Authentication Server", "Keycloak 24.0.5 (OIDC/SSO)", "Quản lý danh tính tập trung, cấp phát JWT token bảo vệ tài nguyên API."),
        ("5", "Object Storage Server", "MinIO Community (S3-compatible)", "Lưu trữ dữ liệu phi cấu trúc, quản lý buckets profile-pics và documents."),
        ("6", "Internal DNS Server", "Bind9 9.18 (Zone cloud.local)", "Dịch vụ định danh nội bộ, phân giải IP các dịch vụ theo tên miền .cloud.local."),
        ("7", "Monitoring Server", "Prometheus v2.45 + Node Exporter", "Thu thập chỉ số CPU, RAM, Disk, Network và giám sát trạng thái Web Server."),
        ("8", "Visualization Server", "Grafana OSS v10.0", "Trực quan hóa đồ thị giám sát thời gian thực, cảnh báo hiệu năng."),
        ("9", "Reverse Proxy / Gateway", "Nginx API Gateway", "Cổng giao tiếp duy nhất đón traffic từ Internet, cân bằng tải Round Robin.")
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
            set_cell_margins(cell, 80, 80, 100, 100)

    # ================= 8. CHƯƠNG 2 =================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 2. KIẾN TRÚC HỆ THỐNG VÀ SƠ ĐỒ MẠNG")

    add_heading_2(doc, "2.1 Thiết kế Mô hình Mạng Nội bộ (cloud-net)")
    add_body_p(doc, "Hệ thống MyMiniCloud sử dụng mô hình mạng ảo hóa cầu nối (Docker Bridge Network) mang tên 'cloud-net' với subnet cấu hình 10.10.10.0/24. Cơ chế này đem lại các lợi ích kiến trúc then chốt:")
    add_bullet_item(doc, "Tính cô lập bảo mật cao (Isolation)", "Các dịch vụ nhạy cảm như MySQL Database (Port 3306) không cần mở cổng công khai ra ngoài Internet mà chỉ có thể được kết nối bởi các container cùng nằm trong mạng nội bộ cloud-net.")
    add_bullet_item(doc, "Phân giải dịch vụ nội bộ (Service Discovery)", "Docker Embedded DNS kết hợp với Internal DNS Bind9 cho phép các dịch vụ gọi nhau thông qua tên container hoặc tên miền chuẩn (như web-frontend-server.cloud.local).")
    add_bullet_item(doc, "Cổng vào duy nhất (Single Point of Entry)", "Toàn bộ lưu lượng truy cập từ người dùng Internet chỉ được phép đi qua API Gateway (Port 80) để kiểm soát, định tuyến và phân phối tải.")

    add_heading_2(doc, "2.2 Bảng Phân bổ Địa chỉ IP và Cổng Dịch vụ (Port Mapping)")
    
    t_ip = doc.add_table(rows=1, cols=4)
    t_ip.alignment = WD_TABLE_ALIGNMENT.CENTER
    ip_headers = ["Tên Container", "Địa chỉ IP (cloud-net)", "Port Nội bộ", "Port Ánh xạ Host / EC2"]
    for i, h in enumerate(ip_headers):
        cell = t_ip.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "002060")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    ip_data = [
        ("api-gateway-proxy-server", "10.10.10.2", "80/TCP", "80 (Public HTTP Gateway)"),
        ("web-frontend-server", "10.10.10.10", "80/TCP", "8080 (Direct Web 1)"),
        ("web-frontend-server2", "10.10.10.11", "80/TCP", "8082 (Direct Web 2)"),
        ("application-backend-server", "10.10.10.20", "8081/TCP", "8085 (Backend Direct)"),
        ("relational-database-server", "10.10.10.30", "3306/TCP", "3306 (MySQL Community)"),
        ("authentication-identity-server", "10.10.10.40", "8080/TCP", "8081 (Keycloak Admin UI)"),
        ("object-storage-server", "10.10.10.50", "9000, 9001", "9000 (API), 9001 (Console)"),
        ("internal-dns-server", "10.10.10.60", "53/UDP, 53/TCP", "1053/UDP (Bind9 DNS)"),
        ("monitoring-prometheus-server", "10.10.10.70", "9090/TCP", "9090 (Prometheus Web UI)"),
        ("monitoring-node-exporter-server", "10.10.10.71", "9100/TCP", "9100 (Metrics Endpoint)"),
        ("monitoring-grafana-dashboard-server", "10.10.10.80", "3000/TCP", "3000 (Grafana Dashboard)")
    ]

    for c_name, c_ip, c_iport, c_eport in ip_data:
        row = t_ip.add_row()
        row.cells[0].text = c_name
        row.cells[1].text = c_ip
        row.cells[2].text = c_iport
        row.cells[3].text = c_eport

    for row in t_ip.rows:
        for cell in row.cells:
            set_cell_margins(cell, 70, 70, 90, 90)

    add_heading_2(doc, "2.3 Luồng Xử lý Dữ liệu Tổng thể (Request Flow)")
    add_bullet_item(doc, "1. Luồng Người dùng truy cập Web & Cân bằng tải", "Client gửi HTTP request đến Cổng 80 của máy ảo AWS EC2 -> Nginx API Gateway tiếp nhận và áp dụng giải thuật Round Robin chuyển tiếp luân phiên 50/50 sang web-frontend-server (10.10.10.10) hoặc web-frontend-server2 (10.10.10.11).")
    add_bullet_item(doc, "2. Luồng Gọi API Backend & Cơ sở dữ liệu", "Khi Client truy cập '/student/' hoặc '/api/students-db', Gateway định tuyến trực tiếp vào application-backend-server (Port 8081). Backend đọc dữ liệu từ file JSON hoặc thiết lập kết nối có xác thực sang relational-database-server (MySQL Port 3306) để trả về phản hồi chuẩn JSON.")
    add_bullet_item(doc, "3. Luồng Xác thực và Phân quyền OIDC", "Client đăng nhập vào Keycloak nhận JWT Access Token. Khi gọi endpoint bảo mật '/secure', Backend sử dụng khóa công khai JWKS từ Keycloak để xác minh chữ ký số bất đối xứng (RS256).")
    add_bullet_item(doc, "4. Luồng Giám sát Chỉ số Hạ tầng", "Prometheus định kỳ gửi HTTP request đến Node Exporter (port 9100) và Web Server (port 80) để thu thập chỉ số CPU, RAM, Disk và Network. Grafana kết nối vào Prometheus qua API để vẽ biểu đồ trực quan.")

    # ================= 9. CHƯƠNG 3 =================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 3. THIẾT KẾ VÀ CẤU HÌNH CHI TIẾT CÁC THÀNH PHẦN")

    add_heading_2(doc, "3.1 Cấu hình Điều phối Toàn cục (docker-compose.yml)")
    add_body_p(doc, "Tập tin 'docker-compose.yml' đóng vai trò trung tâm chỉ huy, định nghĩa 11 dịch vụ, thiết lập các biến môi trường, cơ chế khởi động phụ thuộc (depends_on) và chính sách tự phục hồi khi có sự cố (restart: unless-stopped). Hệ thống sử dụng các Named Volumes chuyên biệt (keycloak-data, grafana-data) để đảm bảo tính toàn vẹn dữ liệu ngay cả khi container bị khởi động lại.")

    add_heading_2(doc, "3.2 Cấu hình Cân bằng tải Round Robin và API Gateway")
    add_body_p(doc, "Trong tệp cấu hình 'api-gateway-proxy-server/nginx.conf', nhóm khai báo một cụm upstream mang tên 'web_cluster' với thuật toán Round Robin mặc định, đồng thời cấu hình các location block chuyển tiếp:")
    add_bullet_item(doc, "location /", "Chuyển tiếp đến upstream web_cluster (chứa Web 1 và Web 2).")
    add_bullet_item(doc, "location /student/", "Chuyển tiếp đến application-backend-server:8081/student (Nhiệm vụ 9).")
    add_bullet_item(doc, "location /api/", "Chuyển tiếp đến application-backend-server:8081/api/.")
    add_bullet_item(doc, "location /auth/", "Chuyển tiếp đến authentication-identity-server:8080/.")

    add_heading_2(doc, "3.3 Tối ưu hóa Build Image Backend với Mirror Registry")
    add_body_p(doc, "Trong quá trình xây dựng Node.js Express trên môi trường máy ảo quốc tế, việc tải các gói thư viện npm (như express, mysql2, jsonwebtoken, jwks-rsa) thường gặp hiện tượng timeout (ETIMEDOUT). Nhóm đã giải quyết xuất sắc bằng cách cấu hình mirror registry (https://registry.npmmirror.com) trực tiếp trong Dockerfile, giúp rút ngắn thời gian build từ 400 giây lỗi xuống còn vỏn vẹn 9 giây thành công 100%.")

    add_heading_2(doc, "3.4 Cấu hình Vùng Tên miền Nội bộ Bind9 (Zone cloud.local)")
    add_body_p(doc, "Tập tin 'internal-dns-server/db.cloud.local' khai báo các bản ghi loại A (Address Record) phân giải chuẩn xác các tên miền nội bộ: web-frontend-server.cloud.local -> 10.10.10.10, app-backend.cloud.local -> 10.10.10.20, minio.cloud.local -> 10.10.10.50, và keycloak.cloud.local -> 10.10.10.40.")

    add_heading_2(doc, "3.5 Cấu hình Thu thập Chỉ số Prometheus và Grafana")
    add_body_p(doc, "File 'monitoring-prometheus-server/prometheus.yml' cấu hình 2 job thu thập chỉ số: job 'node' đo tài nguyên phần cứng từ Node Exporter và job 'web' giám sát trực tiếp web-frontend-server:80. Phía Nginx được bổ sung location '/metrics' trả về định dạng text/plain gauge chuẩn Prometheus, giúp target 'web' đạt trạng thái UP 100%.")

    # ================= 10. CHƯƠNG 4 =================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 4. KẾT QUẢ THỰC NGHIỆM VÀ MINH CHỨNG KIỂM THỬ")

    add_body_p(doc, "Toàn bộ hệ thống MyMiniCloud đã được đóng gói và triển khai thành công 100% trên nền tảng Public Cloud AWS EC2 (Region: us-east-1 N. Virginia). Dưới đây là các thông số vận hành thực tế của máy ảo:")
    add_bullet_item(doc, "Instance ID", "i-008fc89eb3cb7caa8 (Tên máy ảo: MyMiniCloud-EC2)")
    add_bullet_item(doc, "Địa chỉ Public IPv4", "44.206.252.67 (Truy cập trực tiếp qua mạng Internet)")
    add_bullet_item(doc, "Cấu hình Máy ảo", "AWS t2.micro (1 vCPU, 1GB RAM) kết hợp 2GB Swap Memory (/swapfile)")
    add_bullet_item(doc, "Hệ điều hành", "Ubuntu 24.04 LTS (GNU/Linux 7.0.0-1014-aws x86_64)")
    add_bullet_item(doc, "Trạng thái", "Toàn bộ 11/11 container đều đang hoạt động 'Up (healthy)'")

    add_heading_2(doc, "4.1 Minh chứng Phần Căn bản: Máy ảo EC2 và Hạ tầng 11 Container")
    
    # Img 1: AWS Console
    p1 = os.path.join(ss_ec2_dir, "image copy 10.png")
    if os.path.exists(p1):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p1, width=Inches(5.8))
        add_caption(doc, "Hình 4.1: Máy ảo MyMiniCloud-EC2 trạng thái Running trên AWS Management Console (IP: 44.206.252.67)")

    # Img 2: Docker compose ps
    p2 = os.path.join(ss_ec2_dir, "image copy 9.png")
    if os.path.exists(p2):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p2, width=Inches(5.8))
        add_caption(doc, "Hình 4.2: Terminal EC2 hiển thị toàn bộ 11 container đang vận hành đồng bộ (Up) qua lệnh docker compose ps")

    add_heading_2(doc, "4.2 Minh chứng Mở rộng 10: Cân bằng tải Round Robin giữa Web 1 và Web 2")
    add_body_p(doc, "Khi người dùng truy cập vào địa chỉ 'http://44.206.252.67/' qua Cổng 80 của API Gateway, mỗi lần tải lại trang (F5), Nginx sẽ luân phiên phân phối yêu cầu sang Web Server 1 và Web Server 2.")

    # Img 3: Web 1
    p3 = os.path.join(ss_ec2_dir, "Screenshot 2026-11-11 150039.png")
    if os.path.exists(p3):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p3, width=Inches(5.8))
        add_caption(doc, "Hình 4.3: Nginx Gateway tiếp nhận và chuyển tiếp yêu cầu đến Máy chủ Web 1 (đèn xanh web-1 bật sáng)")

    # Img 4: Web 2
    p4 = os.path.join(ss_ec2_dir, "Screenshot 2026-11-11 150049.png")
    if os.path.exists(p4):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p4, width=Inches(5.8))
        add_caption(doc, "Hình 4.4: Thuật toán Round Robin tự động chuyển tiếp yêu cầu tiếp theo đến Máy chủ Web 2 (đèn xanh web-2 bật sáng)")

    add_heading_2(doc, "4.3 Minh chứng Mở rộng 1: Giao diện Web Frontend và 3 Bài viết Blog Kỹ thuật")
    
    # Img 5: Blog index
    p5 = os.path.join(ss_ec2_dir, "image.png")
    if os.path.exists(p5):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p5, width=Inches(5.8))
        add_caption(doc, "Hình 4.5: Trang danh mục Blog kỹ thuật (/blog/) hiển thị danh sách 3 bài viết chuyên sâu")

    # Img 6: Blog 1 detail
    p6 = os.path.join(ss_ec2_dir, "image copy 8.png")
    if os.path.exists(p6):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p6, width=Inches(5.8))
        add_caption(doc, "Hình 4.6: Nội dung chi tiết Bài viết 1 kèm sơ đồ kiến trúc đám mây định dạng vector SVG (/blog/blog1.html)")

    add_heading_2(doc, "4.4 Minh chứng Mở rộng 2, 3 và 9: Backend API và Kết nối CSDL MySQL")
    add_body_p(doc, "Các API được tích hợp định tuyến thông minh qua Gateway Cổng 80, cho phép gọi dữ liệu danh sách sinh viên trực tiếp từ JSON và truy vấn trực tiếp từ bảng students trong CSDL studentdb.")

    # Img 7: API student JSON
    p7 = os.path.join(ss_ec2_dir, "image copy.png")
    if os.path.exists(p7):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p7, width=Inches(5.8))
        add_caption(doc, "Hình 4.7: API /student/ trả về danh sách 5 sinh viên định dạng chuẩn JSON từ Backend (Task 2 & 9)")

    # Img 8: API MySQL
    p8 = os.path.join(ss_ec2_dir, "image copy 2.png")
    if os.path.exists(p8):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p8, width=Inches(5.8))
        add_caption(doc, "Hình 4.8: API /api/students-db kết nối bảo mật tới MySQL Server và truy vấn dữ liệu sinh viên trong CSDL studentdb (Task 3)")

    add_heading_2(doc, "4.5 Minh chứng Mở rộng 4: Máy chủ Xác thực Tập trung Keycloak (OIDC/SSO)")
    
    # Img 9: Keycloak Clients
    p9 = os.path.join(ss_ec2_dir, "image copy 3.png")
    if os.path.exists(p9):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p9, width=Inches(5.8))
        add_caption(doc, "Hình 4.9: Giao diện Keycloak Admin Console tại cổng 8081 cấu hình Client flask-app chuẩn OpenID Connect (Task 4)")

    add_heading_2(doc, "4.6 Minh chứng Mở rộng 5: Lưu trữ Đối tượng MinIO S3 Object Storage")
    add_body_p(doc, "Dịch vụ MinIO được cấu hình đầy đủ 2 bucket: 'profile-pics' dùng để lưu trữ ảnh đại diện cá nhân và 'documents' dùng để lưu trữ tệp tài liệu báo cáo PDF.")

    # Img 10: Minio profile-pics
    p10 = os.path.join(ss_ec2_dir, "image copy 5.png")
    if os.path.exists(p10):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p10, width=Inches(5.8))
        add_caption(doc, "Hình 4.10: Bucket 'profile-pics' trên MinIO Console (Port 9001) lưu trữ ảnh đại diện người dùng")

    # Img 11: Minio documents
    p11 = os.path.join(ss_ec2_dir, "image copy 4.png")
    if os.path.exists(p11):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p11, width=Inches(5.8))
        add_caption(doc, "Hình 4.11: Bucket 'documents' trên MinIO Console lưu trữ tệp tài liệu báo cáo đồ án định dạng PDF")

    add_heading_2(doc, "4.7 Minh chứng Mở rộng 6: Phân giải Tên miền Nội bộ DNS Bind9")
    add_body_p(doc, "Sử dụng lệnh 'dig' trên terminal máy ảo EC2 để kiểm tra khả năng phân giải tên miền vùng cloud.local của máy chủ Bind9:")

    # Img 12: DNS dig
    p12 = os.path.join(ss_ec2_dir, "image copy 12.png")
    if os.path.exists(p12):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p12, width=Inches(5.8))
        add_caption(doc, "Hình 4.12: Lệnh dig kiểm tra phân giải tên miền thành công trả về 4 địa chỉ IP nội bộ: 10.10.10.10, 10.10.10.20, 10.10.10.50, 10.10.10.40 (Task 6)")

    add_heading_2(doc, "4.8 Minh chứng Mở rộng 7 và 8: Hệ thống Giám sát Toàn diện Prometheus & Grafana")
    add_body_p(doc, "Hệ thống giám sát vận hành ổn định theo thời gian thực, đo lường toàn diện các thông số phần cứng của máy chủ EC2 và trạng thái sẵn sàng của Web Server:")

    # Img 13: Prometheus targets
    p13 = os.path.join(ss_ec2_dir, "image copy 11.png")
    if os.path.exists(p13):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p13, width=Inches(5.8))
        add_caption(doc, "Hình 4.13: Bảng điều khiển Prometheus Targets (Port 9090) hiển thị trạng thái cả 2 mục 'node' và 'web' đều là UP (1/1 up) (Task 7)")

    # Img 14: Grafana dashboard
    p14 = os.path.join(ss_ec2_dir, "image copy 6.png")
    if os.path.exists(p14):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(p14, width=Inches(5.8))
        add_caption(doc, "Hình 4.14: Bảng điều khiển Grafana Dashboard (Port 3000) với 3 đồ thị sóng dữ liệu CPU Usage, RAM Usage và Network Traffic thời gian thực (Task 8)")

    # ================= 11. CHƯƠNG 5 =================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 5. ĐÁNH GIÁ, KHÓ KHĂN VÀ HƯỚNG PHÁT TRIỂN")

    add_heading_2(doc, "5.1 Đánh giá Ưu điểm Nổi bật của Hệ thống")
    add_bullet_item(doc, "Tính hoàn thiện và bám sát thực tế", "Hệ thống MyMiniCloud mô phỏng chính xác và đầy đủ các thành phần hạ tầng tương tự một Public Cloud thực thụ, từ lưu trữ, định tuyến, cân bằng tải, cơ sở dữ liệu cho đến quản lý định danh và giám sát.")
    add_bullet_item(doc, "Khả năng co giãn và chịu tải (Scalability)", "Kiến trúc Nginx Gateway kết hợp giải thuật Round Robin cho phép hệ thống mở rộng quy mô dễ dàng bằng cách bổ sung thêm nhiều Web Server instance mà không làm gián đoạn dịch vụ.")
    add_bullet_item(doc, "Mức độ tự động hóa cao (Automation)", "Cung cấp đầy đủ các kịch bản tự động hóa từ khởi tạo môi trường, thiết lập Keycloak bằng kcadm, nạp dashboard Grafana qua REST API, đến script deploy một chạm trên AWS EC2.")
    add_bullet_item(doc, "Tính bền vững của dữ liệu (Data Persistence)", "Sử dụng các Named Volumes đảm bảo dữ liệu của MySQL, MinIO và cấu hình Keycloak không bị mất đi khi khởi động lại máy ảo.")

    add_heading_2(doc, "5.2 Các Khó khăn Kỹ thuật Gặp phải và Giải pháp Khắc phục")
    add_bullet_item(doc, "1. Hiện tượng nghẽn mạng tải npm package trên máy ảo", "Khi build image Node.js Express, máy ảo thường bị lỗi ETIMEDOUT. Nhóm đã giải quyết triệt để bằng cách áp dụng mirror registry (npmmirror.com) với timeout kéo dài trong Dockerfile.")
    add_bullet_item(doc, "2. Giới hạn tài nguyên phần cứng máy ảo AWS t2.micro (1GB RAM)", "Chạy đồng thời 11 container khiến máy ảo có nguy cơ tràn RAM (Out of Memory). Nhóm đã khắc phục thành công bằng cách cấu hình phân vùng bộ nhớ ảo 2GB Swap Memory (/swapfile), giúp hệ thống vận hành cực kỳ mượt mà và ổn định.")
    add_bullet_item(doc, "3. Cơ chế bắt buộc HTTPS của Keycloak trên IP Public", "Keycloak mặc định chặn đăng nhập qua IP Public nếu không có SSL. Nhóm đã sử dụng kcadm.sh thiết lập tham số 'sslRequired=NONE' cho Realm master và realm_VoAnhKiet để cho phép đăng nhập qua HTTP.")
    add_bullet_item(doc, "4. Lỗi định dạng Content-Type khi Prometheus scrape Web", "Prometheus yêu cầu định dạng text/plain trong khi Nginx trả về text/html. Nhóm đã bổ sung location /metrics chuyên biệt trong Nginx trả về gauge metric chuẩn, đưa target lên trạng thái UP.")

    add_heading_2(doc, "5.3 Hướng Phát triển và Mở rộng trong Tương lai")
    add_bullet_item(doc, "Chuyển đổi sang Kubernetes (K8s)", "Chuyển đổi các cấu hình Docker Compose sang Kubernetes Manifests (Deployments, Services, Ingress, PersistentVolumeClaims) và tích hợp cơ chế tự động co giãn tài nguyên Horizontal Pod Autoscaler (HPA).")
    add_bullet_item(doc, "Tích hợp quy trình CI/CD tự động", "Xây dựng pipeline GitHub Actions tự động kiểm thử đơn vị (Unit Test), quét lỗ hổng bảo mật (Trivy), tự động build và push container image lên Docker Hub khi có commit mới.")
    add_bullet_item(doc, "Mã hóa bảo mật toàn diện với HTTPS/TLS", "Cài đặt chứng chỉ số SSL/TLS miễn phí từ Let's Encrypt kết hợp Certbot trên API Gateway để mã hóa toàn bộ dữ liệu truyền thông giữa Client và Cloud.")

    # ================= 12. PHỤ LỤC & TỰ ĐÁNH GIÁ =================
    doc.add_page_break()
    add_heading_1(doc, "PHỤ LỤC. BẢNG TỰ ĐÁNH GIÁ KẾT QUẢ VÀ LIÊN KẾT NỘP BÀI")

    add_heading_2(doc, "Bảng Tự Đánh giá 10 Nhiệm vụ Mở rộng (5.0 / 5.0 Điểm Nâng cao)")
    
    t_eval = doc.add_table(rows=1, cols=5)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    e_headers = ["STT", "Nhiệm vụ Mở rộng", "Yêu cầu Chi tiết của Đề tài", "Kết quả Đạt được", "Điểm Tự chấm"]
    for i, h in enumerate(e_headers):
        cell = t_eval.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_background(cell, "002060")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    eval_data = [
        ("1", "Web Frontend", "Blog cá nhân 3 bài viết kỹ thuật kèm ảnh minh họa và hyperlink", "Hoàn thành 100% (Hình 4.5, 4.6)", "0.5 / 0.5"),
        ("2", "Backend API", "Endpoint /student trả lời danh sách 5 sinh viên định dạng JSON", "Hoàn thành 100% (Hình 4.7)", "0.5 / 0.5"),
        ("3", "Database RDBMS", "Tạo CSDL studentdb + bảng students + API đọc /api/students-db", "Hoàn thành 100% (Hình 4.8)", "0.5 / 0.5"),
        ("4", "Keycloak Identity", "Realm mới + client flask-app + users sv01, sv02 + OIDC JWT check", "Hoàn thành 100% (Hình 4.9)", "0.5 / 0.5"),
        ("5", "MinIO Storage", "Tạo bucket profile-pics (avatar) & documents (file PDF báo cáo)", "Hoàn thành 100% (Hình 4.10, 4.11)", "0.5 / 0.5"),
        ("6", "Internal DNS", "Thêm bản ghi zone cloud.local & kiểm tra dig phân giải IP", "Hoàn thành 100% (Hình 4.12)", "0.5 / 0.5"),
        ("7", "Prometheus Scrape", "Thêm target giám sát web-frontend-server:80 ở trạng thái UP", "Hoàn thành 100% (Hình 4.13)", "0.5 / 0.5"),
        ("8", "Grafana Dashboard", "Dashboard System Health 3 biểu đồ sóng động (CPU, RAM, Mạng)", "Hoàn thành 100% (Hình 4.14)", "0.5 / 0.5"),
        ("9", "API Gateway Proxy", "Cấu hình route /student/ chuyển tiếp tới API của Backend", "Hoàn thành 100% (Hình 4.7)", "0.5 / 0.5"),
        ("10", "Load Balancing", "Cân bằng tải Round Robin luân phiên giữa 2 Web Servers", "Hoàn thành 100% (Hình 4.3, 4.4)", "0.5 / 0.5"),
        ("TỔNG", "ĐIỂM ĐÁNH GIÁ", "Cơ bản: 5.0 / 5.0 đ  |  Mở rộng: 5.0 / 5.0 đ", "ĐẠT TRỌN VẸN 10/10 NHIỆM VỤ", "10.0 / 10.0")
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
                set_cell_background(c, "EBF1F5")
                c.paragraphs[0].runs[0].bold = True

    for row in t_eval.rows:
        for cell in row.cells:
            set_cell_margins(cell, 70, 70, 90, 90)

    add_heading_2(doc, "Danh mục Liên kết Nộp bài và Tài nguyên Đồ án")
    add_bullet_item(doc, "1. Kho chứa Mã nguồn GitHub", "https://github.com/minhduc14022005-dev/Cloud_Final")
    add_bullet_item(doc, "2. Docker Hub Image 1 (Web Server)", "https://hub.docker.com/r/minhduc14022005/myminicloud-web")
    add_bullet_item(doc, "3. Docker Hub Image 2 (App Backend)", "https://hub.docker.com/r/minhduc14022005/myminicloud-app")
    add_bullet_item(doc, "4. Địa chỉ IP Máy chủ trực tiếp trên AWS EC2", "http://44.206.252.67")
    add_bullet_item(doc, "5. Liên kết Video Thuyết trình và Demo Thực nghiệm", "[Đính kèm đường dẫn YouTube / Google Drive của Nhóm]")

    out_file = os.path.join(os.path.dirname(__file__), "CK_523H0014_523H0048.docx")
    doc.save(out_file)
    print("Exported final report successfully:", out_file)

if __name__ == "__main__":
    main()
