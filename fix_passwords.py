#!/usr/bin/env python3
"""
修复数据库中用户密码哈希问题
为所有 password_hash 为空的用户设置密码为 123456
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    print("开始修复用户密码...")
    
    # 查找所有 password_hash 为空的用户
    users_with_empty_password = User.query.filter(User.password_hash == '').all()
    users_with_none_password = User.query.filter(User.password_hash.is_(None)).all()
    
    all_problematic_users = users_with_empty_password + users_with_none_password
    
    if not all_problematic_users:
        print("没有发现密码为空的用户，无需修复")
    else:
        print(f"发现 {len(all_problematic_users)} 个密码为空的用户")
        
        for user in all_problematic_users:
            user.set_password('123456')
            print(f"修复用户: {user.username} - 设置密码为 123456")
        
        db.session.commit()
        print("密码修复完成！")
    
    # 检查所有用户的密码状态
    all_users = User.query.all()
    print(f"\n数据库中共有 {len(all_users)} 个用户")
    print("用户列表:")
    for user in all_users:
        password_status = "有效" if user.password_hash and len(user.password_hash) > 20 else "无效"
        print(f"  {user.username} ({user.role}) - 密码: {password_status}")
