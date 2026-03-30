-- 裁判和志愿者测试数据
-- 执行前请确保数据库已创建并运行此脚本

USE sports_meet;

-- 1. 裁判用户数据
INSERT INTO users (username, password_hash, role, name, student_id, phone, email, is_active, created_at) VALUES
('referee_zhang', 'pbkdf2:sha256:260000$random$hash', 'referee', '张裁判', 'REF001', '13700001001', 'zhang@sports.edu', 1, NOW()),
('referee_li', 'pbkdf2:sha256:260000$random$hash', 'referee', '李裁判', 'REF002', '13700001002', 'li@sports.edu', 1, NOW()),
('referee_wang', 'pbkdf2:sha256:260000$random$hash', 'referee', '王裁判', 'REF003', '13700001003', 'wang@sports.edu', 1, NOW()),
('referee_zhao', 'pbkdf2:sha256:260000$random$hash', 'referee', '赵裁判', 'REF004', '13700001004', 'zhao@sports.edu', 1, NOW()),
('referee_liu', 'pbkdf2:sha256:260000$random$hash', 'referee', '刘裁判', 'REF005', '13700001005', 'liu@sports.edu', 1, NOW()),
('referee_chen', 'pbkdf2:sha256:260000$random$hash', 'referee', '陈裁判', 'REF006', '13700001006', 'chen@sports.edu', 1, NOW()),
('referee_yang', 'pbkdf2:sha256:260000$random$hash', 'referee', '杨裁判', 'REF007', '13700001007', 'yang@sports.edu', 1, NOW()),
('referee_zhou', 'pbkdf2:sha256:260000$random$hash', 'referee', '周裁判', 'REF008', '13700001008', 'zhou@sports.edu', 1, NOW());

-- 2. 志愿者用户数据
INSERT INTO users (username, password_hash, role, name, student_id, phone, email, is_active, created_at) VALUES
('volunteer_wang', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '王小明', '2021010101', '13900001001', 'wangxm@student.edu', 1, NOW()),
('volunteer_li', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '李小红', '2021010102', '13900001002', 'lixh@student.edu', 1, NOW()),
('volunteer_zhang', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '张小华', '2021020201', '13900001003', 'zhangxh@student.edu', 1, NOW()),
('volunteer_liu', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '刘小芳', '2021020202', '13900001004', 'liuxf@student.edu', 1, NOW()),
('volunteer_chen', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '陈小刚', '2021030301', '13900001005', 'chenxg@student.edu', 1, NOW()),
('volunteer_zhao', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '赵小丽', '2021030302', '13900001006', 'zhaoxl@student.edu', 1, NOW()),
('volunteer_zhou', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '杨小强', '2021040401', '13900001007', 'yangxq@student.edu', 1, NOW()),
('volunteer_wu', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '吴小敏', '2021040402', '13900001008', 'wuxm@student.edu', 1, NOW()),
('volunteer_zhu', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '郑小磊', '2021050501', '13900001009', 'zhengxl@student.edu', 1, NOW()),
('volunteer_sun', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '孙小燕', '2021050502', '13900001010', 'sunxy@student.edu', 1, NOW()),
('volunteer_ma', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '马小超', '2021060601', '13900001011', 'maxc@student.edu', 1, NOW()),
('volunteer_tan', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '谭小雯', '2021060602', '13900001012', 'tanxw@student.edu', 1, NOW()),
('volunteer_yan', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '严小波', '2021010103', '13900001013', 'yanxb@student.edu', 1, NOW()),
('volunteer_su', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '苏小品', '2021010104', '13900001014', 'suxp@student.edu', 1, NOW()),
('volunteer_pan', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '潘小小', '2021020203', '13900001015', 'panxx@student.edu', 1, NOW()),
('volunteer_deng', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '邓小刚', '2021020204', '13900001016', 'dengxg@student.edu', 1, NOW()),
('volunteer_xu', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '徐小丽', '2021030303', '13900001017', 'xuxl@student.edu', 1, NOW()),
('volunteer_isun', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '宋小强', '2021030304', '13900001018', 'songxq@student.edu', 1, NOW()),
('volunteer_wei', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '魏小敏', '2021040403', '13900001019', 'weixm@student.edu', 1, NOW()),
('volunteer_tang', 'pbkdf2:sha256:260000$random$hash', 'volunteer', '汤小磊', '2021040404', '13900001020', 'tangxl@student.edu', 1, NOW());

-- 3. 更新密码为哈希值（使用werkzeug生成的实际哈希）
-- 注意：实际部署时应使用正确的密码哈希，这里用示例哈希
UPDATE users SET password_hash = '$pbkdf2-sha256$260000$test$test12345678901234567890123456789012345678901234567890123456' WHERE role = 'referee';
UPDATE users SET password_hash = '$pbkdf2-sha256$260000$test$test12345678901234567890123456789012345678901234567890123456' WHERE role = 'volunteer';

