from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sports-meet-management-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/sports_meet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ROLE_PERMISSIONS = {
    'admin': ['admin', 'teacher', 'athlete', 'referee', 'volunteer'],
    'referee': ['results', 'schedules'],
    'teacher': ['athletes', 'events', 'schedules', 'results', 'registrations'],
    'athlete': ['registration', 'results', 'profile'],
    'volunteer': ['schedules', 'logistics']
}

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash('您没有权限访问该页面', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50))
    student_id = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def has_permission(self, module):
        return self.role in ROLE_PERMISSIONS and module in ROLE_PERMISSIONS[self.role]

class OperationLog(db.Model):
    __tablename__ = 'operation_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', backref='logs')

class Athlete(db.Model):
    __tablename__ = 'athletes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    class_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    id_card = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(50))
    emergency_phone = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', backref='athlete_profile')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    group_type = db.Column(db.String(50))
    max_participants = db.Column(db.Integer, default=10)
    min_participants = db.Column(db.Integer, default=1)
    location = db.Column(db.String(100))
    registration_start = db.Column(db.DateTime)
    registration_end = db.Column(db.DateTime)
    scoring_rule = db.Column(db.String(50), default='standard')
    points_first = db.Column(db.Integer, default=7)
    points_second = db.Column(db.Integer, default=5)
    points_third = db.Column(db.Integer, default=3)
    is_recordable = db.Column(db.Boolean, default=True)
    unit = db.Column(db.String(20), default='秒')
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')
    created_at = db.Column(db.DateTime, default=db.func.now())

class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    status = db.Column(db.String(20), default='pending')
    review_note = db.Column(db.Text)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.now())

    athlete = db.relationship('Athlete', backref='registrations')
    event = db.relationship('Event', backref='registrations')
    reviewer = db.relationship('User', backref='reviewed_registrations')

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    round_number = db.Column(db.Integer, default=1)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    event = db.relationship('Event', backref='schedules')

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'))
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'))
    rank = db.Column(db.Integer)
    score = db.Column(db.String(50))
    is_record_broken = db.Column(db.Boolean, default=False)
    record_approval_status = db.Column(db.String(20), default='pending')
    remarks = db.Column(db.Text)
    entered_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_final = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    schedule = db.relationship('Schedule', backref='results')
    athlete = db.relationship('Athlete', backref='results')
    entered_by_user = db.relationship('User', backref='entered_results')

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    coach = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    member_count = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())

class TeamScore(db.Model):
    __tablename__ = 'team_scores'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer)

    team = db.relationship('Team', backref='scores')
    event = db.relationship('Event', backref='team_scores')

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    publisher = db.Column(db.String(50))
    priority = db.Column(db.String(20), default='normal')
    is_published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20))
    min_stock = db.Column(db.Integer, default=0)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='normal')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class MaterialInOut(db.Model):
    __tablename__ = 'material_in_out'
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    operation_type = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    material = db.relationship('Material', backref='in_out_records')
    operator = db.relationship('User', backref='material_operations')

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50))
    available_time = db.Column(db.String(200))
    skills = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', backref='volunteer_profile')

class VolunteerAssignment(db.Model):
    __tablename__ = 'volunteer_assignments'
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'))
    position_name = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'))
    task_description = db.Column(db.Text)
    check_in_time = db.Column(db.DateTime)
    check_out_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='assigned')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    volunteer = db.relationship('Volunteer', backref='assignments')
    event = db.relationship('Event', backref='volunteer_assignments')
    schedule = db.relationship('Schedule', backref='volunteer_assignments')

class MedicalInfo(db.Model):
    __tablename__ = 'medical_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    responsible_person = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

class EmergencyRecord(db.Model):
    __tablename__ = 'emergency_records'
    id = db.Column(db.Integer, primary_key=True)
    incident_time = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))
    handling_status = db.Column(db.String(20), default='pending')
    handler = db.Column(db.String(50))
    handling_result = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    resolved_at = db.Column(db.DateTime)

class EventImage(db.Model):
    __tablename__ = 'event_images'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    image_url = db.Column(db.String(200))
    description = db.Column(db.Text)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())

    event = db.relationship('Event', backref='images')
    uploader = db.relationship('User', backref='uploaded_images')

class ScoringRule(db.Model):
    __tablename__ = 'scoring_rules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rule_type = db.Column(db.String(50))
    points_json = db.Column(db.Text)
    is_default = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def log_operation(action, details=''):
    if current_user.is_authenticated:
        log = OperationLog(
            user_id=current_user.id,
            action=action,
            details=details,
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.is_active and user.check_password(password):
            user.last_login = datetime.now()
            db.session.commit()
            login_user(user)
            log_operation('login', f'用户登录: {user.username}')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.role == 'referee':
                return redirect(url_for('referee_dashboard'))
            elif user.role == 'volunteer':
                return redirect(url_for('volunteer_dashboard'))
            else:
                return redirect(url_for('athlete_dashboard'))
        flash('用户名或密码错误', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        role = request.form.get('role', 'athlete')
        student_id = request.form.get('student_id')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return redirect(url_for('register'))

        user = User(username=username, role=role, name=name, student_id=student_id, phone=phone, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        if role == 'athlete' and student_id:
            athlete = Athlete(user_id=user.id, name=name, student_id=student_id, phone=phone)
            db.session.add(athlete)
            db.session.commit()

        flash('注册成功，请等待审核', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    log_operation('logout', f'用户登出: {current_user.username}')
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('login'))

    athlete_count = Athlete.query.count()
    event_count = Event.query.count()
    registration_count = Registration.query.count()
    announcement_count = Announcement.query.filter_by(is_published=True).count()
    team_count = Team.query.count()
    volunteer_count = Volunteer.query.count()
    pending_registrations = Registration.query.filter_by(status='pending').count()
    material_low_stock = Material.query.filter(Material.quantity <= Material.min_stock).count()

    recent_athletes = Athlete.query.order_by(Athlete.created_at.desc()).limit(5).all()
    recent_announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.created_at.desc()).limit(3).all()
    recent_schedules = Schedule.query.order_by(Schedule.start_time.desc()).limit(5).all()
    recent_logs = OperationLog.query.order_by(OperationLog.created_at.desc()).limit(10).all()

    teams = Team.query.order_by(Team.total_score.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                         athlete_count=athlete_count,
                         event_count=event_count,
                         registration_count=registration_count,
                         announcement_count=announcement_count,
                         team_count=team_count,
                         volunteer_count=volunteer_count,
                         pending_registrations=pending_registrations,
                         material_low_stock=material_low_stock,
                         recent_athletes=recent_athletes,
                         recent_announcements=recent_announcements,
                         recent_schedules=recent_schedules,
                         recent_logs=recent_logs,
                         teams=teams)

@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))

    athlete_count = Athlete.query.count()
    event_count = Event.query.count()
    registration_count = Registration.query.count()
    pending_registrations = Registration.query.filter_by(status='pending').count()
    recent_schedules = Schedule.query.order_by(Schedule.start_time.desc()).limit(5).all()

    return render_template('teacher/dashboard.html',
                         athlete_count=athlete_count,
                         event_count=event_count,
                         registration_count=registration_count,
                         pending_registrations=pending_registrations,
                         recent_schedules=recent_schedules)

