from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(100), nullable=True)
    level = db.Column(db.Integer, default=1)
    followers = db.Column(db.Integer, default=0)
    following = db.Column(db.Integer, default=0)
    visits = db.Column(db.Integer, default=0)
    listen_time = db.Column(db.String(50), default='0分钟')
    vip_level = db.Column(db.Integer, default=0)
    courses = db.relationship('Course', backref='user', lazy=True)

    # 设置密码（生成哈希）
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码验证方法
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    materials = db.relationship('Material', backref='course', lazy=True)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    type = db.Column(db.String(20))  # 如 'text', 'video', 'quiz'
    duration = db.Column(db.Integer)  # 内容时长(分钟)
    file_path = db.Column(db.String(200))  # 文件路径
    url = db.Column(db.String(500))  # 超链接地址
    difficulty = db.Column(db.Integer)  # 难度等级(1-5)
    tags = db.Column(db.String(200))  # 标签，用于推荐
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_rate = db.Column(db.Float, default=0.0)  # 完成率(0-1)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer, default=0)  # 花费时间(分钟)

class LearningPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    preferred_tag = db.Column(db.String(50))
    preferred_difficulty = db.Column(db.Integer)  # 1-5
    preferred_content_type = db.Column(db.String(20))

class LearningGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.relationship('Course')

class FavoriteCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系定义
    user = db.relationship('User', backref=db.backref('favorites', lazy=True, cascade='all, delete-orphan'))
    material = db.relationship('Material', backref=db.backref('favorites', lazy=True, cascade='all, delete-orphan'))
    
    # 确保用户不会重复收藏同一资料
    __table_args__ = (
        db.UniqueConstraint('user_id', 'material_id', name='unique_user_material_favorite'),
    )

    def __repr__(self):
        return f'<Favorite {self.user_id}:{self.material_id}>'


# 任务模型
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.name}>'

# 讨论主题模型
class DiscussionThread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    replies = db.relationship('DiscussionReply', backref='thread', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User')

    def __repr__(self):
        return f'<DiscussionThread {self.title}>'

# 讨论回复模型
class DiscussionReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('discussion_thread.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User')

    def __repr__(self):
        return f'<DiscussionReply {self.id}>'

# 文章教程模型
class ArticleTutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)  # 文章摘要
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 如：入门指南、进阶技巧、案例分析等
    tags = db.Column(db.String(500))  # 标签，用逗号分隔
    difficulty_level = db.Column(db.Integer, default=1)  # 难度等级 1-5
    is_public = db.Column(db.Boolean, default=True)  # 是否公开可见
    view_count = db.Column(db.Integer, default=0)  # 浏览次数
    like_count = db.Column(db.Integer, default=0)  # 点赞次数
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ArticleTutorial {self.title}>'
    
    def increment_views(self):
        self.view_count += 1
        db.session.commit()
    
    def increment_likes(self):
        self.like_count += 1
        db.session.commit()
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []