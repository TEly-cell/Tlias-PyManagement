from app import app, db
from app import Material

with app.app_context():
    # 打印Material表的列名
    print('Material表列名:')
    for column in Material.__table__.columns:
        print(f'{column.name}: {column.type}')

    # 检查是否有任何未提交的迁移
    from flask_migrate import upgrade
    try:
        upgrade()
        print('数据库迁移已应用')
    except Exception as e:
        print(f'迁移检查错误: {e}')