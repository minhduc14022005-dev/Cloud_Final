const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const mysql = require('mysql2/promise');
const jwt = require('jsonwebtoken');
const jwksRsa = require('jwks-rsa');

const app = express();
const PORT = process.env.PORT || 8081;

app.use(cors());
app.use(express.json());

// Cấu hình Keycloak OIDC
// Issuer trong token phụ thuộc địa chỉ người dùng gọi Keycloak (vd localhost:8081),
// còn container backend phải lấy khóa qua tên nội bộ => tách 2 biến.
const ISSUER = process.env.OIDC_ISSUER || 'http://localhost:8081/realms/realm_523H0048';
const JWKS_URI = process.env.OIDC_JWKS_URI || `${ISSUER}/protocol/openid-connect/certs`;
const AUDIENCE = process.env.OIDC_AUDIENCE || 'flask-app';

const jwksClient = jwksRsa({
    jwksUri: JWKS_URI,
    cache: true,
    cacheMaxAge: 600000, // 10 phút
    rateLimit: true,
    jwksRequestsPerMinute: 10
});

function getKey(header, callback) {
    jwksClient.getSigningKey(header.kid, function (err, key) {
        if (err) {
            return callback(err, null);
        }
        const signingKey = key.getPublicKey ? key.getPublicKey() : key.rsaPublicKey;
        callback(null, signingKey);
    });
}

// 1. Cơ bản: API /hello
app.get('/hello', (req, res) => {
    res.json({ message: 'Hello from App Server!' });
});

// 2. Mở rộng 2: API /student đọc dữ liệu từ students.json
app.get('/student', (req, res) => {
    const jsonPath = path.join(__dirname, 'students.json');
    if (!fs.existsSync(jsonPath)) {
        return res.status(404).json({ error: 'students.json not found' });
    }
    try {
        const rawData = fs.readFileSync(jsonPath, 'utf-8');
        const students = JSON.parse(rawData);
        res.json(students);
    } catch (err) {
        res.status(500).json({ error: 'Error reading students.json', details: err.message });
    }
});

// 3. Cơ bản: API /secure xác thực OIDC JWT từ Keycloak
app.get('/secure', (req, res) => {
    const authHeader = req.headers['authorization'] || '';
    if (!authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing Bearer token' });
    }

    const token = authHeader.split(' ')[1];
    jwt.verify(
        token,
        getKey,
        {
            issuer: ISSUER,
            audience: AUDIENCE,
            algorithms: ['RS256']
        },
        (err, decoded) => {
            if (err) {
                return res.status(401).json({ error: 'Invalid token', details: err.message });
            }
            res.json({
                message: 'Secure resource OK',
                preferred_username: decoded.preferred_username || decoded.sub,
                user: decoded
            });
        }
    );
});

// 4. Mở rộng 3: API /students-db đọc từ MySQL
app.get('/students-db', async (req, res) => {
    const dbConfig = {
        host: process.env.DB_HOST || 'relational-database-server',
        user: process.env.DB_USER || 'root',
        password: process.env.DB_PASSWORD || 'root',
        database: process.env.DB_NAME || 'studentdb',
        charset: 'utf8mb4',
        connectTimeout: 4000
    };

    try {
        const connection = await mysql.createConnection(dbConfig);
        const [rows] = await connection.execute(
            "SELECT id, student_id, fullname, DATE_FORMAT(dob, '%Y-%m-%d') as dob, major FROM students;"
        );
        await connection.end();
        res.json({
            source: 'MySQL studentdb (Node.js)',
            count: rows.length,
            data: rows
        });
    } catch (err) {
        res.status(500).json({
            error: 'Database query failed',
            details: err.message
        });
    }
});

// Khởi chạy server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`[Node.js App Server] listening on http://0.0.0.0:${PORT}`);
});

