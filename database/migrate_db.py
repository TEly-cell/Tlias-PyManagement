from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app/data/tlias.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 导入数据库实例
from app.db import db
# 初始化数据库
db.init_app(app)

# 导入模型，确保所有模型都被加载
from app.models import User, Course, Material, Progress, LearningPreference, LearningGoal, FavoriteCourse, Favorite, Task, DiscussionThread, DiscussionReply

# 初始化迁移工具
migrate = Migrate(app, db)

if __name__ == '__main__':
    print('数据库迁移脚本已准备好。请在命令行中运行:')
    print('flask db migrate -m "Add user profile fields"')
    print('然后运行:')
    print('flask db upgrade')