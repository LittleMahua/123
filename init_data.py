"""
体育运动会管理系统 - 完整数据生成脚本
生成：
- 200个运动员
- 10个裁判
- 20个老师
- 50个志愿者
- 20条赛事
- 20+条赛程
- 报名审核、比赛成绩、团队、物资、志愿者任务、医疗点、应急记录、公告等
"""

import sys
sys.path.insert(0, r'D:\APP\JetBrains\PyCharm 2025.2.3\data\PythonProject1')

from app import app, db, User, Athlete, Event, Registration, Schedule, Result, Team, TeamScore, \
    Announcement, Material, MaterialInOut, Volunteer, VolunteerAssignment, MedicalInfo, EmergencyRecord
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from sqlalchemy import text
import random

# 密码哈希（123456）
PASSWORD_HASH = generate_password_hash('123456')

# 常用姓氏和名字
SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '周', '吴', '徐', '孙', '马', '朱', '胡', '郭', '何', '高', '林', '罗', '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹', '彭', '曾', '肖', '田', '董', '袁', '潘', '于', '蒋', '蔡', '余', '杜', '叶', '程', '苏', '魏', '吕', '丁', '任', '沈']
NAMES_MALE = ['伟', '强', '磊', '军', '明', '辉', '刚', '建', '峰', '宇', '浩', '博', '文', '杰', '鑫', '俊', '涛', '超', '勇', '毅', '翔', '凯', '华', '飞', '志', '龙', '海', '波', '鹏', '宇', '浩', '然', '轩', '瑞', '泽', '昊', '晨', '辰', '逸', '睿']
NAMES_FEMALE = ['芳', '娜', '秀', '敏', '静', '丽', '强', '磊', '军', '洋', '艳', '杰', '娟', '霞', '婷', '雪', '颖', '梅', '琳', '玲', '萍', '燕', '华', '红', '倩', '璐', '琪', '瑶', '欣', '怡', '佳', '彤', '雯', '茜', '菲', '萱', '妍', '媛', '薇', '蕾']

CLASSES = ['计算机1班', '计算机2班', '计算机3班', '软件工程1班', '软件工程2班', '网络工程1班', '网络工程2班', '信息安全1班', '人工智能1班', '大数据1班',
           '电子1班', '电子2班', '通信1班', '通信2班', '自动化1班', '自动化2班', '电气1班', '电气2班', '机械1班', '机械2班']

def generate_name(gender=None):
    """生成中文姓名"""
    surname = random.choice(SURNAMES)
    if gender == 'male':
        name = random.choice(NAMES_MALE)
    elif gender == 'female':
        name = random.choice(NAMES_FEMALE)
    else:
        name = random.choice(NAMES_MALE + NAMES_FEMALE)
    return surname + name

def generate_phone():
    """生成手机号"""
    prefixes = ['138', '139', '137', '136', '135', '134', '150', '151', '152', '157', '158', '159', '182', '183', '187', '188']
    return random.choice(prefixes) + ''.join([str(random.randint(0, 9)) for _ in range(8)])

def clear_data():
    """清空所有数据（保留管理员）"""
    print("清空数据库...")
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    
    tables = [
        'emergency_records', 'medical_info', 'volunteer_assignments', 'volunteers',
        'material_in_out', 'materials', 'event_images', 'results', 'schedules',
        'registrations', 'events', 'team_scores', 'teams', 'athletes', 'operation_logs'
    ]
    
    for table in tables:
        db.session.execute(text(f"DELETE FROM {table}"))
    
    db.session.execute(text("DELETE FROM users WHERE role != 'admin'"))
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    db.session.commit()
    print("数据库已清空（保留管理员）")

def create_teachers():
    """创建20个老师"""
    print("创建20个老师...")
    teachers = []
    for i in range(1, 21):
        teacher = User(
            username=f'teacher_{i:03d}',
            password_hash=PASSWORD_HASH,
            role='teacher',
            name=f'{random.choice(SURNAMES)}老师',
            student_id=f'teacher{i:03d}',
            phone=generate_phone(),
            email=f'teacher{i:03d}@example.com',
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(30, 90))
        )
        teachers.append(teacher)
    
    db.session.add_all(teachers)
    db.session.commit()
    print(f"已创建 {len(teachers)} 个老师")
    return teachers

