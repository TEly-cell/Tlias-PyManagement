import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.abspath('.'))

from app import app, db
from app import DiscussionThread, DiscussionReply

# 创建应用上下文并创建表
with app.app_context():
    db.create_all()
    print('讨论区相关表创建成功!')