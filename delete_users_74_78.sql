-- 删除ID为74-78的用户（先删除子表，再删除父表）
USE sports_meet;

-- 先删除志愿者详细信息（子表）
DELETE FROM volunteers WHERE user_id BETWEEN 74 AND 78;

-- 再删除用户（父表）
DELETE FROM users WHERE id BETWEEN 74 AND 78;

SELECT 'ID 74-78 用户已删除' AS result;