def create_referees():
    """创建10个裁判"""
    print("创建10个裁判...")
    referees = []
    for i in range(1, 11):
        referee = User(
            username=f'referee_{i:03d}',
            password_hash=PASSWORD_HASH,
            role='referee',
            name=f'裁判{chr(64+i)}',
            student_id=f'referee{i:03d}',
            phone=generate_phone(),
            email=f'referee{i:03d}@example.com',
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(30, 90))
        )
        referees.append(referee)
    
    db.session.add_all(referees)
    db.session.commit()
    print(f"已创建 {len(referees)} 个裁判")
    return [r.id for r in referees]

def create_volunteers():
    """创建50个志愿者"""
    print("创建50个志愿者...")
    volunteers_users = []
    volunteers_profiles = []
    
    for i in range(1, 51):
        name = generate_name()
        user = User(
            username=f'volunteer_{i:03d}',
            password_hash=PASSWORD_HASH,
            role='volunteer',
            name=name,
            student_id=f'vol{i:03d}',
            phone=generate_phone(),
            email=f'volunteer{i:03d}@example.com',
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(10, 60))
        )
        volunteers_users.append(user)
    
    db.session.add_all(volunteers_users)
    db.session.commit()
    
    # 创建志愿者档案
    departments = ['学生会', '团委', '社团联合会', '青年志愿者协会', '红十字会', '班级']
    for i, user in enumerate(volunteers_users):
        volunteer = Volunteer(
            user_id=user.id,
            name=user.name,
            student_id=user.student_id,
            phone=user.phone,
            department=random.choice(departments),
            available_time='周末及节假日',
            skills=random.choice(['摄影', '文案', '组织', '医疗', '翻译', '计算机', '体育']),
            status='active'
        )
        volunteers_profiles.append(volunteer)
    
    db.session.add_all(volunteers_profiles)
    db.session.commit()
    print(f"已创建 {len(volunteers_users)} 个志愿者")
    return volunteers_users, volunteers_profiles

def create_athletes():
    """创建200个运动员"""
    print("创建200个运动员...")
    athletes_users = []
    athletes_profiles = []
    
    for i in range(1, 201):
        gender = random.choice(['男', '女'])
        name = generate_name('male' if gender == '男' else 'female')
        
        user = User(
            username=f'athlete_{i:03d}',
            password_hash=PASSWORD_HASH,
            role='athlete',
            name=name,
            student_id=f'2024{i:04d}',
            phone=generate_phone(),
            email=f'athlete{i:03d}@example.com',
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(5, 45))
        )
        athletes_users.append(user)
    
    db.session.add_all(athletes_users)
    db.session.commit()
    
    # 创建运动员档案
    for i, user in enumerate(athletes_users):
        gender = '男' if i % 2 == 0 else '女'
        athlete = Athlete(
            user_id=user.id,
            name=user.name,
            student_id=user.student_id,
            gender=gender,
            class_name=random.choice(CLASSES),
            phone=user.phone,
            id_card=f'{random.randint(100000, 999999)}{random.randint(10000000, 99999999)}',
            emergency_contact=generate_name(),
            emergency_phone=generate_phone(),
            is_verified=random.choice([True, True, True, False]),
            created_at=user.created_at
        )
        athletes_profiles.append(athlete)
    
    db.session.add_all(athletes_profiles)
    db.session.commit()
    print(f"已创建 {len(athletes_users)} 个运动员")
    return athletes_users, athletes_profiles

