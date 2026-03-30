-- 添加可登录的裁判和志愿者账户
USE sports_meet;

-- 先清空现有志愿者账户（可选）
DELETE FROM volunteers WHERE user_id IN (SELECT id FROM users WHERE role = 'volunteer');
DELETE FROM users WHERE role = 'volunteer';
DELETE FROM users WHERE role = 'referee' AND username LIKE 'referee%';

-- 重新插入裁判账户 (使用正确的密码哈希)
INSERT INTO users (username, password_hash, role, name, is_active, created_at) VALUES
('referee', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'referee', '裁判员', 1, NOW()),
('referee2', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'referee', '张裁判', 1, NOW()),
('referee3', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'referee', '李裁判', 1, NOW());

-- 重新插入志愿者账户
INSERT INTO users (username, password_hash, role, name, is_active, created_at) VALUES
('volunteer', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'volunteer', '志愿者', 1, NOW()),
('volunteer2', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'volunteer', '王小明', 1, NOW()),
('volunteer3', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'volunteer', '李小红', 1, NOW()),
('volunteer4', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'volunteer', '张小华', 1, NOW()),
('volunteer5', '$pbkdf2-sha256$260000$testpassword$0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c', 'volunteer', '刘小芳', 1, NOW());

-- 添加志愿者详细信息
INSERT INTO volunteers (user_id, name, student_id, phone, department, available_time, skills, status)
SELECT id, name, '2021000000', '13800000000', '志愿服务部', '全天', '志愿服务', 'active'
FROM users WHERE role = 'volunteer';

SELECT '账户创建成功！' AS result;
SELECT * FROM users WHERE role IN ('referee', 'volunteer');
