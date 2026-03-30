#!/usr/bin/env python3
"""
生成50个运动员和20个志愿者用户
密码均为123456
"""

from app import app, db, User, Athlete
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

# 班级列表
classes = [
    '计算机2401班', '计算机2402班',
    '软件工程2401班', '软件工程2402班',
    '信息安全2401班', '信息安全2402班',
    '数据科学2401班',
    '人工智能2401班',
    '物联网2401班'
]

# 性别列表
genders = ['男', '女']

with app.app_context():
    print("开始生成用户...")
    
    # 1. 生成50个运动员
    for i in range(21, 71):
        username = f'athlete{i:03d}'
        student_id = f'2024001{i:03d}'
        name = f'运动员{i}'
        phone = f'13900001{i:03d}'
        email = f'{username}@example.com'
        class_name = random.choice(classes)
        gender = random.choice(genders)
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            print(f"用户 {username} 已存在，跳过...")
            continue
        
        # 创建用户
        user = User(
            username=username,
            role='athlete',
            name=name,
            student_id=student_id,
            phone=phone,
            email=email,
            is_active=True,
            created_at=datetime.now()
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.flush()  # 获取user.id
        
        # 创建运动员记录
        athlete = Athlete(
            user_id=user.id,
            name=name,
            student_id=student_id,
            gender=gender,
            class_name=class_name,
            phone=phone,
            id_card=f'1101012000{i:04d}{i:04d}',
            emergency_contact=f'{name}家长',
            emergency_phone=f'1380000{i:04d}',
            is_verified=True,
            created_at=datetime.now()
        )
        db.session.add(athlete)
        
        print(f"创建运动员 {username} - {name}")
    
    # 2. 生成20个志愿者
    for i in range(1, 21):
        username = f'volunteer{i:03d}'
        student_id = f'V2024{i:03d}'
        name = f'志愿者{i}'
        phone = f'13800002{i:03d}'
        email = f'{username}@example.com'
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            print(f"用户 {username} 已存在，跳过...")
            continue
        
        # 创建用户
        user = User(
            username=username,
            role='volunteer',
            name=name,
            student_id=student_id,
            phone=phone,
            email=email,
            is_active=True,
            created_at=datetime.now()
        )
        user.set_password('123456')
        db.session.add(user)
        
        print(f"创建志愿者 {username} - {name}")
    
    # 提交事务
    db.session.commit()
    print("\n用户生成完成！")
    print("运动员账号: athlete021-athlete070, 密码: 123456")
    print("志愿者账号: volunteer001-volunteer020, 密码: 123456")
