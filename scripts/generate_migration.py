import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

# 初始化Flask应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\develop\\Python\\PyManagement\\app\\data\\tlias.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 导入数据库和模型
from app.db import db
from app.models import User, Course, Material, Progress, LearningPreference, LearningGoal, FavoriteCourse, Favorite, Task, DiscussionThread, DiscussionReply

db.init_app(app)

# 初始化Flask-Migrate
from flask_migrate import Migrate
migrate = Migrate(app, db)

# 创建应用上下文
with app.app_context():
    # 确保数据库目录存在
    db_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    os.makedirs(db_dir, exist_ok=True)
    
    # 直接配置Alembic生成迁移
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config('migrations/alembic.ini')
    alembic_cfg.attributes['engine'] = db.engine
    alembic_cfg.attributes['target_metadata'] = db.metadata

    command.revision(alembic_cfg, message='InitialAllModels', autogenerate=True)