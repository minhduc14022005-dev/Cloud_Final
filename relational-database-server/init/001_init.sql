-- Client init mặc định dùng latin1, thiếu dòng này tên tiếng Việt bị lưu sai mã (mojibake)
SET NAMES utf8mb4;

-- 1. Database cơ bản minicloud
CREATE DATABASE IF NOT EXISTS minicloud CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE minicloud;

CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO notes (title) VALUES ('Hello from MySQL!');

-- 2. Database mở rộng 3: studentdb
CREATE DATABASE IF NOT EXISTS studentdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE studentdb;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    major VARCHAR(50) NOT NULL
);

INSERT INTO students (student_id, fullname, dob, major) VALUES
('21110001', 'Võ Huỳnh Minh Đức', '2003-05-15', 'Cloud Computing & DevOps'),
('21110002', 'Võ Anh Kiệt', '2003-08-20', 'Software Engineering'),
('21110003', 'Nguyễn Văn An', '2003-01-10', 'Information Security'),
('21110004', 'Trần Thị Bích', '2003-11-25', 'Data Science');