@app.route('/referee/dashboard')
@login_required
def referee_dashboard():
    if current_user.role != 'referee':
        return redirect(url_for('login'))

    today = datetime.now().date()
    today_schedules = Schedule.query.filter(
        db.func.date(Schedule.start_time) == today
    ).all()

    pending_results = Result.query.filter_by(is_final=False).count()

    return render_template('referee/dashboard.html',
                         today_schedules=today_schedules,
                         pending_results=pending_results)

@app.route('/volunteer/dashboard')
@login_required
def volunteer_dashboard():
    if current_user.role != 'volunteer':
        return redirect(url_for('login'))

    volunteer = Volunteer.query.filter_by(user_id=current_user.id).first()
    my_assignments = []
    if volunteer:
        my_assignments = VolunteerAssignment.query.filter_by(volunteer_id=volunteer.id).all()

    return render_template('volunteer/dashboard.html',
                         volunteer=volunteer,
                         my_assignments=my_assignments)

@app.route('/athlete/dashboard')
@login_required
def athlete_dashboard():
    if current_user.role not in ['athlete', 'athlete_pending']:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif current_user.role == 'referee':
            return redirect(url_for('referee_dashboard'))
        elif current_user.role == 'volunteer':
            return redirect(url_for('volunteer_dashboard'))

    athlete = Athlete.query.filter_by(student_id=current_user.student_id).first()
    my_registrations = []
    my_results = []
    if athlete:
        my_registrations = Registration.query.filter_by(athlete_id=athlete.id).all()
        my_results = Result.query.filter_by(athlete_id=athlete.id).all()

    recent_announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.created_at.desc()).limit(3).all()
    return render_template('athlete/dashboard.html',
                         recent_announcements=recent_announcements,
                         my_registrations=my_registrations,
                         my_results=my_results)

@app.route('/athletes')
@login_required
def athletes():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('athlete_dashboard'))
    all_athletes = Athlete.query.all()
    return render_template('admin/athletes.html', athletes=all_athletes)

@app.route('/athletes/add', methods=['POST'])
@login_required
def add_athlete():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    gender = request.form.get('gender')
    class_name = request.form.get('class_name')
    phone = request.form.get('phone')
    id_card = request.form.get('id_card')
    emergency_contact = request.form.get('emergency_contact')
    emergency_phone = request.form.get('emergency_phone')

    if Athlete.query.filter_by(student_id=student_id).first():
        flash('学号已存在', 'danger')
        return redirect(url_for('athletes'))

    athlete = Athlete(name=name, student_id=student_id, gender=gender, class_name=class_name,
                     phone=phone, id_card=id_card, emergency_contact=emergency_contact,
                     emergency_phone=emergency_phone)
    db.session.add(athlete)
    db.session.commit()
    log_operation('add_athlete', f'添加运动员: {name}')
    flash('运动员添加成功', 'success')
    return redirect(url_for('athletes'))