-- 4. 志愿者详细信息
INSERT INTO volunteers (user_id, name, student_id, phone, department, available_time, skills, status) VALUES
(3, '王小明', '2021010101', '13900001001', '计算机学院', '全天', '摄影、视频制作', 'active'),
(4, '李小红', '2021010102', '13900001002', '计算机学院', '上午', '急救技能', 'active'),
(5, '张小华', '2021020201', '13900001003', '机械学院', '全天', '场地布置', 'active'),
(6, '刘小芳', '2021020202', '13900001004', '机械学院', '下午', '物资管理', 'active'),
(7, '陈小刚', '2021030301', '13900001005', '电子学院', '全天', '设备维护', 'active'),
(8, '赵小丽', '2021030302', '13900001006', '电子学院', '上午', '引导服务', 'active'),
(9, '杨小强', '2021040401', '13900001007', '经管学院', '全天', '秩序维护', 'active'),
(10, '吴小敏', '2021040402', '13900001008', '经管学院', '下午', '成绩统计', 'active'),
(11, '郑小磊', '2021050501', '13900001009', '外语学院', '全天', '外语翻译', 'active'),
(12, '孙小燕', '2021050502', '13900001010', '外语学院', '上午', '接待服务', 'active'),
(13, '马小超', '2021060601', '13900001011', '土木学院', '下午', '搬运物资', 'active'),
(14, '谭小雯', '2021060602', '13900001012', '土木学院', '全天', '急救技能', 'active'),
(15, '严小波', '2021010103', '13900001013', '计算机学院', '全天', '摄影', 'active'),
(16, '苏小品', '2021010104', '13900001014', '计算机学院', '下午', '新媒体运营', 'active'),
(17, '潘小小', '2021020203', '13900001015', '机械学院', '全天', '机械维修', 'active'),
(18, '邓小刚', '2021020204', '13900001016', '机械学院', '全天', '电器维修', 'active'),
(19, '徐小丽', '2021030303', '13900001017', '电子学院', '上午', '通信设备调试', 'active'),
(20, '宋小强', '2021030304', '13900001018', '电子学院', '下午', '电脑维护', 'active'),
(21, '魏小敏', '2021040403', '13900001019', '经管学院', '全天', '文秘工作', 'active'),
(22, '汤小磊', '2021040404', '13900001020', '经管学院', '全天', '财务管理', 'active');

-- 5. 志愿者任务分配
INSERT INTO volunteer_assignments (volunteer_id, position_name, event_id, schedule_id, task_description, status) VALUES
(1, '摄影师', 1, 1, '拍摄男子100米比赛', 'completed'),
(1, '摄影师', 1, 2, '拍摄男子100米决赛', 'completed'),
(1, '摄影师', 15, 21, '拍摄接力比赛', 'completed'),
(2, '急救志愿者', 1, 1, '现场急救保障', 'completed'),
(2, '急救志愿者', 9, 13, '跳远场地医疗保障', 'completed'),
(3, '场地布置员', 1, 1, '赛前场地布置', 'completed'),
(3, '场地布置员', 9, 13, '田赛场地布置', 'completed'),
(4, '物资管理员', NULL, NULL, '管理赛事物资', 'completed'),
(4, '物资管理员', NULL, NULL, '管理开幕式物资', 'completed'),
(5, '设备维护员', 1, 1, '检查起跑设备', 'completed'),
(5, '设备维护员', 15, 21, '接力赛设备检查', 'completed'),
(6, '引导员', NULL, NULL, '引导运动员入场', 'completed'),
(6, '引导员', NULL, NULL, '引导观众就座', 'completed'),
(7, '秩序维护员', 9, 13, '维护跳远比赛秩序', 'completed'),
(7, '秩序维护员', 11, 17, '维护跳高比赛秩序', 'completed'),
(8, '成绩记录员', 1, 2, '记录决赛成绩', 'completed'),
(8, '成绩记录员', 3, 6, '记录200米成绩', 'completed'),
(9, '翻译志愿者', NULL, NULL, '外国来宾翻译', 'completed'),
(9, '翻译志愿者', NULL, NULL, '外宾接待', 'completed'),
(10, '接待员', NULL, NULL, '接待领导来宾', 'completed'),
(10, '接待员', NULL, NULL, '开幕式接待', 'completed'),
(11, '物资搬运员', NULL, NULL, '搬运比赛器材', 'completed'),
(11, '物资搬运员', 13, 19, '搬运铅球器材', 'completed'),
(12, '急救志愿者', 9, 13, '跳远场地医疗保障', 'completed'),
(12, '急救志愿者', 14, 20, '铅球场地医疗保障', 'completed'),
(13, '摄影师', NULL, NULL, '拍摄开幕式', 'completed'),
(13, '摄影师', NULL, NULL, '拍摄闭幕式', 'completed'),
(14, '新媒体运营', NULL, NULL, '赛事直播', 'completed'),
(14, '新媒体运营', NULL, NULL, '社交媒体发布', 'completed'),
(15, '设备维护员', 2, 3, '女子100米设备检查', 'completed'),
(16, '设备维护员', NULL, NULL, '音响设备维护', 'completed'),
(17, '通信设备调试', 1, 1, '检录处设备调试', 'completed'),
(18, '电脑维护', NULL, NULL, '成绩录入系统维护', 'completed'),
(19, '文秘工作', NULL, NULL, '文件整理', 'completed'),
(20, '财务管理', NULL, NULL, '奖金核算', 'completed');

SELECT '裁判和志愿者数据生成完成！' AS result;
