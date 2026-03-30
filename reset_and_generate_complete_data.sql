-- 体育运动会管理系统数据生成脚本
-- 清空数据库并重新生成完整数据
-- 保留管理员用户

-- 1. 清空数据库（保留管理员）
SET FOREIGN_KEY_CHECKS = 0;

-- 按顺序删除数据，避免外键约束
DELETE FROM emergency_records;
DELETE FROM medical_info;
DELETE FROM volunteer_assignments;
DELETE FROM volunteer;
DELETE FROM material_in_out;
DELETE FROM materials;
DELETE FROM event_images;
DELETE FROM results;
DELETE FROM schedules;
DELETE FROM registrations;
DELETE FROM events;
DELETE FROM team_scores;
DELETE FROM teams;
DELETE FROM athletes;
DELETE FROM operation_logs;

-- 删除非管理员用户
DELETE FROM users WHERE role != 'admin';

SET FOREIGN_KEY_CHECKS = 1;

-- 2. 生成管理员用户（如果不存在）
INSERT INTO users (username, password_hash, role, name, student_id, phone, email, is_active, created_at) 
VALUES ('admin', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'admin', '系统管理员', 'admin001', '13800138000', 'admin@example.com', 1, NOW())
ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash);

-- 3. 生成老师用户（20个）
INSERT INTO users (username, password_hash, role, name, student_id, phone, email, is_active, created_at) VALUES
('teacher_001', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '王老师', 'teacher001', '13900139001', 'teacher001@example.com', 1, NOW()),
('teacher_002', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '李老师', 'teacher002', '13900139002', 'teacher002@example.com', 1, NOW()),
('teacher_003', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '张老师', 'teacher003', '13900139003', 'teacher003@example.com', 1, NOW()),
('teacher_004', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '刘老师', 'teacher004', '13900139004', 'teacher004@example.com', 1, NOW()),
('teacher_005', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '陈老师', 'teacher005', '13900139005', 'teacher005@example.com', 1, NOW()),
('teacher_006', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '杨老师', 'teacher006', '13900139006', 'teacher006@example.com', 1, NOW()),
('teacher_007', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '赵老师', 'teacher007', '13900139007', 'teacher007@example.com', 1, NOW()),
('teacher_008', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '黄老师', 'teacher008', '13900139008', 'teacher008@example.com', 1, NOW()),
('teacher_009', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '周老师', 'teacher009', '13900139009', 'teacher009@example.com', 1, NOW()),
('teacher_010', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '吴老师', 'teacher010', '13900139010', 'teacher010@example.com', 1, NOW()),
('teacher_011', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '郑老师', 'teacher011', '13900139011', 'teacher011@example.com', 1, NOW()),
('teacher_012', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '孙老师', 'teacher012', '13900139012', 'teacher012@example.com', 1, NOW()),
('teacher_013', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '钱老师', 'teacher013', '13900139013', 'teacher013@example.com', 1, NOW()),
('teacher_014', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '孙老师', 'teacher014', '13900139014', 'teacher014@example.com', 1, NOW()),
('teacher_015', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '周老师', 'teacher015', '13900139015', 'teacher015@example.com', 1, NOW()),
('teacher_016', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '吴老师', 'teacher016', '13900139016', 'teacher016@example.com', 1, NOW()),
('teacher_017', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '郑老师', 'teacher017', '13900139017', 'teacher017@example.com', 1, NOW()),
('teacher_018', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '王老师', 'teacher018', '13900139018', 'teacher018@example.com', 1, NOW()),
('teacher_019', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '李老师', 'teacher019', '13900139019', 'teacher019@example.com', 1, NOW()),
('teacher_020', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'teacher', '张老师', 'teacher020', '13900139020', 'teacher020@example.com', 1, NOW());