@app.route('/athletes/delete/<int:id>')
@login_required
def delete_athlete(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    athlete = Athlete.query.get_or_404(id)
    db.session.delete(athlete)
    db.session.commit()
    log_operation('delete_athlete', f'删除运动员ID: {id}')
    flash('运动员删除成功', 'success')
    return redirect(url_for('athletes'))

@app.route('/athletes/edit/<int:id>', methods=['POST'])
@login_required
def edit_athlete(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    athlete = Athlete.query.get_or_404(id)
    athlete.name = request.form.get('name')
    athlete.gender = request.form.get('gender')
    athlete.class_name = request.form.get('class_name')
    athlete.phone = request.form.get('phone')
    athlete.emergency_contact = request.form.get('emergency_contact')
    athlete.emergency_phone = request.form.get('emergency_phone')
    db.session.commit()
    log_operation('edit_athlete', f'编辑运动员: {athlete.name}')
    flash('运动员信息更新成功', 'success')
    return redirect(url_for('athletes'))

@app.route('/athletes/verify/<int:id>')
@login_required
def verify_athlete(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    athlete = Athlete.query.get_or_404(id)
    athlete.is_verified = True
    db.session.commit()
    flash('运动员审核通过', 'success')
    return redirect(url_for('athletes'))

@app.route('/events')
@login_required
def events():
    if current_user.role not in ['admin', 'teacher', 'referee']:
        return redirect(url_for('athlete_dashboard'))
    all_events = Event.query.all()
    return render_template('admin/events.html', events=all_events)

@app.route('/events/add', methods=['POST'])
@login_required
def add_event():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    name = request.form.get('name')
    event_type = request.form.get('event_type')
    gender = request.form.get('gender')
    group_type = request.form.get('group_type')
    max_participants = request.form.get('max_participants')
    min_participants = request.form.get('min_participants', 1)
    location = request.form.get('location')
    registration_start_str = request.form.get('registration_start')
    registration_end_str = request.form.get('registration_end')
    scoring_rule = request.form.get('scoring_rule', 'standard')
    points_first = request.form.get('points_first', 7)
    points_second = request.form.get('points_second', 5)
    points_third = request.form.get('points_third', 3)
    unit = request.form.get('unit', '秒')
    is_recordable = request.form.get('is_recordable') == 'on'
    description = request.form.get('description')

    registration_start = datetime.strptime(registration_start_str, '%Y-%m-%dT%H:%M') if registration_start_str else None
    registration_end = datetime.strptime(registration_end_str, '%Y-%m-%dT%H:%M') if registration_end_str else None

    event = Event(name=name, event_type=event_type, gender=gender, group_type=group_type,
                 max_participants=max_participants, min_participants=min_participants,
                 location=location, registration_start=registration_start,
                 registration_end=registration_end, scoring_rule=scoring_rule,
                 points_first=points_first, points_second=points_second,
                 points_third=points_third, unit=unit, is_recordable=is_recordable,
                 description=description)
    db.session.add(event)
    db.session.commit()
    log_operation('add_event', f'添加项目: {name}')
    flash('项目添加成功', 'success')
    return redirect(url_for('events'))

@app.route('/events/delete/<int:id>')
@login_required
def delete_event(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    log_operation('delete_event', f'删除项目ID: {id}')
    flash('项目删除成功', 'success')
    return redirect(url_for('events'))

@app.route('/events/edit/<int:id>', methods=['POST'])
@login_required
def edit_event(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    event = Event.query.get_or_404(id)
    event.name = request.form.get('name')
    event.event_type = request.form.get('event_type')
    event.gender = request.form.get('gender')
    event.group_type = request.form.get('group_type')
    event.max_participants = request.form.get('max_participants')
    event.min_participants = request.form.get('min_participants')
    event.location = request.form.get('location')
    event.scoring_rule = request.form.get('scoring_rule')
    event.points_first = request.form.get('points_first')
    event.points_second = request.form.get('points_second')
    event.points_third = request.form.get('points_third')
    event.unit = request.form.get('unit')
    event.is_recordable = request.form.get('is_recordable') == 'on'
    event.description = request.form.get('description')
    db.session.commit()
    log_operation('edit_event', f'编辑项目: {event.name}')
    flash('项目信息更新成功', 'success')
    return redirect(url_for('events'))

@app.route('/events/publish/<int:id>')
@login_required
def publish_event(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    event = Event.query.get_or_404(id)
    event.status = 'published'
    db.session.commit()
    flash('项目已发布', 'success')
    return redirect(url_for('events'))

@app.route('/registration')
@login_required
def registration():
    if current_user.role != 'athlete':
        return redirect(url_for('admin_dashboard'))

    all_events = Event.query.filter_by(status='published').all()
    my_registrations = []
    athlete = None

    athlete = Athlete.query.filter_by(student_id=current_user.student_id).first()
    if athlete:
        my_registrations = Registration.query.filter_by(athlete_id=athlete.id).all()

    return render_template('athlete/registration.html', events=all_events, registrations=my_registrations, athlete=athlete)

@app.route('/registration/register', methods=['POST'])
@login_required
def register_event():
    if current_user.role != 'athlete':
        return redirect(url_for('login'))

    athlete = Athlete.query.filter_by(student_id=current_user.student_id).first()
    if not athlete:
        flash('请先完善个人信息', 'warning')
        return redirect(url_for('registration'))

    event_id = request.form.get('event_id')
    event = Event.query.get(event_id)

    existing = Registration.query.filter_by(athlete_id=athlete.id, event_id=event_id).first()
    if existing:
        flash('您已报名该项目', 'warning')
        return redirect(url_for('registration'))

    current_count = Registration.query.filter_by(event_id=event_id, status='approved').count()
    if event and current_count >= event.max_participants:
        flash('该项目报名人数已满', 'warning')
        return redirect(url_for('registration'))

    reg = Registration(athlete_id=athlete.id, event_id=event_id, status='pending')
    db.session.add(reg)
    db.session.commit()
    log_operation('register_event', f'报名项目ID: {event_id}')

    all_events = Event.query.filter_by(status='published').all()
    my_registrations = Registration.query.filter_by(athlete_id=athlete.id).all()
    return render_template('athlete/registration.html', events=all_events, registrations=my_registrations, athlete=athlete, show_success_modal=True)

@app.route('/registration/cancel/<int:id>')
@login_required
def cancel_registration(id):
    if current_user.role != 'athlete':
        return redirect(url_for('login'))

    registration = Registration.query.get_or_404(id)
    athlete = Athlete.query.filter_by(student_id=current_user.student_id).first()

    if registration.athlete_id != athlete.id:
        flash('无权限取消此报名', 'danger')
        return redirect(url_for('registration'))

    db.session.delete(registration)
    db.session.commit()
    log_operation('cancel_registration', f'取消报名ID: {id}')
    flash('取消报名成功', 'success')
    return redirect(url_for('registration'))

@app.route('/registrations')
@login_required
def all_registrations():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('athlete_dashboard'))

    status_filter = request.args.get('status', 'all')
    query = Registration.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)

    registrations = query.order_by(Registration.created_at.desc()).all()
    return render_template('admin/registrations.html', registrations=registrations, status_filter=status_filter)

@app.route('/registrations/review/<int:id>', methods=['POST'])
@login_required
def review_registration(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))

    registration = Registration.query.get_or_404(id)
    action = request.form.get('action')
    review_note = request.form.get('review_note')

    if action == 'approve':
        registration.status = 'approved'
        flash('报名已通过', 'success')
    elif action == 'reject':
        registration.status = 'rejected'
        registration.review_note = review_note
        flash('报名已驳回', 'success')

    registration.reviewed_by = current_user.id
    registration.reviewed_at = datetime.now()
    db.session.commit()
    log_operation('review_registration', f'审核报名ID: {id}, 结果: {action}')
    return redirect(url_for('all_registrations'))

@app.route('/registrations/batch_review', methods=['POST'])
@login_required
def batch_review_registration():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))

    registration_ids = request.form.getlist('registration_ids')
    action = request.form.get('action')

    for reg_id in registration_ids:
        registration = Registration.query.get(int(reg_id))
        if registration:
            registration.status = 'approved' if action == 'approve' else 'rejected'
            registration.reviewed_by = current_user.id
            registration.reviewed_at = datetime.now()

    db.session.commit()
    log_operation('batch_review', f'批量审核{len(registration_ids)}条报名')
    flash(f'已批量审核{len(registration_ids)}条报名', 'success')
    return redirect(url_for('all_registrations'))

@app.route('/schedules')
@login_required
def schedules():
    if current_user.role not in ['admin', 'teacher', 'referee', 'volunteer', 'athlete']:
        return redirect(url_for('login'))
    all_schedules = Schedule.query.all()
    all_events = Event.query.all()

    my_schedules = []
    if current_user.role == 'athlete':
        athlete = Athlete.query.filter_by(user_id=current_user.id).first()
        if athlete:
            my_regs = Registration.query.filter_by(athlete_id=athlete.id, status='approved').all()
            for reg in my_regs:
                schedule = Schedule.query.filter_by(event_id=reg.event_id).first()
                if schedule:
                    my_schedules.append(schedule)

    return render_template('admin/schedules.html', schedules=all_schedules, events=all_events, current_role=current_user.role, my_schedules=my_schedules)

@app.route('/schedules/add', methods=['POST'])
@login_required
def add_schedule():
    if current_user.role not in ['admin', 'teacher', 'referee']:
        return redirect(url_for('login'))
    event_id = request.form.get('event_id')
    round_number = request.form.get('round_number', 1)
    start_time_str = request.form.get('start_time')
    end_time_str = request.form.get('end_time')
    location = request.form.get('location')
    notes = request.form.get('notes')

    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M') if start_time_str else None
    end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M') if end_time_str else None

    schedule = Schedule(event_id=event_id, round_number=round_number, start_time=start_time,
                      end_time=end_time, location=location, notes=notes)
    db.session.add(schedule)
    db.session.commit()
    log_operation('add_schedule', f'添加赛程ID: {schedule.id}')
    flash('赛程添加成功', 'success')
    return redirect(url_for('schedules'))

@app.route('/schedules/delete/<int:id>')
@login_required
def delete_schedule(id):
    if current_user.role not in ['admin', 'teacher', 'referee']:
        return redirect(url_for('login'))
    schedule = Schedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    log_operation('delete_schedule', f'删除赛程ID: {id}')
    flash('赛程删除成功', 'success')
    return redirect(url_for('schedules'))

@app.route('/schedules/edit/<int:id>', methods=['POST'])
@login_required
def edit_schedule(id):
    if current_user.role not in ['admin', 'teacher', 'referee']:
        return redirect(url_for('login'))
    schedule = Schedule.query.get_or_404(id)
    schedule.event_id = request.form.get('event_id')
    start_time_str = request.form.get('start_time')
    end_time_str = request.form.get('end_time')
    schedule.location = request.form.get('location')
    schedule.status = request.form.get('status')
    schedule.notes = request.form.get('notes')
    schedule.round_number = request.form.get('round_number', 1)

    if start_time_str:
        schedule.start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
    if end_time_str:
        schedule.end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

    db.session.commit()
    log_operation('edit_schedule', f'编辑赛程ID: {id}')
    flash('赛程信息更新成功', 'success')
    return redirect(url_for('schedules'))

@app.route('/results')
@login_required
def results():
    if current_user.role not in ['admin', 'teacher', 'referee', 'athlete']:
        return redirect(url_for('login'))

    event_id = request.args.get('event_id')
    query = Result.query

    if event_id:
        schedule_ids = [s.id for s in Schedule.query.filter_by(event_id=event_id).all()]
        query = query.filter(Result.schedule_id.in_(schedule_ids))

    all_results = query.all()
    all_schedules = Schedule.query.all()
    all_athletes = Athlete.query.all()
    all_events = Event.query.all()

    results_by_event = {}
    for result in all_results:
        if result.schedule and result.schedule.event:
            event_id_key = result.schedule.event.id
            if event_id_key not in results_by_event:
                results_by_event[event_id_key] = []
            results_by_event[event_id_key].append(result)

    # 对每个赛事的成绩按实际成绩排序，并重新计算排名
    for event_id in results_by_event:
        event_results = results_by_event[event_id]
        if not event_results:
            continue
        
        # 获取赛事单位
        event = event_results[0].schedule.event if event_results[0].schedule else None
        unit = event.unit if event else ''
        
        # 定义成绩排序函数（按照score字段直接排序）
        def score_key(result):
            if not result.score:
                return (True, '')
            
            score_str = result.score
            # 直接按照score字段字符串排序
            return (False, score_str)
        
        # 按成绩排序
        event_results.sort(key=score_key)
        
        # 重新计算排名
        for i, result in enumerate(event_results, 1):
            result.rank = i
    
    # 保存排名到数据库
    db.session.commit()
    
    # 按rank正序排序，无名次的排最后
    for event_id in results_by_event:
        event_results = results_by_event[event_id]
        if not event_results:
            continue
        
        # 按rank正序排序，rank为空的排最后
        event_results.sort(key=lambda x: x.rank if x.rank else 999)

    return render_template('admin/results.html',
                         results=all_results,
                         schedules=all_schedules,
                         athletes=all_athletes,
                         events=all_events,
                         results_by_event=results_by_event,
                         selected_event=event_id,
                         current_role=current_user.role)

@app.route('/result/<int:id>')
@login_required
def result_detail(id):
    result = Result.query.get_or_404(id)
    return render_template('admin/result_detail.html', result=result)

@app.route('/results/add', methods=['POST'])
@login_required
def add_result():
    if current_user.role not in ['admin', 'teacher', 'referee']:
        return redirect(url_for('login'))
    schedule_id = request.form.get('schedule_id')
    athlete_id = request.form.get('athlete_id')
    score = request.form.get('score')
    is_record_broken = request.form.get('is_record_broken') == 'on'
    remarks = request.form.get('remarks')

    # 创建成绩记录（不设置rank，稍后自动计算）
    result = Result(schedule_id=schedule_id, athlete_id=athlete_id, rank=None, score=score,
                   is_record_broken=is_record_broken, remarks=remarks,
                   entered_by=current_user.id, is_final=False)
    db.session.add(result)
    db.session.commit()
    
    # 重新计算该赛事的所有成绩排名
    schedule = Schedule.query.get(schedule_id)
    if schedule and schedule.event:
        event_id = schedule.event.id
        # 获取该赛事的所有成绩
        event_results = Result.query.join(Schedule).filter(Schedule.event_id == event_id).all()
        
        # 按成绩排序并重新计算排名
        if event_results:
            unit = schedule.event.unit
            
            def score_key(result):
                if not result.score:
                    return (True, '')
                
                score_str = result.score
                # 直接按照score字段字符串排序
                return (False, score_str)
            
            # 按成绩排序
            event_results.sort(key=score_key)
            
            # 重新计算排名
            for i, r in enumerate(event_results, 1):
                r.rank = i
            
            db.session.commit()

    log_operation('add_result', f'录入成绩: 运动员ID-{athlete_id}, 项目ID-{schedule_id}')
    flash('成绩录入成功，排名已自动计算', 'success')
    return redirect(url_for('results'))

@app.route('/results/edit/<int:id>', methods=['POST'])
@login_required
def edit_result(id):
    if current_user.role not in ['admin', 'teacher', 'referee']:
        return redirect(url_for('login'))
    result = Result.query.get_or_404(id)
    result.score = request.form.get('score')
    result.is_record_broken = request.form.get('is_record_broken') == 'on'
    result.remarks = request.form.get('remarks')
    result.updated_at = datetime.now()
    db.session.commit()
    
    # 重新计算该赛事的所有成绩排名
    if result.schedule and result.schedule.event:
        event_id = result.schedule.event.id
        # 获取该赛事的所有成绩
        event_results = Result.query.join(Schedule).filter(Schedule.event_id == event_id).all()
        
        # 按成绩排序并重新计算排名
        if event_results:
            unit = result.schedule.event.unit
            
            def score_key(result):
                if not result.score:
                    return (True, '')
                
                score_str = result.score
                # 直接按照score字段字符串排序
                return (False, score_str)
            
            # 按成绩排序
            event_results.sort(key=score_key)
            
            # 重新计算排名
            for i, r in enumerate(event_results, 1):
                r.rank = i
            
            db.session.commit()

    log_operation('edit_result', f'编辑成绩ID: {id}')
    flash('成绩更新成功，排名已自动重新计算', 'success')
    return redirect(url_for('results'))

@app.route('/results/confirm/<int:id>')
@login_required
def confirm_result(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    result = Result.query.get_or_404(id)
    result.is_final = True
    db.session.commit()
    log_operation('confirm_result', f'确认成绩ID: {id}')
    flash('成绩已确认为最终成绩', 'success')
    return redirect(url_for('results'))

@app.route('/results/delete/<int:id>')
@login_required
def delete_result(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    result = Result.query.get_or_404(id)
    schedule = result.schedule
    db.session.delete(result)
    db.session.commit()
    
    # 重新计算该赛事的所有成绩排名
    if schedule and schedule.event:
        event_id = schedule.event.id
        # 获取该赛事的所有成绩
        event_results = Result.query.join(Schedule).filter(Schedule.event_id == event_id).all()
        
        # 按成绩排序并重新计算排名
        if event_results:
            unit = schedule.event.unit
            
            def score_key(result):
                if not result.score:
                    return (True, '')
                
                score_str = result.score
                # 直接按照score字段字符串排序
                return (False, score_str)
            
            # 按成绩排序
            event_results.sort(key=score_key)
            
            # 重新计算排名
            for i, r in enumerate(event_results, 1):
                r.rank = i
            
            db.session.commit()

    log_operation('delete_result', f'删除成绩ID: {id}')
    flash('成绩删除成功，排名已自动重新计算', 'success')
    return redirect(url_for('results'))

@app.route('/results/export')
@login_required
def export_results():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))

    import csv
    from flask import make_response

    results = Result.query.all()
    response = make_response()
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=results_{datetime.now().strftime("%Y%m%d")}.csv'

    writer = csv.writer(response)
    writer.writerow(['排名', '运动员', '项目', '成绩', '破纪录', '录入时间'])

    for result in results:
        writer.writerow([
            result.rank or '',
            result.athlete.name if result.athlete else '',
            result.schedule.event.name if result.schedule and result.schedule.event else '',
            result.score or '',
            '是' if result.is_record_broken else '否',
            result.created_at.strftime('%Y-%m-%d %H:%M') if result.created_at else ''
        ])

    log_operation('export_results', '导出成绩数据')
    return response

@app.route('/results/ranking')
@login_required
def ranking():
    if current_user.role not in ['admin', 'teacher', 'referee', 'athlete']:
        return redirect(url_for('login'))

    all_athletes = Athlete.query.all()
    athlete_scores = {}

    for athlete in all_athletes:
        results = Result.query.filter_by(athlete_id=athlete.id, is_final=True).all()
        total_score = 0
        gold = silver = bronze = 0
        for result in results:
            if result.rank == 1:
                total_score += result.schedule.event.points_first if result.schedule and result.schedule.event else 7
                gold += 1
            elif result.rank == 2:
                total_score += result.schedule.event.points_second if result.schedule and result.schedule.event else 5
                silver += 1
            elif result.rank == 3:
                total_score += result.schedule.event.points_third if result.schedule and result.schedule.event else 3
                bronze += 1

        if total_score > 0:
            athlete_scores[athlete.id] = {
                'name': athlete.name,
                'class_name': athlete.class_name,
                'total_score': total_score,
                'gold': gold,
                'silver': silver,
                'bronze': bronze
            }

    sorted_athletes = sorted(athlete_scores.items(), key=lambda x: x[1]['total_score'], reverse=True)

    teams = Team.query.order_by(Team.total_score.desc()).all()

    return render_template('admin/ranking.html',
                         sorted_athletes=sorted_athletes[:20],
                         teams=teams)

@app.route('/teams')
@login_required
def teams():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('athlete_dashboard'))
    all_teams = Team.query.all()
    return render_template('admin/teams.html', teams=all_teams)