def create_events():
    """创建20条赛事"""
    print("创建20条赛事...")
    
    events_data = [
        {'name': '男子100米', 'event_type': '径赛', 'gender': '男', 'group_type': '个人', 'unit': '秒'},
        {'name': '女子100米', 'event_type': '径赛', 'gender': '女', 'group_type': '个人', 'unit': '秒'},
        {'name': '男子200米', 'event_type': '径赛', 'gender': '男', 'group_type': '个人', 'unit': '秒'},
        {'name': '女子200米', 'event_type': '径赛', 'gender': '女', 'group_type': '个人', 'unit': '秒'},
        {'name': '男子400米', 'event_type': '径赛', 'gender': '男', 'group_type': '个人', 'unit': '秒'},
        {'name': '女子400米', 'event_type': '径赛', 'gender': '女', 'group_type': '个人', 'unit': '秒'},
        {'name': '男子800米', 'event_type': '径赛', 'gender': '男', 'group_type': '个人', 'unit': '分'},
        {'name': '女子800米', 'event_type': '径赛', 'gender': '女', 'group_type': '个人', 'unit': '分'},
        {'name': '男子1500米', 'event_type': '径赛', 'gender': '男', 'group_type': '个人', 'unit': '分'},
        {'name': '女子1500米', 'event_type': '径赛', 'gender': '女', 'group_type': '个人', 'unit': '分'},
        {'name': '男子跳远', 'event_type': '田赛', 'gender': '男', 'group_type': '个人', 'unit': '米'},
        {'name': '女子跳远', 'event_type': '田赛', 'gender': '女', 'group_type': '个人', 'unit': '米'},
        {'name': '男子跳高', 'event_type': '田赛', 'gender': '男', 'group_type': '个人', 'unit': '米'},
        {'name': '女子跳高', 'event_type': '田赛', 'gender': '女', 'group_type': '个人', 'unit': '米'},
        {'name': '男子铅球', 'event_type': '田赛', 'gender': '男', 'group_type': '个人', 'unit': '米'},
        {'name': '女子铅球', 'event_type': '田赛', 'gender': '女', 'group_type': '个人', 'unit': '米'},
        {'name': '男子4x100米接力', 'event_type': '径赛', 'gender': '男', 'group_type': '团体', 'unit': '秒'},
        {'name': '女子4x100米接力', 'event_type': '径赛', 'gender': '女', 'group_type': '团体', 'unit': '秒'},
        {'name': '混合4x400米接力', 'event_type': '径赛', 'gender': '混合', 'group_type': '团体', 'unit': '秒'},
        {'name': '男女混合跳绳', 'event_type': '趣味', 'gender': '混合', 'group_type': '团体', 'unit': '个'},
    ]
    
    events = []
    for i, data in enumerate(events_data):
        event = Event(
            name=data['name'],
            event_type=data['event_type'],
            gender=data['gender'],
            group_type=data['group_type'],
            max_participants=random.randint(8, 20),
            min_participants=1 if data['group_type'] == '个人' else 4,
            location=random.choice(['田径场', '体育馆', '室外篮球场', '足球场']),
            registration_start=datetime.now() - timedelta(days=30),
            registration_end=datetime.now() + timedelta(days=5),
            scoring_rule='standard',
            points_first=9,
            points_second=7,
            points_third=5,
            is_recordable=True,
            unit=data['unit'],
            description=f'{data["name"]}项目，欢迎踊跃报名！',
            status='published'
        )
        events.append(event)
    
    db.session.add_all(events)
    db.session.commit()
    print(f"已创建 {len(events)} 条赛事")
    return events

def create_schedules(events):
    """创建25条赛程安排"""
    print("创建25条赛程安排...")
    schedules = []
    
    base_date = datetime.now() + timedelta(days=3)
    times = [
        (8, 30), (9, 0), (9, 30), (10, 0), (10, 30),
        (14, 0), (14, 30), (15, 0), (15, 30), (16, 0)
    ]
    
    locations = ['田径场A区', '田径场B区', '田径场C区', '体育馆', '跳远沙坑', '铅球场地']
    
    for i in range(25):
        event = random.choice(events)
        day_offset = i // 10
        hour, minute = times[i % len(times)]
        
        start_time = base_date + timedelta(days=day_offset, hours=hour-8, minutes=minute)
        end_time = start_time + timedelta(minutes=random.randint(30, 90))
        
        schedule = Schedule(
            event_id=event.id,
            round_number=random.randint(1, 3),
            start_time=start_time,
            end_time=end_time,
            location=random.choice(locations),
            status=random.choice(['scheduled', 'ongoing', 'completed']),
            notes=f'{event.name}第{random.randint(1,3)}轮'
        )
        schedules.append(schedule)
    
    db.session.add_all(schedules)
    db.session.commit()
    print(f"已创建 {len(schedules)} 条赛程")
    return schedules

