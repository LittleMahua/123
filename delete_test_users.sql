-- 删除多余的裁判和志愿者测试账户
USE sports_meet;

-- 删除裁判账户
DELETE FROM users WHERE username IN ('referee', 'referee2', 'referee3');

-- 删除志愿者账户
DELETE FROM users WHERE username IN ('volunteer', 'volunteer2', 'volunteer3', 'volunteer4', 'volunteer5');

-- 删除对应的志愿者详细信息
DELETE FROM volunteers WHERE user_id NOT IN (SELECT id FROM users WHERE role = 'volunteer');

SELECT '多余用户已删除' AS result;
