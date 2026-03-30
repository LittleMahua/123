-- 数据库字段修复脚本
-- 运行此脚本添加缺失的字段到现有数据库表

-- 1. 为 users 表添加缺失字段
ALTER TABLE users ADD COLUMN email VARCHAR(100);
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD COLUMN last_login DATETIME;

-- 2. 为 athletes 表添加缺失字段
ALTER TABLE athletes ADD COLUMN user_id INT;
ALTER TABLE athletes ADD COLUMN id_card VARCHAR(20);
ALTER TABLE athletes ADD COLUMN emergency_contact VARCHAR(50);
ALTER TABLE athletes ADD COLUMN emergency_phone VARCHAR(20);
ALTER TABLE athletes ADD COLUMN is_verified BOOLEAN DEFAULT FALSE;

-- 3. 为 events 表添加缺失字段
ALTER TABLE events ADD COLUMN group_type VARCHAR(50);
ALTER TABLE events ADD COLUMN min_participants INT DEFAULT 1;
ALTER TABLE events ADD COLUMN registration_start DATETIME;
ALTER TABLE events ADD COLUMN registration_end DATETIME;
ALTER TABLE events ADD COLUMN scoring_rule VARCHAR(50) DEFAULT 'standard';
ALTER TABLE events ADD COLUMN points_first INT DEFAULT 7;
ALTER TABLE events ADD COLUMN points_second INT DEFAULT 5;
ALTER TABLE events ADD COLUMN points_third INT DEFAULT 3;
ALTER TABLE events ADD COLUMN is_recordable BOOLEAN DEFAULT TRUE;
ALTER TABLE events ADD COLUMN unit VARCHAR(20) DEFAULT '秒';
ALTER TABLE events ADD COLUMN description TEXT;
ALTER TABLE events ADD COLUMN status VARCHAR(20) DEFAULT 'draft';

-- 4. 为 registrations 表添加缺失字段
ALTER TABLE registrations ADD COLUMN review_note TEXT;
ALTER TABLE registrations ADD COLUMN reviewed_by INT;
ALTER TABLE registrations ADD COLUMN reviewed_at DATETIME;

-- 5. 为 schedules 表添加缺失字段
ALTER TABLE schedules ADD COLUMN round_number INT DEFAULT 1;
ALTER TABLE schedules ADD COLUMN notes TEXT;

-- 6. 为 results 表添加缺失字段
ALTER TABLE results ADD COLUMN is_record_broken BOOLEAN DEFAULT FALSE;
ALTER TABLE results ADD COLUMN record_approval_status VARCHAR(20) DEFAULT 'pending';
ALTER TABLE results ADD COLUMN entered_by INT;
ALTER TABLE results ADD COLUMN is_final BOOLEAN DEFAULT FALSE;
ALTER TABLE results ADD COLUMN updated_at DATETIME;

-- 7. 为 announcements 表添加缺失字段
ALTER TABLE announcements ADD COLUMN priority VARCHAR(20) DEFAULT 'normal';
ALTER TABLE announcements ADD COLUMN view_count INT DEFAULT 0;
ALTER TABLE announcements ADD COLUMN updated_at DATETIME;

SELECT '数据库修复完成！' AS result;