def create_registrations(athletes, events):
    """创建报名记录"""
    print("创建报名记录...")
    registrations = []
    
    for athlete in athletes:
        # 每个运动员报名2-4个项目
        num_events = random.randint(2, 4)
        selected_events = random.sample(events, min(num_events, len(events)))
        
        for event in selected_events:
            # 跳过性别不匹配的项目
            if event.gender == '男' and athlete.gender != '男':
                continue
            if event.gender == '女' and athlete.gender != '女':
                continue
                
            registration = Registration(
                athlete_id=athlete.id,
                event_id=event.id,
                status=random.choice(['approved', 'approved', 'approved', 'pending', 'rejected']),
                review_note='',
                created_at=datetime.now() - timedelta(days=random.randint(5, 25))
            )
            registrations.append(registration)
    
    db.session.add_all(registrations)
    db.session.commit()
    print(f"已创建 {len(registrations)} 条报名记录")
    return registrations

def create_results(schedules, athletes, events_dict, referee_ids):
    """创建比赛成绩"""
    print("创建比赛成绩...")
    results = []
    
    for schedule in schedules:
        if schedule.status == 'completed':
            # 为已完成的赛程生成成绩
            num_participants = random.randint(5, 12)
            selected_athletes = random.sample(athletes, min(num_participants, len(athletes)))
            
            event = events_dict.get(schedule.event_id)
            
            for rank, athlete in enumerate(selected_athletes, 1):
                # 根据赛事类型生成成绩
                if event:
                    if event.unit == '秒':
                        score = f"{random.randint(10, 60)}.{random.randint(0, 99):02d}"
                    elif event.unit == '分':
                        score = f"{random.randint(2, 8)}:{random.randint(0, 59):02d}"
                    elif event.unit == '米':
                        score = f"{random.uniform(1.5, 15.0):.2f}"
                    else:
                        score = str(random.randint(50, 200))
                else:
                    score = str(random.randint(10, 100))
                
                result = Result(
                    schedule_id=schedule.id,
                    athlete_id=athlete.id,
                    rank=rank if rank <= 8 else None,
                    score=score,
                    is_record_broken=random.choice([False, False, False, True]),
                    record_approval_status='approved' if random.random() > 0.9 else 'pending',
                    remarks='',
                    entered_by=random.choice(referee_ids),
                    is_final=True
                )
                results.append(result)
    
    db.session.add_all(results)
    db.session.commit()
    print(f"已创建 {len(results)} 条成绩记录")
    return results

def create_teams():
    """创建团队"""
    print("创建团队...")
    teams = []
    team_names = ['计算机学院', '软件学院', '电子工程学院', '通信学院', '自动化学院', 
                  '机械学院', '电气学院', '理学院', '经管学院', '人文学院']
    
    for i, name in enumerate(team_names):
        team = Team(
            name=name,
            code=f'TEAM{i+1:02d}',
            coach=generate_name(),
            contact_phone=generate_phone(),
            member_count=random.randint(15, 30),
            total_score=random.randint(0, 100),
            rank=i + 1
        )
        teams.append(team)
    
    db.session.add_all(teams)
    db.session.commit()
    print(f"已创建 {len(teams)} 个团队")
    return teams

def create_materials():
    """创建物资"""
    print("创建物资...")
    materials = []
    
    materials_data = [
        {'name': '发令枪', 'category': '器材', 'quantity': 5, 'unit': '把'},
        {'name': '秒表', 'category': '器材', 'quantity': 20, 'unit': '个'},
        {'name': '跨栏架', 'category': '器材', 'quantity': 30, 'unit': '个'},
        {'name': '铅球', 'category': '器材', 'quantity': 10, 'unit': '个'},
        {'name': '标枪', 'category': '器材', 'quantity': 15, 'unit': '支'},
        {'name': '铁饼', 'category': '器材', 'quantity': 8, 'unit': '个'},
        {'name': '跳高垫', 'category': '器材', 'quantity': 6, 'unit': '块'},
        {'name': '沙坑耙', 'category': '器材', 'quantity': 4, 'unit': '把'},
        {'name': '号码布', 'category': '用品', 'quantity': 500, 'unit': '张'},
        {'name': '别针', 'category': '用品', 'quantity': 1000, 'unit': '个'},
        {'name': '饮用水', 'category': '消耗品', 'quantity': 200, 'unit': '箱'},
        {'name': '功能饮料', 'category': '消耗品', 'quantity': 50, 'unit': '箱'},
        {'name': '急救箱', 'category': '医疗', 'quantity': 10, 'unit': '个'},
        {'name': '担架', 'category': '医疗', 'quantity': 4, 'unit': '副'},
        {'name': '氧气袋', 'category': '医疗', 'quantity': 6, 'unit': '个'},
    ]
    
    for data in materials_data:
        material = Material(
            name=data['name'],
            category=data['category'],
            quantity=data['quantity'],
            unit=data['unit'],
            min_stock=random.randint(1, 5),
            location=random.choice(['器材室A', '器材室B', '医疗站', '后勤仓库']),
            description=f'{data["name"]}，用于运动会',
            status='normal'
        )
        materials.append(material)
    
    db.session.add_all(materials)
    db.session.commit()
    print(f"已创建 {len(materials)} 种物资")
    return materials