-- 4. 生成裁判用户（10个）
INSERT INTO users (username, password_hash, role, name, student_id, phone, email, is_active, created_at) VALUES
('referee_001', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判A', 'referee001', '13700137001', 'referee001@example.com', 1, NOW()),
('referee_002', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判B', 'referee002', '13700137002', 'referee002@example.com', 1, NOW()),
('referee_003', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判C', 'referee003', '13700137003', 'referee003@example.com', 1, NOW()),
('referee_004', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判D', 'referee004', '13700137004', 'referee004@example.com', 1, NOW()),
('referee_005', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判E', 'referee005', '13700137005', 'referee005@example.com', 1, NOW()),
('referee_006', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判F', 'referee006', '13700137006', 'referee006@example.com', 1, NOW()),
('referee_007', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判G', 'referee007', '13700137007', 'referee007@example.com', 1, NOW()),
('referee_008', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判H', 'referee008', '13700137008', 'referee008@example.com', 1, NOW()),
('referee_009', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判I', 'referee009', '13700137009', 'referee009@example.com', 1, NOW()),
('referee_010', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'referee', '裁判J', 'referee010', '13700137010', 'referee010@example.com', 1, NOW());

-- 5. 生成志愿者用户（50个）
INSERT INTO users (username, password_hash, role, name, student_id, phone, email, is_active, created_at) VALUES
('volunteer_001', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者1', 'vol001', '13600136001', 'volunteer001@example.com', 1, NOW()),
('volunteer_002', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者2', 'vol002', '13600136002', 'volunteer002@example.com', 1, NOW()),
('volunteer_003', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者3', 'vol003', '13600136003', 'volunteer003@example.com', 1, NOW()),
('volunteer_004', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者4', 'vol004', '13600136004', 'volunteer004@example.com', 1, NOW()),
('volunteer_005', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者5', 'vol005', '13600136005', 'volunteer005@example.com', 1, NOW()),
('volunteer_006', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者6', 'vol006', '13600136006', 'volunteer006@example.com', 1, NOW()),
('volunteer_007', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者7', 'vol007', '13600136007', 'volunteer007@example.com', 1, NOW()),
('volunteer_008', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者8', 'vol008', '13600136008', 'volunteer008@example.com', 1, NOW()),
('volunteer_009', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者9', 'vol009', '13600136009', 'volunteer009@example.com', 1, NOW()),
('volunteer_010', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者10', 'vol010', '13600136010', 'volunteer010@example.com', 1, NOW()),
('volunteer_011', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者11', 'vol011', '13600136011', 'volunteer011@example.com', 1, NOW()),
('volunteer_012', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者12', 'vol012', '13600136012', 'volunteer012@example.com', 1, NOW()),
('volunteer_013', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者13', 'vol013', '13600136013', 'volunteer013@example.com', 1, NOW()),
('volunteer_014', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者14', 'vol014', '13600136014', 'volunteer014@example.com', 1, NOW()),
('volunteer_015', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者15', 'vol015', '13600136015', 'volunteer015@example.com', 1, NOW()),
('volunteer_016', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者16', 'vol016', '13600136016', 'volunteer016@example.com', 1, NOW()),
('volunteer_017', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者17', 'vol017', '13600136017', 'volunteer017@example.com', 1, NOW()),
('volunteer_018', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者18', 'vol018', '13600136018', 'volunteer018@example.com', 1, NOW()),
('volunteer_019', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者19', 'vol019', '13600136019', 'volunteer019@example.com', 1, NOW()),
('volunteer_020', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者20', 'vol020', '13600136020', 'volunteer020@example.com', 1, NOW()),
('volunteer_021', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者21', 'vol021', '13600136021', 'volunteer021@example.com', 1, NOW()),
('volunteer_022', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者22', 'vol022', '13600136022', 'volunteer022@example.com', 1, NOW()),
('volunteer_023', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者23', 'vol023', '13600136023', 'volunteer023@example.com', 1, NOW()),
('volunteer_024', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者24', 'vol024', '13600136024', 'volunteer024@example.com', 1, NOW()),
('volunteer_025', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者25', 'vol025', '13600136025', 'volunteer025@example.com', 1, NOW()),
('volunteer_026', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者26', 'vol026', '13600136026', 'volunteer026@example.com', 1, NOW()),
('volunteer_027', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者27', 'vol027', '13600136027', 'volunteer027@example.com', 1, NOW()),
('volunteer_028', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者28', 'vol028', '13600136028', 'volunteer028@example.com', 1, NOW()),
('volunteer_029', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者29', 'vol029', '13600136029', 'volunteer029@example.com', 1, NOW()),
('volunteer_030', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者30', 'vol030', '13600136030', 'volunteer030@example.com', 1, NOW()),
('volunteer_031', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者31', 'vol031', '13600136031', 'volunteer031@example.com', 1, NOW()),
('volunteer_032', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者32', 'vol032', '13600136032', 'volunteer032@example.com', 1, NOW()),
('volunteer_033', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者33', 'vol033', '13600136033', 'volunteer033@example.com', 1, NOW()),
('volunteer_034', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者34', 'vol034', '13600136034', 'volunteer034@example.com', 1, NOW()),
('volunteer_035', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者35', 'vol035', '13600136035', 'volunteer035@example.com', 1, NOW()),
('volunteer_036', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者36', 'vol036', '13600136036', 'volunteer036@example.com', 1, NOW()),
('volunteer_037', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者37', 'vol037', '13600136037', 'volunteer037@example.com', 1, NOW()),
('volunteer_038', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者38', 'vol038', '13600136038', 'volunteer038@example.com', 1, NOW()),
('volunteer_039', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者39', 'vol039', '13600136039', 'volunteer039@example.com', 1, NOW()),
('volunteer_040', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者40', 'vol040', '13600136040', 'volunteer040@example.com', 1, NOW()),
('volunteer_041', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者41', 'vol041', '13600136041', 'volunteer041@example.com', 1, NOW()),
('volunteer_042', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者42', 'vol042', '13600136042', 'volunteer042@example.com', 1, NOW()),
('volunteer_043', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者43', 'vol043', '13600136043', 'volunteer043@example.com', 1, NOW()),
('volunteer_044', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者44', 'vol044', '13600136044', 'volunteer044@example.com', 1, NOW()),
('volunteer_045', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者45', 'vol045', '13600136045', 'volunteer045@example.com', 1, NOW()),
('volunteer_046', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者46', 'vol046', '13600136046', 'volunteer046@example.com', 1, NOW()),
('volunteer_047', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者47', 'vol047', '13600136047', 'volunteer047@example.com', 1, NOW()),
('volunteer_048', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者48', 'vol048', '13600136048', 'volunteer048@example.com', 1, NOW()),
('volunteer_049', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者49', 'vol049', '13600136049', 'volunteer049@example.com', 1, NOW()),
('volunteer_050', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'volunteer', '志愿者50', 'vol050', '13600136050', 'volunteer050@example.com', 1, NOW());

-- 6. 生成运动员用户（200个）
INSERT INTO users (username, password_hash, role, name, student_id, phone, email, is_active, created_at) VALUES
('athlete_001', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '张三', '20240001', '13800138001', 'athlete001@example.com', 1, NOW()),
('athlete_002', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '李四', '20240002', '13800138002', 'athlete002@example.com', 1, NOW()),
('athlete_003', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '王五', '20240003', '13800138003', 'athlete003@example.com', 1, NOW()),
('athlete_004', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '赵六', '20240004', '13800138004', 'athlete004@example.com', 1, NOW()),
('athlete_005', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '钱七', '20240005', '13800138005', 'athlete005@example.com', 1, NOW()),
('athlete_006', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '孙八', '20240006', '13800138006', 'athlete006@example.com', 1, NOW()),
('athlete_007', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '周九', '20240007', '13800138007', 'athlete007@example.com', 1, NOW()),
('athlete_008', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '吴十', '20240008', '13800138008', 'athlete008@example.com', 1, NOW()),
('athlete_009', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '郑一', '20240009', '13800138009', 'athlete009@example.com', 1, NOW()),
('athlete_010', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '王二', '20240010', '13800138010', 'athlete010@example.com', 1, NOW()),
('athlete_011', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '陈三', '20240011', '13800138011', 'athlete011@example.com', 1, NOW()),
('athlete_012', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '林四', '20240012', '13800138012', 'athlete012@example.com', 1, NOW()),
('athlete_013', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '黄五', '20240013', '13800138013', 'athlete013@example.com', 1, NOW()),
('athlete_014', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '杨六', '20240014', '13800138014', 'athlete014@example.com', 1, NOW()),
('athlete_015', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '马七', '20240015', '13800138015', 'athlete015@example.com', 1, NOW()),
('athlete_016', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '朱八', '20240016', '13800138016', 'athlete016@example.com', 1, NOW()),
('athlete_017', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '胡九', '20240017', '13800138017', 'athlete017@example.com', 1, NOW()),
('athlete_018', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '郭十', '20240018', '13800138018', 'athlete018@example.com', 1, NOW()),
('athlete_019', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '何一', '20240019', '13800138019', 'athlete019@example.com', 1, NOW()),
('athlete_020', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '高二', '20240020', '13800138020', 'athlete020@example.com', 1, NOW()),
('athlete_021', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '罗三', '20240021', '13800138021', 'athlete021@example.com', 1, NOW()),
('athlete_022', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '梁四', '20240022', '13800138022', 'athlete022@example.com', 1, NOW()),
('athlete_023', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0', 'athlete', '宋五', '20240023', '13800138023', 'athlete023@example.com', 1, NOW()),
('athlete_024', '$scrypt$N=16384,r=8,p=1$o7J2q3R4t5Y6u7i8o9p0a1s2d3f4g5h6j7k8l9$j8e7d6c5b4a3s2d1f0g9h8j7k6l5m4n3b2v1c0