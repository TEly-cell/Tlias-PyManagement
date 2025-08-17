from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
import uuid
import random
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Email, Optional, URL, EqualTo
from datetime import datetime, timedelta
import os
import time
import random
import json
import uuid
from dotenv import load_dotenv
from flask import url_for


# 加载环境变量
load_dotenv()

# 初始化Flask应用
app = Flask(__name__)

# 初始化CSRF保护
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app/data/tlias.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 安全配置
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止JavaScript访问cookie
app.config['SESSION_COOKIE_SECURE'] = os.getenv('ENVIRONMENT') == 'production'  # 生产环境使用HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 会话有效期
app.config['WTF_CSRF_ENABLED'] = True  # 启用CSRF保护
# app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', '127.0.0.1:5000')  # 开发环境中不需要设置SERVER_NAME

# 添加HTTP安全响应头
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# 导入数据库实例
from app.db import db
# 初始化数据库
db.init_app(app)

# 导入模型
from app.models import User, Course, Material, Progress, LearningPreference, LearningGoal, FavoriteCourse, Favorite, Task, DiscussionThread, DiscussionReply, ArticleTutorial
# 初始化迁移工具
migrate = Migrate(app, db)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 导入Werkzeug安全工具
from werkzeug.security import generate_password_hash, check_password_hash



# 登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('密码', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('登录')

# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('邮箱', validators=[InputRequired(), Email(), Length(max=100)])
    password = PasswordField('密码', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('注册')

# 修改密码表单
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[InputRequired(), Length(min=8, max=80)])
    new_password = PasswordField('新密码', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('确认新密码', validators=[InputRequired(), Length(min=8, max=80), EqualTo('new_password', message='两次输入的密码不一致')])
    submit = SubmitField('保存修改')

# 更新个人资料表单
class UpdateProfileForm(FlaskForm):
    email = StringField('邮箱', validators=[InputRequired(), Email(), Length(max=100)])
    avatar = FileField('头像', validators=[Optional()])
    submit = SubmitField('更新设置')

# 创建课程表单
class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('课程描述', validators=[Optional(), Length(max=500)])
    submit = SubmitField('创建课程')

# 创建学习资料表单
class MaterialForm(FlaskForm):
    title = StringField('资料标题', validators=[InputRequired(), Length(max=100)])
    content = TextAreaField('资料内容', validators=[Optional()])
    url = StringField('超链接', validators=[Optional(), URL(require_tld=True, message='请输入有效的URL')])
    type = SelectField('资料类型', choices=[('text', '文本'), ('video', '视频'), ('quiz', '测验')], validators=[InputRequired()])
    duration = StringField('时长(分钟)', validators=[Optional()])
    difficulty = SelectField('难度等级', choices=[('1', '简单'), ('2', '较简单'), ('3', '中等'), ('4', '较难'), ('5', '困难')], validators=[InputRequired()])
    tags = StringField('标签(用逗号分隔)', validators=[Optional(), Length(max=200)])
    submit = SubmitField('添加资料')

# 更新学习进度表单
class ProgressForm(FlaskForm):
    completion_rate = StringField('完成率(0-100)', validators=[InputRequired()])
    time_spent = StringField('花费时间(分钟)', validators=[Optional()])
    completed = SelectField('是否完成', choices=[('False', '未完成'), ('True', '已完成')], validators=[InputRequired()])
    submit = SubmitField('更新进度')

# 学习目标表单
class LearningGoalForm(FlaskForm):
    title = StringField('目标标题', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('目标描述', validators=[Optional(), Length(max=500)])
    course_id = SelectField('关联课程', coerce=int, validators=[Optional()])
    target_date = StringField('目标日期', validators=[InputRequired()])
    submit = SubmitField('创建目标')

# 讨论主题表单
class DiscussionThreadForm(FlaskForm):
    title = StringField('主题标题', validators=[InputRequired(), Length(max=200)])
    content = TextAreaField('主题内容', validators=[InputRequired(), Length(max=5000)])
    submit = SubmitField('发布主题')

# 讨论回复表单
class DiscussionReplyForm(FlaskForm):
    content = TextAreaField('回复内容', validators=[InputRequired(), Length(max=2000)])
    submit = SubmitField('发表回复')

# 用户加载回调
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 音乐模块路由
@app.route('/games')
def games():
    game = request.args.get('game')
    game_info = None
    if game:
        from app.games.games import games as games_data
        game_info = games_data.get(game)
    return render_template('games.html', current_game=game_info)

@app.route('/game/<game_name>')
@login_required
def game(game_name):
    if game_name == 'snake':
        return render_template('games/snake.html')
    elif game_name == 'snake_simple':
        return render_template('games/snake_simple.html')
    elif game_name == 'match3':
        return render_template('match3.html')
    else:
        return redirect(url_for('games'))

# 讨论区路由
@app.route('/discussions')
@login_required
def discussions():
    threads = DiscussionThread.query.order_by(DiscussionThread.updated_at.desc()).all()
    return render_template('discussions.html', threads=threads)

@app.route('/discussions/create', methods=['GET', 'POST'])
@login_required
def create_discussion():
    form = DiscussionThreadForm()
    if form.validate_on_submit():
        thread = DiscussionThread(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(thread)
        db.session.commit()
        flash('讨论主题创建成功!', 'success')
        return redirect(url_for('discussions'))
    return render_template('create_discussion.html', form=form)

@app.route('/discussions/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def discussion_thread(thread_id):
    thread = DiscussionThread.query.get_or_404(thread_id)
    reply_form = DiscussionReplyForm()
    if reply_form.validate_on_submit():
        reply = DiscussionReply(
            thread_id=thread_id,
            user_id=current_user.id,
            content=reply_form.content.data
        )
        db.session.add(reply)
        # 更新主题的更新时间
        thread.updated_at = datetime.utcnow()
        db.session.commit()
        flash('回复成功!', 'success')
        return redirect(url_for('discussion_thread', thread_id=thread_id))
    return render_template('discussion_thread.html', thread=thread, reply_form=reply_form)

# 课程评论提交路由
@app.route('/course/add_comment/<int:course_id>', methods=['POST'])
@login_required
def add_course_comment(course_id):
    content = request.form.get('comment_content')
    if content and len(content.strip()) > 0:
        from app.models import CourseComment
        new_comment = CourseComment(
            user_id=current_user.id,
            course_id=course_id,
            content=content.strip()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('评论添加成功!', 'success')
    return redirect(url_for('course_detail', course_id=course_id))

# 游戏模块API



  


  


# 创建游戏API
@app.route('/create_game')
@login_required
def create_game():
    game_type = request.args.get('type', 'snake')
    width = int(request.args.get('width', 20))
    height = int(request.args.get('height', 20))
    game_id = str(uuid.uuid4())
    from app.games.games import create_game as create_game_func
    create_game_func(game_type, game_id, width=width, height=height)
    return jsonify({'game_id': game_id})

# 路由
@app.route('/')
def home_page():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

# 游戏更新API路由
@app.route('/api/games/update', methods=['GET'])
@login_required
def api_update_game():
    game_id = request.args.get('game_id')
    action = request.args.get('action')
    
    # 对于交换操作，传递包含坐标的字典
    if action == 'swap':
        action_data = {
            'action': 'swap',
            'x1': request.args.get('x1'),
            'y1': request.args.get('y1'),
            'x2': request.args.get('x2'),
            'y2': request.args.get('y2')
        }
    else:
        action_data = action
    
    from app.games.games import update_game as update_game_func
    result = update_game_func(game_id, action_data)
    return jsonify(result)

# 路由


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 初始化登录尝试计数
    if 'login_attempts' not in session:
        session['login_attempts'] = 0
    if 'last_attempt_time' not in session:
        session['last_attempt_time'] = time.time()
    
    # 检查是否超过登录尝试次数
    if session['login_attempts'] >= 5:
        # 计算剩余锁定时间（5分钟）
        elapsed_time = time.time() - session['last_attempt_time']
        if elapsed_time < 300:
            remaining = int(300 - elapsed_time)
            flash(f'登录尝试次数过多，请{remaining}秒后再试')
            return render_template('login.html', form=form)
        else:
            # 重置登录尝试计数
            session['login_attempts'] = 0
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['login_attempts'] = 0  # 重置登录尝试次数
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home_page'))
        else:
            session['login_attempts'] += 1
            session['last_attempt_time'] = time.time()
            flash('用户名或密码不正确')
            
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('用户名已被注册')
            return redirect(url_for('register'))
            
        # Check if email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('邮箱已被注册')
            return redirect(url_for('register'))
            
        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('login'))
        
    # Show validation errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}：{error}')
            
    return render_template('register.html', form=form)

@app.route('/recommendations/more')
@login_required
def show_more_recommendations():
    # 获取当前用户的兴趣标签
    user_interests = []
    if current_user.learning_preference and current_user.learning_preference.interests:
        user_interests = [tag.strip() for tag in current_user.learning_preference.interests.split(',') if tag.strip()]
    
    # 1. 获取其他用户的公开资料
    other_users_materials = []
    if user_interests:
        # 构建标签匹配条件
        tag_conditions = []
        for tag in user_interests:
            tag_conditions.append(Material.tags.ilike(f'%{tag}%'))
        
        other_users_materials = Material.query.filter(
            Material.is_public == True,
            Material.user_id != current_user.id,
            db.or_(*tag_conditions)
        ).all()
    else:
        # 如果没有兴趣标签，获取最新的公开资料
        other_users_materials = Material.query.filter(
            Material.is_public == True,
            Material.user_id != current_user.id
        ).order_by(Material.created_at.desc()).limit(10).all()
    
    # 2. 生成搜索关键词
    search_keywords = list(set(user_interests))  # 去重用户兴趣
    
    # 从相关资料中提取更多关键词
    for material in other_users_materials:
        if material.tags:
            material_tags = [tag.strip() for tag in material.tags.split(',') if tag.strip()]
            for tag in material_tags:
                if tag not in search_keywords:
                    search_keywords.append(tag)
                    if len(search_keywords) >= 5:  # 限制最多5个关键词
                        break
        if len(search_keywords) >= 5:
            break
    
    # 3. 渲染模板并传递数据
    return render_template('more_recommendations.html', search_keywords=search_keywords,
                          other_users_materials=other_users_materials)



@app.route('/course/unfavorite/<int:course_id>', methods=['POST'])
@login_required
def unfavorite_course(course_id):
    # 检查是否已经收藏
    favorite = FavoriteCourse.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()
    
    if not favorite:
        return jsonify({'success': False, 'message': '课程未被收藏'})
    
    # 删除收藏
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '取消收藏成功'})

# 我的收藏路由
@app.route('/favorites')
@login_required
def my_favorites():
    # 获取用户收藏的课程
    favorite_courses = db.session.query(Course).join(
        FavoriteCourse, Course.id == FavoriteCourse.course_id
    ).filter(
        FavoriteCourse.user_id == current_user.id
    ).order_by(
        FavoriteCourse.created_at.desc()
    ).all()

    # 格式化课程数据
    courses_data = []
    for course in favorite_courses:
        courses_data.append({
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'created_at': course.created_at.strftime('%Y-%m-%d'),
            'materials_count': len(course.materials)
        })

    return render_template('favorites.html', courses=favorite_courses)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

# 学习资料管理路由
@app.route('/material/create/<int:course_id>', methods=['GET', 'POST'])
@login_required
def create_material(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user_id != current_user.id:
        flash('无权访问此课程')
        return redirect(url_for('dashboard'))
    form = MaterialForm()
    if form.validate_on_submit():
        # 处理文件上传
        file_path = None
        if 'file_upload' in request.files:
            file = request.files['file_upload']
            if file.filename:
                try:
                    # 创建上传目录（如果不存在）
                    upload_dir = os.path.join(app.root_path, 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    # 生成安全的唯一文件名
                    from werkzeug.utils import secure_filename
                    safe_filename = secure_filename(file.filename)
                    filename = f'{datetime.utcnow().strftime("%Y%m%d%H%M%S")}_{safe_filename}'
                    file_path = os.path.join('uploads', filename)
                    # 保存文件
                    file.save(os.path.join(app.root_path, file_path))
                except Exception as e:
                    db.session.rollback()
                    flash(f'文件上传失败: {str(e)}', 'danger')
                    return redirect(url_for('create_material', course_id=course_id))
        
        new_material = Material(
            title=form.title.data,
            content=form.content.data,
            url=form.url.data,
            type=form.type.data,
            duration=int(form.duration.data) if form.duration.data else None,
            file_path=file_path,
            course_id=course_id,
            created_by=current_user.id
        )
        db.session.add(new_material)
        db.session.commit()
        
        flash('学习资料创建成功')
        return redirect(url_for('course_detail', course_id=course_id))
    
    return render_template('create_material.html', form=form, course=course)

    course = Course.query.get_or_404(material.course_id)
    if course.user_id != current_user.id:
        flash('无权访问此资料')
        return redirect(url_for('dashboard'))
    # 检查是否已有进度记录
    progress = Progress.query.filter_by(user_id=current_user.id, material_id=material_id).first()
    if not progress:
        # 创建新的进度记录
        progress = Progress(user_id=current_user.id, material_id=material_id)
        db.session.add(progress)
        db.session.commit()
    return render_template('material_detail.html', material=material, course=course, progress=progress)

# 学习进度跟踪路由
@app.route('/progress/update/<int:material_id>', methods=['GET', 'POST'])
@login_required
def update_progress(material_id):
    material = Material.query.get_or_404(material_id)
    course = Course.query.get_or_404(material.course_id)
    return render_template('material_detail.html', material=material, course=course)
    if course.user_id != current_user.id:
        flash('无权访问此资料')
        return redirect(url_for('dashboard'))
    progress = Progress.query.filter_by(user_id=current_user.id, material_id=material_id).first()
    if not progress:
        progress = Progress(user_id=current_user.id, material_id=material_id)
        db.session.add(progress)
    form = ProgressForm(
        completion_rate=str(progress.completion_rate * 100),
        time_spent=str(progress.time_spent),
        completed=str(progress.completed)
    )
    if form.validate_on_submit():
        progress.completion_rate = float(form.completion_rate.data) / 100
        progress.time_spent = int(form.time_spent.data) if form.time_spent.data else 0
        progress.completed = form.completed.data == 'True'
        progress.last_accessed = datetime.utcnow()
        db.session.commit()
        flash('学习进度已更新!')
        # 更新学习偏好
        update_learning_preference(current_user.id, material)
        return redirect(url_for('material_detail', material_id=material_id))
    return render_template('update_progress.html', form=form, material=material)

# 学习目标管理路由
@app.route('/goal/create', methods=['GET', 'POST'])
@login_required
def create_goal():
    form = LearningGoalForm()
    # 加载用户的课程作为下拉选项
    form.course_id.choices = [(0, '无关联课程')] + [(course.id, course.name) for course in Course.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        # 解析目标日期
        target_date = datetime.strptime(form.target_date.data, '%Y-%m-%d')
        
        new_goal = LearningGoal(
            title=form.title.data,
            description=form.description.data,
            course_id=form.course_id.data if form.course_id.data != 0 else None,
            target_date=target_date,
            user_id=current_user.id
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('学习目标创建成功!')
        return redirect(url_for('view_goals'))
    
    return render_template('create_goal.html', form=form)

@app.route('/goals')
@login_required
def view_goals():
    goals = LearningGoal.query.filter_by(user_id=current_user.id).order_by(LearningGoal.target_date.asc()).all()
    return render_template('view_goals.html', goals=goals)

@app.route('/goal/update/<int:goal_id>', methods=['POST'])
@login_required
def update_goal(goal_id):
    goal = LearningGoal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash('无权访问此目标')
        return redirect(url_for('view_goals'))
    
    goal.completed = not goal.completed
    db.session.commit()
    flash('学习目标状态已更新!')
    return redirect(url_for('view_goals'))

# 学习统计路由
@app.route('/stats')
def learning_stats():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = 8  # 每页显示8篇文章
        
        # 获取公共文章教程（所有用户可见），添加分页
        query = ArticleTutorial.query.filter_by(is_public=True)
        
        # 搜索参数
        search_query = request.args.get('search', '')
        category_filter = request.args.get('category', '')
        
        if search_query:
            query = query.filter(ArticleTutorial.title.contains(search_query))
        
        if category_filter:
            query = query.filter(ArticleTutorial.category == category_filter)
        
        # 按创建时间降序排序并分页
        pagination = query.order_by(ArticleTutorial.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
        
        public_articles = pagination.items
        
        # 如果用户已登录，计算个人统计数据
        if current_user.is_authenticated:
            # 计算总体完成率
            total_materials = Progress.query.filter_by(user_id=current_user.id).count()
            completed_materials = Progress.query.filter_by(user_id=current_user.id, completed=True).count()
            overall_completion_rate = completed_materials / total_materials if total_materials > 0 else 0

            # 计算每周学习时间
            weekly_stats = []
            for i in range(7):
                day = datetime.now() - timedelta(days=i)
                start_of_day = datetime(day.year, day.month, day.day, 0, 0, 0)
                end_of_day = datetime(day.year, day.month, day.day, 23, 59, 59)
                time_spent = db.session.query(db.func.sum(Progress.time_spent)).filter(
                    Progress.user_id == current_user.id,
                    Progress.last_accessed >= start_of_day,
                    Progress.last_accessed <= end_of_day
                ).scalar() or 0
                weekly_stats.append({
                    'day': day.strftime('%Y-%m-%d'),
                    'time_spent': time_spent
                })
            weekly_stats.reverse()

            # 按课程统计
            courses = Course.query.filter_by(user_id=current_user.id).all()
            course_stats = []
            for course in courses:
                course_materials = Material.query.filter_by(course_id=course.id).count()
                completed = Progress.query.filter(
                    Progress.user_id == current_user.id,
                    Progress.material_id.in_(db.session.query(Material.id).filter(Material.course_id == course.id)),
                    Progress.completed == True
                ).count()
                completion_rate = completed / course_materials if course_materials > 0 else 0
                course_stats.append({
                    'course_name': course.name,
                    'completion_rate': completion_rate,
                    'materials_count': course_materials,
                    'completed_count': completed
                })

            # 构建总体统计数据
            overall_stats = {
                'completion_rate': overall_completion_rate * 100,
                'completed_courses': len([c for c in course_stats if c['completion_rate'] == 1]),
                'total_courses': len(course_stats),
                'completed_materials': completed_materials,
                'total_materials': total_materials,
                'total_time_spent': sum([s['time_spent'] for s in weekly_stats])
            }

            # 模拟最近学习活动数据
            recent_activities = []
            if courses:
                for course in courses[:3]:  # 只显示前3个课程的活动
                    materials = Material.query.filter_by(course_id=course.id).all()
                    for material in materials[:2]:  # 每个课程显示2个资料
                        progress = Progress.query.filter_by(
                            user_id=current_user.id,
                            material_id=material.id
                        ).first()
                        if progress:
                            recent_activities.append({
                                'course_id': course.id,
                                'course_name': course.name,
                                'material_id': material.id,
                                'material_title': material.title,
                                'completion_rate': (progress.completion_rate or 0) * 100,
                                'completed': progress.completed or False,
                                'last_accessed': progress.last_accessed or db.func.now()
                        })
        else:
            # 未登录用户的数据为空
            overall_stats = None
            course_stats = []
            recent_activities = []
            
    except Exception as e:
        logger.error(f"学习统计页面出错: {str(e)}", exc_info=True)
        return jsonify({'error': '获取学习统计失败', 'details': str(e)}), 500
    
    return render_template('learning_stats.html',
                          overall_stats=overall_stats,
                          course_stats=course_stats,
                          recent_activities=recent_activities,
                          public_articles=public_articles,
                          pagination=pagination,
                          search_query=search_query,
                          category_filter=category_filter)

# 智能推荐路由
@app.route('/recommendations')
@login_required
def recommendations():
    # 获取用户学习偏好
    preferences = LearningPreference.query.filter_by(user_id=current_user.id).all()

    # 根据偏好生成推荐
    recommended_materials = []

    if preferences:
        # 简单推荐算法: 基于标签、难度和内容类型
        for pref in preferences:
            query = Material.query.join(Course).filter(
                Course.user_id == current_user.id,
                Material.tags.like(f'%{pref.preferred_tag}%'),
                Material.difficulty == pref.preferred_difficulty,
                Material.type == pref.preferred_content_type
            )
            recommended = query.limit(5).all()
            recommended_materials.extend(recommended)
    else:
        # 如果没有偏好，推荐最近添加的资料
        recommended_materials = Material.query.join(Course).filter(
            Course.user_id == current_user.id
        ).order_by(Material.created_at.desc()).limit(5).all()

    # 去重
    recommended_materials = list({m.id: m for m in recommended_materials}.values())

    return render_template('recommendations.html', materials=recommended_materials)

# API路由 - 用于前端获取数据
@app.route('/api/stats')
@login_required
def api_stats():
    total_materials = Progress.query.filter_by(user_id=current_user.id).count()
    completed_materials = Progress.query.filter_by(user_id=current_user.id, completed=True).count()
    overall_completion_rate = completed_materials / total_materials if total_materials > 0 else 0

    # 计算每周学习时间
    weekly_stats = []
    for i in range(7):
        day = datetime.now() - timedelta(days=i)
        start_of_day = datetime(day.year, day.month, day.day, 0, 0, 0)
        end_of_day = datetime(day.year, day.month, day.day, 23, 59, 59)
        time_spent = db.session.query(db.func.sum(Progress.time_spent)).filter(
            Progress.user_id == current_user.id,
            Progress.last_accessed >= start_of_day,
            Progress.last_accessed <= end_of_day
        ).scalar() or 0
        weekly_stats.append({
            'day': day.strftime('%Y-%m-%d'),
            'time_spent': time_spent
        })
    weekly_stats.reverse()

    return jsonify({
        'overall_completion_rate': overall_completion_rate
    })

# 客服中心路由
@app.route('/support')
@login_required
def support_center():
    # 常见问题
    faqs = [
        {'question': '如何创建新课程？', 'answer': '在仪表板页面点击"创建课程"按钮，填写课程名称和描述即可。'},
        {'question': '如何添加学习资料？', 'answer': '进入课程详情页面，点击"添加学习资料"按钮，填写相关信息即可。'},
        {'question': '如何跟踪学习进度？', 'answer': '在学习资料详情页面，点击"更新进度"按钮，设置完成率和学习时间。'},
        {'question': '如何修改个人资料？', 'answer': '点击右上角头像，选择"个人资料"，即可修改密码和邮箱。'},
        {'question': '如何创建学习目标？', 'answer': '点击导航栏中的"学习目标"，然后点击"创建目标"按钮，填写相关信息即可。'}
    ]
    return render_template('support_center.html', faqs=faqs)

# AI聊天API
@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    data = request.json
    message = data.get('message', '').lower()

    # 意图识别和更智能的回复系统
    # 1. 问候类
    greetings = ['你好', '嗨', '您好', '早上好', '下午好', '晚上好']
    if any(greeting in message for greeting in greetings):
        return jsonify({'response': '您好！我是智能客服助手，很高兴为您服务。请问有什么可以帮到您的吗？'})

    # 2. 身份类
    identity = ['你是谁', '你叫什么', '你是什么']
    if any(id in message for id in identity):
        return jsonify({'response': '我是Tlias智能学习平台的智能客服助手，专门为您解答学习管理系统的相关问题。如果您有任何使用上的疑问，都可以问我哦！'})

    # 3. 感谢类
    thanks = ['谢谢', '感谢', '非常感谢']
    if any(thank in message for thank in thanks):
        return jsonify({'response': '不客气！这是我应该做的。如有其他问题，请随时提问，我会尽力为您解答。'})

    # 4. 再见类
    goodbyes = ['再见', '拜拜', '下次见']
    if any(goodbye in message for goodbye in goodbyes):
        return jsonify({'response': '再见！祝您学习愉快，取得理想的成绩！如果您还有其他问题，欢迎随时再来咨询。'})

    # 5. 课程创建类
    course_create = ['创建课程', '新建课程', '如何创建课程']
    if any(cc in message for cc in course_create):
        return jsonify({'response': '创建课程非常简单！首先，登录您的账号并进入仪表板页面，找到并点击"创建课程"按钮。然后，填写课程名称、描述、选择课程分类和设置访问权限。最后，点击"保存"按钮即可成功创建新课程。创建后，您还可以添加学习资料和布置作业哦！'})

    # 6. 学习资料类
    materials = ['添加资料', '上传资料', '如何添加学习资料', '学习资料']
    if any(m in message for m in materials):
        return jsonify({'response': '添加学习资料的步骤如下：1. 进入您创建的课程详情页面；2. 点击"添加学习资料"按钮；3. 填写资料标题、描述，选择资料类型（如文档、视频、音频等）；4. 上传资料文件或填写外部链接；5. 设置资料的难度级别和标签；6. 点击"保存"按钮完成添加。添加后，学生就可以在课程中查看和学习这份资料了。'})

    # 7. 学习进度类
    progress = ['学习进度', '查看进度', '更新进度']
    if any(p in message for p in progress):
        return jsonify({'response': '跟踪学习进度的方法有两种：1. 对于单个学习资料，进入资料详情页面，点击"更新进度"按钮，设置完成率和学习时间；2. 在"我的学习"页面，您可以查看所有课程的总体学习进度、已完成和未完成的资料数量，以及最近的学习记录。系统会自动统计您的学习时间和完成率，并生成学习报告。'})

    # 8. 个人资料类
    profile = ['个人资料', '修改资料', '更改密码', '更新信息']
    if any(pf in message for pf in profile):
        return jsonify({'response': '修改个人资料的步骤：点击右上角的头像，选择"个人资料"选项。在个人资料页面，您可以修改姓名、邮箱、手机号码等基本信息。如果需要修改密码，点击"修改密码"选项，输入当前密码和新密码，然后点击"保存"按钮即可。请确保您的个人信息准确无误，以便我们能及时与您联系。'})

    # 9. 学习目标类
    goals = ['学习目标', '创建目标', '设定目标']
    if any(g in message for g in goals):
        return jsonify({'response': '创建学习目标有助于提高学习效率。操作步骤：点击导航栏中的"学习目标"选项，然后点击"创建目标"按钮。在创建目标页面，填写目标名称、描述、选择目标类型（如短期目标、长期目标）、设置开始日期和截止日期，以及目标完成标准。创建后，系统会定期提醒您目标的完成进度，并在目标达成时给予奖励。'})

    # 10. 常见问题类
    faq = ['常见问题', 'FAQ', '问题解答']
    if any(f in message for f in faq):
        return jsonify({'response': '您可以在客服中心页面左侧的"常见问题"部分找到大部分使用问题的解答。那里包含了关于课程创建、学习资料添加、学习进度跟踪、个人资料修改等方面的常见问题和详细解答。如果您没有找到想要的答案，请随时向我提问，我会尽力为您解答。'})

    # 11. 搜索功能类
    search = ['搜索', '查找', '如何搜索']
    if any(s in message for s in search):
        return jsonify({'response': '在平台顶部的搜索框中，您可以输入关键词搜索课程、学习资料、讨论话题等内容。您也可以使用高级搜索功能，根据课程分类、难度级别、发布时间等条件进行筛选，以便更精准地找到您需要的内容。'})

    # 12. 讨论区类
    discussion = ['讨论区', '提问', '回答问题', '参与讨论']
    if any(d in message for d in discussion):
        return jsonify({'response': '讨论区是学员之间交流学习心得、解答疑问的平台。点击导航栏中的"讨论区"选项，您可以浏览热门讨论话题，也可以创建新的讨论。在讨论详情页面，您可以发表自己的观点和回答他人的问题。请遵守社区规范，文明发言，共同维护良好的讨论氛围。'})

    # 如果没有匹配的意图，使用更智能的默认回复
    default_responses = [
        f'抱歉，我不太理解您的问题："{data.get("message", "")}"。请尝试用其他方式描述，或者提供更多细节，我会尽力为您解答。',
        f'关于"{data.get("message", "")}"，很抱歉，我暂时无法回答这个问题。不过，我正在不断学习和进步，相信很快就能为您解答了。',
        '您的问题有点复杂，我需要时间思考一下。请稍等片刻，我会尽力为您提供准确的回答。'
    ]
    return jsonify({'response': random.choice(default_responses)})

# 文章教程详情页路由
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    article = ArticleTutorial.query.get_or_404(article_id)
    if not article.is_public and not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # 增加浏览次数
    article.increment_views()
    
    # 获取相关文章（同分类的文章）
    related_articles = ArticleTutorial.query.filter(
        ArticleTutorial.category == article.category,
        ArticleTutorial.id != article.id,
        ArticleTutorial.is_public == True
    ).order_by(ArticleTutorial.created_at.desc()).limit(3).all()
    
    return render_template('article_detail.html', 
                         article=article, 
                         related_articles=related_articles)

# 文章点赞API
@app.route('/api/article/<int:article_id>/like', methods=['POST'])
def like_article(article_id):
    article = ArticleTutorial.query.get_or_404(article_id)
    if not article.is_public:
        return jsonify({'error': '文章不可访问'}), 403
    
    article.increment_likes()
    return jsonify({'likes': article.like_count})

# 辅助函数: 更新学习偏好
def update_learning_preference(user_id, material):
    # 简单的偏好更新逻辑: 记录用户最近接触的标签、难度和内容类型
    if material.tags:
        tags = material.tags.split(',')
        for tag in tags:
            tag = tag.strip()
            if tag:
                pref = LearningPreference.query.filter_by(
                    user_id=user_id,
                    preferred_tag=tag,
                    preferred_difficulty=material.difficulty,
                    preferred_content_type=material.type
                ).first()
                if not pref:
                    pref = LearningPreference(
                        user_id=user_id,
                        preferred_tag=tag,
                        preferred_difficulty=material.difficulty,
                        preferred_content_type=material.type
                    )
                    db.session.add(pref)
        db.session.commit()


# 消消乐游戏路由
@app.route('/match3')
def match3():
    return render_template('match3.html')

# 消消乐游戏备用路由
@app.route('/game/match3')
def game_match3():
    return render_template('match3.html')

# 测试交换功能的路由
@app.route('/test_swap')
def test_swap():
    return render_template('test_swap.html')


    other_users_materials = Material.query.join(Course).filter(
        Course.user_id != current_user.id,
        Material.tags.ilike('%' + interest_tags[0] + '%') if interest_tags else True
    ).order_by(Material.created_at.desc()).limit(5).all()

    # 2. 生成网页搜索关键词推荐
    search_keywords = []
    if interest_tags:
        search_keywords = interest_tags[:3]  # 取前3个兴趣标签作为搜索关键词

    return render_template('more_recommendations.html', 
                          other_users_materials=other_users_materials,
                          search_keywords=search_keywords)

# 已删除重复的应用启动代码块



@app.route('/discussions/<int:thread_id>/delete', methods=['POST'])
@login_required
def delete_thread(thread_id):
    thread = DiscussionThread.query.get_or_404(thread_id)
    if thread.user_id != current_user.id and not hasattr(current_user, 'is_admin'):  # 修改此处以避免属性错误
        flash('没有权限删除该主题', 'danger')
        return redirect(url_for('discussions'))
    db.session.delete(thread)
    db.session.commit()
    flash('讨论主题已删除', 'success')
    return redirect(url_for('discussions'))

@app.route('/discussions/reply/<int:reply_id>/delete', methods=['POST'])
@login_required
def delete_reply(reply_id):
    reply = DiscussionReply.query.get_or_404(reply_id)
    thread_id = reply.thread_id
    if reply.user_id != current_user.id and not hasattr(current_user, 'is_admin'):  # 修改此处以避免属性错误
        flash('没有权限删除该回复', 'danger')
        return redirect(url_for('discussion_thread', thread_id=thread_id))
    db.session.delete(reply)
    # 更新主题的更新时间
    thread = DiscussionThread.query.get_or_404(thread_id)
    thread.updated_at = datetime.utcnow()
    db.session.commit()
    flash('回复已删除', 'success')
    return redirect(url_for('discussion_thread', thread_id=thread_id))

# API测试页面
@app.route('/api_test')
def api_test():
    return render_template('api_test.html')

# 游戏模块API

@login_required
def swap_game():
    game_id = request.args.get('game_id')
    x1 = request.args.get('x1')
    y1 = request.args.get('y1')
    x2 = request.args.get('x2')
    y2 = request.args.get('y2')

    # 添加调试信息
    print(f"收到交换请求: game_id={game_id}, x1={x1}, y1={y1}, x2={x2}, y2={y2}")
    print(f"请求参数: {request.args}")
    print(f"请求头: {request.headers}")

    if not all([game_id, x1, y1, x2, y2]):
        print(f"缺少参数: game_id={game_id}, x1={x1}, y1={y1}, x2={x2}, y2={y2}")
        return jsonify({'success': False, 'error': '缺少必要的参数'})

    try:
        # 注意：Match3Game.swap_cells方法期望的参数顺序是(y1, x1, y2, x2)
        # 我们需要调整参数顺序以匹配后端期望
        action = {
            'action': 'swap',
            'x1': int(x1),  # 保持x1不变
            'y1': int(y1),  # 保持y1不变
            'x2': int(x2),  # 保持x2不变
            'y2': int(y2)   # 保持y2不变
        }
        from app.games.games import update_game
        result = update_game(game_id, action)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/games/create', methods=['GET'])
@login_required
def api_create_game():
    print('========== 收到创建游戏请求 ==========')
    print(f'请求时间: {datetime.utcnow()}')
    print(f'请求IP: {request.remote_addr}')
    print(f'请求头: {request.headers}')
    game_type = request.args.get('type', 'snake')
    print(f'游戏类型: {game_type}')
    print(f'当前用户ID: {current_user.id}')
    print(f'当前用户名: {current_user.username}')
    width = int(request.args.get('width', 20))
    height = int(request.args.get('height', 20))
    game_id = str(uuid.uuid4())
    from app.games.games import create_game as create_game_func
    create_game_func(game_type, game_id, width=width, height=height)
    return jsonify({'game_id': game_id})

@app.route('/api/games/reset', methods=['GET'])
@login_required
def api_reset_game():
    game_id = request.args.get('game_id')
    from app.games.games import reset_game as reset_game_func
    result = reset_game_func(game_id)
    return jsonify(result)

# 任务模块API
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'name': task.name,
            'difficulty': task.difficulty,
            'completed': task.completed,
            'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(task_list)

@app.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.json
    if not data or 'name' not in data or 'difficulty' not in data:
        return jsonify({'success': False, 'message': '缺少必要的任务信息'})

    new_task = Task(
        user_id=current_user.id,
        name=data['name'],
        difficulty=data['difficulty']
    )

    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'success': True, 'message': '任务添加成功', 'task_id': new_task.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'添加任务时出错: {str(e)}'})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'success': False, 'message': '无权修改此任务'})

    data = request.json
    if 'completed' in data:
        task.completed = data['completed']

    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '任务状态已更新'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新任务时出错: {str(e)}'})

@app.route('/dashboard')
@login_required
def dashboard():
    # 获取搜索参数和排序参数
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'created_at_desc')

    # 构建查询
    query = Course.query.filter_by(user_id=current_user.id)

    # 应用搜索过滤
    if search_query:
        query = query.filter(Course.name.like(f'%{search_query}%') | Course.description.like(f'%{search_query}%'))

    # 应用排序
    if sort_by == 'created_at_desc':
        query = query.order_by(Course.created_at.desc())
    elif sort_by == 'created_at_asc':
        query = query.order_by(Course.created_at.asc())
    elif sort_by == 'name_asc':
        query = query.order_by(Course.name.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Course.name.desc())

    # 执行查询
    courses = query.all()

    return render_template('dashboard.html', courses=courses, search_query=search_query, sort_by=sort_by)

@app.route('/profile')
@login_required
def profile():
    password_form = ChangePasswordForm()
    profile_form = UpdateProfileForm()
    return render_template('profile.html', password_form=password_form, profile_form=profile_form)

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('密码修改成功')
        else:
            flash('旧密码输入错误')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}：{error}')
    return redirect(url_for('profile'))

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email and existing_email.id != current_user.id:
            flash('邮箱已被注册')
        else:
            current_user.email = form.email.data
            
            # 处理头像上传
            if 'avatar' in request.files:
                file = request.files['avatar']
                if file and file.filename:
                    # 生成唯一文件名
                    filename = secure_filename(file.filename)
                    unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
                    # 确保上传目录存在
                    upload_dir = os.path.join(app.static_folder, 'avatars')
                    os.makedirs(upload_dir, exist_ok=True)
                    # 保存文件
                    file_path = os.path.join(upload_dir, unique_filename)
                    file.save(file_path)
                    # 更新用户头像
                    current_user.avatar = unique_filename
            
            db.session.commit()
            flash('个人资料更新成功')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}：{error}')
    return redirect(url_for('profile'))