def create_material_records(materials):
    """创建物资出入库记录"""
    print("创建物资出入库记录...")
    records = []
    
    for material in materials:
        # 入库记录
        for _ in range(random.randint(1, 3)):
            record = MaterialInOut(
                material_id=material.id,
                operation_type='in',
                quantity=random.randint(10, 50),
                operator_id=1,
                notes='采购入库'
            )
            records.append(record)
        
        # 出库记录
        for _ in range(random.randint(0, 2)):
            record = MaterialInOut(
                material_id=material.id,
                operation_type='out',
                quantity=random.randint(1, 10),
                operator_id=1,
                notes='领用出库'
            )
            records.append(record)
    
    db.session.add_all(records)
    db.session.commit()
    print(f"已创建 {len(records)} 条物资记录")
    return records

def create_volunteer_assignments(volunteers, events, schedules):
    """创建志愿者任务分配"""
    print("创建志愿者任务分配...")
    assignments = []
    
    positions = ['检录处', '计时组', '计分组', '引导员', '医疗协助', '秩序维护', '摄影', '后勤']
    
    for volunteer in volunteers:
        # 每个志愿者分配1-3个任务
        num_tasks = random.randint(1, 3)
        for _ in range(num_tasks):
            event = random.choice(events)
            # 找到该赛事的赛程，如果没有则使用None
            event_schedules = [s for s in schedules if s.event_id == event.id]
            schedule = random.choice(event_schedules) if event_schedules else None
            
            assignment = VolunteerAssignment(
                volunteer_id=volunteer.id,
                position_name=random.choice(positions),
                event_id=event.id,
                schedule_id=schedule.id if schedule else None,
                task_description=f'负责{event.name}的{random.choice(positions)}工作',
                status=random.choice(['assigned', 'confirmed', 'completed'])
            )
            assignments.append(assignment)
    
    db.session.add_all(assignments)
    db.session.commit()
    print(f"已创建 {len(assignments)} 条志愿者任务")
    return assignments

def create_medical_info():
    """创建医疗点"""
    print("创建医疗点...")
    medical_points = []
    
    locations = [
        {'name': '主医疗站', 'location': '体育馆医务室', 'phone': '120-0001'},
        {'name': '田径场医疗点', 'location': '田径场东侧', 'phone': '120-0002'},
        {'name': '看台医疗点', 'location': '主席台旁', 'phone': '120-0003'},
        {'name': '后勤保障点', 'location': '后勤楼一楼', 'phone': '120-0004'},
    ]
    
    for data in locations:
        point = MedicalInfo(
            name=data['name'],
            location=data['location'],
            phone=data['phone'],
            responsible_person=generate_name(),
            status='active',
            notes='24小时值班'
        )
        medical_points.append(point)
    
    db.session.add_all(medical_points)
    db.session.commit()
    print(f"已创建 {len(medical_points)} 个医疗点")
    return medical_points

