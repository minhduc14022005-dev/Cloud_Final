-- 1. Database cơ bản minicloud
CREATE DATABASE IF NOT EXISTS minicloud CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE minicloud;

CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

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
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO students (student_id, fullname, dob, major) VALUES
('523H0014', 'Võ Huỳnh Minh Đức', '2003-05-15', 'Cloud Computing & DevOps'),
('523H0048', 'Võ Anh Kiệt', '2003-08-20', 'Software Engineering'),
('523H0001', 'Nguyễn Văn An', '2003-01-10', 'Information Security'),
('523H0002', 'Trần Thị Bích', '2003-11-25', 'Data Science');