@app.route('/teams/add', methods=['POST'])
@login_required
def add_team():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    name = request.form.get('name')
    code = request.form.get('code')
    coach = request.form.get('coach')
    contact_phone = request.form.get('contact_phone')

    team = Team(name=name, code=code, coach=coach, contact_phone=contact_phone)
    db.session.add(team)
    db.session.commit()
    flash('队伍添加成功', 'success')
    return redirect(url_for('teams'))

@app.route('/teams/edit/<int:id>', methods=['POST'])
@login_required
def edit_team(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    team = Team.query.get_or_404(id)
    team.name = request.form.get('name')
    team.code = request.form.get('code')
    team.coach = request.form.get('coach')
    team.contact_phone = request.form.get('contact_phone')
    team.total_score = int(request.form.get('total_score') or 0)
    db.session.commit()
    flash('队伍信息更新成功', 'success')
    return redirect(url_for('teams'))

@app.route('/teams/delete/<int:id>')
@login_required
def delete_team(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    flash('队伍删除成功', 'success')
    return redirect(url_for('teams'))

@app.route('/teams/calculate_scores/<int:id>')
@login_required
def calculate_team_scores(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))

    team = Team.query.get_or_404(id)
    total_score = 0

    all_athletes = Athlete.query.all()
    athlete_class_map = {}
    for athlete in all_athletes:
        if athlete.class_name and team.code in athlete.class_name:
            athlete_class_map[athlete.id] = athlete

    if athlete_class_map:
        athlete_ids = list(athlete_class_map.keys())
        results = Result.query.filter(
            Result.athlete_id.in_(athlete_ids),
            Result.is_final == True
        ).all()

        for result in results:
            if result.schedule and result.schedule.event:
                event = result.schedule.event
                if result.rank == 1:
                    total_score += event.points_first if event.points_first else 7
                elif result.rank == 2:
                    total_score += event.points_second if event.points_second else 5
                elif result.rank == 3:
                    total_score += event.points_third if event.points_third else 3

    team.total_score = total_score
    db.session.commit()
    flash(f'队伍{team.name}已更新为{total_score}分', 'success')
    return redirect(url_for('teams'))

@app.route('/materials')
@login_required
def materials():
    if current_user.role not in ['admin', 'teacher', 'volunteer']:
        return redirect(url_for('athlete_dashboard'))
    all_materials = Material.query.all()
    return render_template('admin/materials.html', materials=all_materials)

@app.route('/materials/add', methods=['POST'])
@login_required
def add_material():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    name = request.form.get('name')
    category = request.form.get('category')
    quantity = request.form.get('quantity')
    unit = request.form.get('unit')
    min_stock = request.form.get('min_stock', 0)
    location = request.form.get('location')
    description = request.form.get('description')

    material = Material(name=name, category=category, quantity=quantity, unit=unit,
                       min_stock=min_stock, location=location, description=description)
    db.session.add(material)
    db.session.commit()
    flash('物资添加成功', 'success')
    return redirect(url_for('materials'))

@app.route('/materials/edit/<int:id>', methods=['POST'])
@login_required
def edit_material(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    material = Material.query.get_or_404(id)
    material.name = request.form.get('name')
    material.category = request.form.get('category')
    material.quantity = request.form.get('quantity')
    material.unit = request.form.get('unit')
    material.min_stock = request.form.get('min_stock')
    material.location = request.form.get('location')
    material.description = request.form.get('description')
    db.session.commit()
    flash('物资信息更新成功', 'success')
    return redirect(url_for('materials'))

@app.route('/materials/delete/<int:id>')
@login_required
def delete_material(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    material = Material.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash('物资删除成功', 'success')
    return redirect(url_for('materials'))

@app.route('/materials/in/<int:id>', methods=['POST'])
@login_required
def material_in(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    material = Material.query.get_or_404(id)
    quantity = int(request.form.get('quantity'))
    notes = request.form.get('notes')

    material.quantity += quantity
    record = MaterialInOut(material_id=id, operation_type='in', quantity=quantity,
                          operator_id=current_user.id, notes=notes)
    db.session.add(record)
    db.session.commit()
    flash(f'入库{quantity}{material.unit}', 'success')
    return redirect(url_for('materials'))

@app.route('/materials/out/<int:id>', methods=['POST'])
@login_required
def material_out(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    material = Material.query.get_or_404(id)
    quantity = int(request.form.get('quantity'))
    notes = request.form.get('notes')

    if material.quantity < quantity:
        flash('库存不足', 'danger')
        return redirect(url_for('materials'))

    material.quantity -= quantity
    record = MaterialInOut(material_id=id, operation_type='out', quantity=quantity,
                          operator_id=current_user.id, notes=notes)
    db.session.add(record)
    db.session.commit()
    flash(f'出库{quantity}{material.unit}', 'success')
    return redirect(url_for('materials'))

@app.route('/volunteers')
@login_required
def volunteers():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('athlete_dashboard'))
    all_volunteers = Volunteer.query.all()
    return render_template('admin/volunteers.html', volunteers=all_volunteers)

@app.route('/volunteers/add', methods=['POST'])
@login_required
def add_volunteer():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    phone = request.form.get('phone')
    department = request.form.get('department')
    available_time = request.form.get('available_time')
    skills = request.form.get('skills')

    volunteer = Volunteer(name=name, student_id=student_id, phone=phone,
                        department=department, available_time=available_time,
                        skills=skills)
    db.session.add(volunteer)
    db.session.commit()
    flash('志愿者添加成功', 'success')
    return redirect(url_for('volunteers'))

@app.route('/volunteers/edit/<int:id>', methods=['POST'])
@login_required
def edit_volunteer(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    volunteer = Volunteer.query.get_or_404(id)
    volunteer.name = request.form.get('name')
    volunteer.student_id = request.form.get('student_id')
    volunteer.phone = request.form.get('phone')
    volunteer.department = request.form.get('department')
    volunteer.available_time = request.form.get('available_time')
    volunteer.skills = request.form.get('skills')
    volunteer.status = request.form.get('status')
    db.session.commit()
    flash('志愿者信息更新成功', 'success')
    return redirect(url_for('volunteers'))

@app.route('/volunteers/delete/<int:id>')
@login_required
def delete_volunteer(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    volunteer = Volunteer.query.get_or_404(id)
    db.session.delete(volunteer)
    db.session.commit()
    flash('志愿者删除成功', 'success')
    return redirect(url_for('volunteers'))

@app.route('/volunteer_assignments')
@login_required
def volunteer_assignments():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('athlete_dashboard'))
    assignments = VolunteerAssignment.query.all()
    volunteers = Volunteer.query.all()
    events = Event.query.all()
    schedules = Schedule.query.all()
    return render_template('admin/volunteer_assignments.html',
                         assignments=assignments,
                         volunteers=volunteers,
                         events=events,
                         schedules=schedules)

@app.route('/volunteer_assignments/add', methods=['POST'])
@login_required
def add_volunteer_assignment():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    volunteer_id = request.form.get('volunteer_id')
    position_name = request.form.get('position_name')
    event_id = request.form.get('event_id')
    schedule_id = request.form.get('schedule_id')
    task_description = request.form.get('task_description')

    assignment = VolunteerAssignment(volunteer_id=volunteer_id, position_name=position_name,
                                     event_id=event_id, schedule_id=schedule_id,
                                     task_description=task_description)
    db.session.add(assignment)
    db.session.commit()
    flash('任务分配成功', 'success')
    return redirect(url_for('volunteer_assignments'))

@app.route('/volunteer_assignments/checkin/<int:id>')
@login_required
def volunteer_checkin(id):
    assignment = VolunteerAssignment.query.get_or_404(id)
    assignment.check_in_time = datetime.now()
    assignment.status = 'checked_in'
    db.session.commit()
    flash('签到成功', 'success')
    return redirect(url_for('volunteer_assignments'))

@app.route('/volunteer_assignments/checkout/<int:id>')
@login_required
def volunteer_checkout(id):
    assignment = VolunteerAssignment.query.get_or_404(id)
    assignment.check_out_time = datetime.now()
    assignment.status = 'completed'
    db.session.commit()
    flash('签退成功', 'success')
    return redirect(url_for('volunteer_assignments'))

@app.route('/medical')
@login_required
def medical_info():
    if current_user.role not in ['admin', 'teacher', 'volunteer', 'athlete']:
        return redirect(url_for('login'))
    medical_info_list = MedicalInfo.query.all()
    return render_template('admin/medical.html', medical_info=medical_info_list, current_role=current_user.role)

@app.route('/medical/add', methods=['POST'])
@login_required
def add_medical_info():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    name = request.form.get('name')
    location = request.form.get('location')
    phone = request.form.get('phone')
    responsible_person = request.form.get('responsible_person')
    notes = request.form.get('notes')

    medical = MedicalInfo(name=name, location=location, phone=phone,
                        responsible_person=responsible_person, notes=notes)
    db.session.add(medical)
    db.session.commit()
    flash('医疗点添加成功', 'success')
    return redirect(url_for('medical_info'))

@app.route('/medical/delete/<int:id>')
@login_required
def delete_medical_info(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    medical = MedicalInfo.query.get_or_404(id)
    db.session.delete(medical)
    db.session.commit()
    flash('医疗点删除成功', 'success')
    return redirect(url_for('medical_info'))

@app.route('/medical/edit/<int:id>', methods=['POST'])
@login_required
def edit_medical_info(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    medical = MedicalInfo.query.get_or_404(id)
    medical.name = request.form.get('name')
    medical.location = request.form.get('location')
    medical.phone = request.form.get('phone')
    medical.responsible_person = request.form.get('responsible_person')
    medical.notes = request.form.get('notes')
    db.session.commit()
    flash('医疗点信息更新成功', 'success')
    return redirect(url_for('medical_info'))

@app.route('/emergency')
@login_required
def emergency_records():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('athlete_dashboard'))
    records = EmergencyRecord.query.order_by(EmergencyRecord.incident_time.desc()).all()
    return render_template('admin/emergency.html', records=records)

@app.route('/emergency/add', methods=['POST'])
@login_required
def add_emergency_record():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    incident_time_str = request.form.get('incident_time')
    location = request.form.get('location')
    description = request.form.get('description')
    severity = request.form.get('severity')
    handler = request.form.get('handler')
    handling_result = request.form.get('handling_result')
    handling_status = request.form.get('handling_status')

    incident_time = datetime.strptime(incident_time_str, '%Y-%m-%dT%H:%M') if incident_time_str else datetime.now()

    record = EmergencyRecord(incident_time=incident_time, location=location,
                          description=description, severity=severity,
                          handler=handler, handling_result=handling_result,
                          handling_status=handling_status)
    if handling_status == 'resolved':
        record.resolved_at = datetime.now()

    db.session.add(record)
    db.session.commit()
    flash('应急记录添加成功', 'success')
    return redirect(url_for('emergency_records'))

@app.route('/emergency/resolve/<int:id>')
@login_required
def resolve_emergency(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    record = EmergencyRecord.query.get_or_404(id)
    record.handling_status = 'resolved'
    record.resolved_at = datetime.now()
    db.session.commit()
    flash('事件已标记为已处理', 'success')
    return redirect(url_for('emergency_records'))

@app.route('/announcements')
@login_required
def announcements():
    all_announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.created_at.desc()).all()
    for ann in all_announcements:
        ann.view_count += 1
        db.session.commit()
    return render_template('announcements.html', announcements=all_announcements)

@app.route('/announcement/<int:id>')
@login_required
def announcement_detail(id):
    announcement = Announcement.query.get_or_404(id)
    return render_template('announcement_detail.html', announcement=announcement)

@app.route('/admin/announcements')
@login_required
def admin_announcements():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    all_announcements = Announcement.query.all()
    return render_template('admin/announcements.html', announcements=all_announcements)

@app.route('/admin/announcements/add', methods=['POST'])
@login_required
def add_announcement():
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    title = request.form.get('title')
    content = request.form.get('content')
    is_published = request.form.get('is_published') == 'on'
    priority = request.form.get('priority', 'normal')

    announcement = Announcement(title=title, content=content, publisher=current_user.name,
                             is_published=is_published, priority=priority)
    db.session.add(announcement)
    db.session.commit()
    log_operation('add_announcement', f'发布公告: {title}')
    flash('公告发布成功', 'success')
    return redirect(url_for('admin_announcements'))

@app.route('/admin/announcements/publish/<int:id>')
@login_required
def publish_announcement(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    announcement = Announcement.query.get_or_404(id)
    announcement.is_published = True
    db.session.commit()
    log_operation('publish_announcement', f'发布公告ID: {id}')
    flash('公告已发布', 'success')
    return redirect(url_for('admin_announcements'))

@app.route('/admin/announcements/unpublish/<int:id>')
@login_required
def unpublish_announcement(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    announcement = Announcement.query.get_or_404(id)
    announcement.is_published = False
    db.session.commit()
    flash('公告已取消发布', 'success')
    return redirect(url_for('admin_announcements'))

@app.route('/admin/announcements/delete/<int:id>')
@login_required
def delete_announcement(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    log_operation('delete_announcement', f'删除公告ID: {id}')
    flash('公告删除成功', 'success')
    return redirect(url_for('admin_announcements'))

@app.route('/admin/announcements/edit/<int:id>', methods=['POST'])
@login_required
def edit_announcement(id):
    if current_user.role not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    announcement = Announcement.query.get_or_404(id)
    announcement.title = request.form.get('title')
    announcement.content = request.form.get('content')
    announcement.is_published = request.form.get('is_published') == 'on'
    announcement.priority = request.form.get('priority', 'normal')
    db.session.commit()
    log_operation('edit_announcement', f'编辑公告ID: {id}')
    flash('公告更新成功', 'success')
    return redirect(url_for('admin_announcements'))

@app.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    all_users = User.query.order_by(User.id).all()
    return render_template('admin/users.html', users=all_users)

@app.route('/users/add', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    role = request.form.get('role')
    student_id = request.form.get('student_id')
    phone = request.form.get('phone')
    email = request.form.get('email')
    is_active = request.form.get('is_active') == 'on'

    if User.query.filter_by(username=username).first():
        flash('用户名已存在', 'danger')
        return redirect(url_for('users'))

    user = User(username=username, role=role, name=name, student_id=student_id,
               phone=phone, email=email, is_active=is_active)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    log_operation('add_user', f'添加用户: {username}, 角色: {role}')
    flash('用户添加成功', 'success')
    return redirect(url_for('users'))

@app.route('/users/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('不能删除当前用户', 'danger')
        return redirect(url_for('users'))
    db.session.delete(user)
    db.session.commit()
    log_operation('delete_user', f'删除用户ID: {id}')
    flash('用户删除成功', 'success')
    return redirect(url_for('users'))

@app.route('/users/edit/<int:id>', methods=['POST'])
@login_required
def edit_user(id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    user = User.query.get_or_404(id)
    user.name = request.form.get('name')
    user.role = request.form.get('role')
    user.student_id = request.form.get('student_id')
    user.phone = request.form.get('phone')
    user.email = request.form.get('email')
    user.is_active = request.form.get('is_active') == 'on'
    db.session.commit()
    log_operation('edit_user', f'编辑用户ID: {id}')
    flash('用户信息更新成功', 'success')
    return redirect(url_for('users'))

@app.route('/users/toggle_active/<int:id>')
@login_required
def toggle_user_active(id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    db.session.commit()
    status = '激活' if user.is_active else '禁用'
    flash(f'用户已{status}', 'success')
    return redirect(url_for('users'))

@app.route('/logs')
@login_required
def operation_logs():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    logs = OperationLog.query.order_by(OperationLog.created_at.desc()).limit(100).all()
    return render_template('admin/logs.html', logs=logs)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    athlete = None
    if current_user.role == 'athlete':
        athlete = Athlete.query.filter_by(user_id=current_user.id).first()
        if not athlete:
            athlete = Athlete(user_id=current_user.id, name=current_user.name or current_user.username, student_id=current_user.student_id or '')
            db.session.add(athlete)
            db.session.commit()
            athlete = Athlete.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        current_user.email = request.form.get('email')
        db.session.add(current_user)

        if athlete:
            athlete.class_name = request.form.get('class_name')
            athlete.gender = request.form.get('gender')
            db.session.add(athlete)

        db.session.commit()

        log_operation('update_profile', '更新个人信息')
        flash('个人信息更新成功', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', athlete=athlete)

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not current_user.check_password(current_password):
        flash('当前密码错误', 'danger')
        return redirect(url_for('profile'))

    if new_password != confirm_password:
        flash('两次输入的密码不一致', 'danger')
        return redirect(url_for('profile'))

    if len(new_password) < 6:
        flash('密码长度至少6位', 'danger')
        return redirect(url_for('profile'))

    current_user.set_password(new_password)
    db.session.commit()
    log_operation('change_password', '修改密码')
    flash('密码修改成功，请重新登录', 'success')
    return redirect(url_for('logout'))

@app.route('/api/events/registration-status')
@login_required
def api_event_registration_status():
    events = Event.query.filter_by(status='published').all()
    result = []
    for event in events:
        current_count = Registration.query.filter_by(event_id=event.id, status='approved').count()
        result.append({
            'id': event.id,
            'name': event.name,
            'registered': current_count,
            'max': event.max_participants,
            'full': current_count >= event.max_participants
        })
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # 仅创建管理员账户（如果不存在则创建）
        created_count = 0
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin', name='系统管理员', is_active=True)
            admin.set_password('admin123')
            db.session.add(admin)
            created_count += 1

        # 批量提交
        if created_count > 0:
            db.session.commit()
            print(f"已创建 {created_count} 个默认用户账户")

    app.run(debug=True, host='0.0.0.0', port=5000)
