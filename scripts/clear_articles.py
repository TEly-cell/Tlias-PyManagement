import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
from app.models import ArticleTutorial

app = create_app()
with app.app_context():
    # 清空所有文章数据
    db.session.query(ArticleTutorial).delete()
    db.session.commit()
    print("已成功清空所有文章数据")