@app.route('/api/games/<game_id>/state')
@login_required
def api_get_game_state(game_id):
    """获取游戏状态"""
    try:
        from app.games.games import get_game_state
        result = get_game_state(game_id)
        if result is None:
            return jsonify({'error': '游戏不存在'}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/games/swap', methods=['POST'])
@login_required
def api_swap_game():
    game_id = request.args.get('game_id')  # 移除type=int，支持字符串格式的UUID
    x1 = request.args.get('x1', type=int)
    y1 = request.args.get('y1', type=int)
    x2 = request.args.get('x2', type=int)
    y2 = request.args.get('y2', type=int)
    from app.games.games import update_game
    result = update_game(game_id, {'action': 'swap', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
    return jsonify(result)

# 检查课程是否已收藏
@app.route('/course/is_favorite/<int:course_id>', methods=['GET'])
@login_required
def is_course_favorite(course_id):
    is_favorite = FavoriteCourse.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first() is not None
    return jsonify({'is_favorite': is_favorite})

# 课程管理路由
@app.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        new_course = Course(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_course)
        db.session.commit()
        flash('课程创建成功!')
        return redirect(url_for('dashboard'))
    return render_template('create_course.html', form=form)

@app.route('/course/detail/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    materials = Material.query.filter_by(course_id=course_id).all()
    
    # 计算课程完成率
    total_materials = len(materials)
    if total_materials > 0:
        # 计算当前用户完成的资料数量
        completed_count = 0
        for material in materials:
            progress = Progress.query.filter_by(
                user_id=current_user.id,
                material_id=material.id,
                completed=True
            ).first()
            if progress:
                completed_count += 1
        completion_rate = (completed_count / total_materials) * 100
    else:
        completion_rate = 0
    
    # 获取推荐课程
    recommended_courses = Course.query.filter(
        Course.id != course_id
    ).limit(3).all()
    
    # Generate recent activities for this course
    recent_activities = []
    if current_user.is_authenticated:
        # Get recent progress for materials in this course
        recent_progresses = Progress.query.filter(
            Progress.user_id == current_user.id,
            Progress.material_id.in_([m.id for m in materials])
        ).order_by(Progress.last_accessed.desc()).limit(5).all()
        
        for progress in recent_progresses:
            material = next((m for m in materials if m.id == progress.material_id), None)
            if material:
                recent_activities.append({
                    'course_id': course.id,
                    'course_name': course.name,
                    'material_id': material.id,
                    'material_title': material.title,
                    'completion_rate': (progress.completion_rate or 0) * 100,
                    'completed': progress.completed or False,
                    'last_accessed': progress.last_accessed or datetime.now()
                })
    
    return render_template('course_detail.html', course=course, materials=materials, completion_rate=completion_rate, recommended_courses=recommended_courses, recent_activities=recent_activities)

# 收藏课程
@app.route('/course/favorite/<int:course_id>', methods=['POST'])
@login_required
def favorite_course(course_id):
    # 检查课程是否存在
    course = Course.query.get_or_404(course_id)
    
    # 检查是否已经收藏
    existing_favorite = FavoriteCourse.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing_favorite:
        return jsonify({'success': False, 'message': '课程已经被收藏'})
    
    # 创建新收藏
    new_favorite = FavoriteCourse(
        user_id=current_user.id,
        course_id=course_id
    )
    
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '课程收藏成功'})

@app.route('/material/<int:material_id>')
@login_required
def material_detail(material_id):
    material = Material.query.get_or_404(material_id)
    course = Course.query.get_or_404(material.course_id)
    return render_template('material_detail.html', material=material, course=course)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)