def create_emergency_records():
    """创建应急记录"""
    print("创建应急记录...")
    records = []
    
    descriptions = [
        '运动员轻微扭伤',
        '观众中暑',
        '运动员肌肉拉伤',
        '器材故障',
        '运动员低血糖',
        '观众突发疾病',
        '运动员摔倒擦伤',
        '天气突变暂停比赛'
    ]
    
    for i in range(10):
        record = EmergencyRecord(
            incident_time=datetime.now() - timedelta(days=random.randint(1, 30)),
            location=random.choice(['田径场', '体育馆', '看台', '休息区']),
            description=random.choice(descriptions),
            severity=random.choice(['low', 'medium', 'high']),
            handling_status=random.choice(['resolved', 'resolved', 'resolved', 'pending']),
            handler=generate_name(),
            handling_result='已妥善处理' if random.random() > 0.3 else '处理中'
        )
        records.append(record)
    
    db.session.add_all(records)
    db.session.commit()
    print(f"已创建 {len(records)} 条应急记录")
    return records

def create_announcements():
    """创建公告"""
    print("创建公告...")
    announcements = []
    
    announcements_data = [
        {'title': '关于举办2024年春季运动会的通知', 'priority': 'high'},
        {'title': '运动会报名开始啦！', 'priority': 'high'},
        {'title': '运动会赛程安排公告', 'priority': 'normal'},
        {'title': '运动员注意事项', 'priority': 'normal'},
        {'title': '关于运动会期间课程调整的通知', 'priority': 'high'},
        {'title': '志愿者招募公告', 'priority': 'normal'},
        {'title': '运动会闭幕式通知', 'priority': 'normal'},
        {'title': '优秀运动员表彰名单', 'priority': 'normal'},
        {'title': '运动会成绩公告', 'priority': 'high'},
        {'title': '感谢信', 'priority': 'low'},
    ]
    
    for data in announcements_data:
        announcement = Announcement(
            title=data['title'],
            content=f'这是{data["title"]}的详细内容，请大家关注。',
            publisher=random.choice(['体育部', '学生会', '组委会', '教务处']),
            priority=data['priority'],
            is_published=random.choice([True, True, True, False]),
            view_count=random.randint(50, 500)
        )
        announcements.append(announcement)
    
    db.session.add_all(announcements)
    db.session.commit()
    print(f"已创建 {len(announcements)} 条公告")
    return announcements

def main():
    """主函数"""
    with app.app_context():
        print("=" * 60)
        print("体育运动会管理系统 - 数据生成脚本")
        print("=" * 60)
        
        # 清空数据
        clear_data()
        
        # 创建各类用户
        teachers = create_teachers()
        referee_ids = create_referees()
        volunteers_users, volunteers_profiles = create_volunteers()
        athletes_users, athletes_profiles = create_athletes()
        
        # 创建赛事相关数据
        events = create_events()
        events_dict = {e.id: e for e in events}
        schedules = create_schedules(events)
        registrations = create_registrations(athletes_profiles, events)
        results = create_results(schedules, athletes_profiles, events_dict, referee_ids)
        
        # 创建团队
        teams = create_teams()
        
        # 创建物资
        materials = create_materials()
        material_records = create_material_records(materials)
        
        # 创建志愿者任务
        assignments = create_volunteer_assignments(volunteers_profiles, events, schedules)
        
        # 创建医疗相关
        medical_points = create_medical_info()
        emergency_records = create_emergency_records()
        
        # 创建公告
        announcements = create_announcements()
        
        print("=" * 60)
        print("数据生成完成！")
        print("=" * 60)
        print(f"用户数据：")
        print(f"  - 管理员: 1")
        print(f"  - 老师: {len(teachers)}")
        print(f"  - 裁判: {len(referee_ids)}")
        print(f"  - 志愿者: {len(volunteers_users)}")
        print(f"  - 运动员: {len(athletes_users)}")
        print(f"赛事数据：")
        print(f"  - 赛事: {len(events)}")
        print(f"  - 赛程: {len(schedules)}")
        print(f"  - 报名: {len(registrations)}")
        print(f"  - 成绩: {len(results)}")
        print(f"  - 团队: {len(teams)}")
        print(f"  - 物资种类: {len(materials)}")
        print(f"  - 物资记录: {len(material_records)}")
        print(f"  - 志愿者任务: {len(assignments)}")
        print(f"  - 医疗点: {len(medical_points)}")
        print(f"  - 应急记录: {len(emergency_records)}")
        print(f"  - 公告: {len(announcements)}")
        print("=" * 60)
        print("所有用户密码均为: 123456")
        print("=" * 60)

if __name__ == '__main__':
    main()
