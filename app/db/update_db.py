from app import app, db
from app import Material, LearningGoal
from sqlalchemy import text

with app.app_context():
    # 检查Material表结构
    inspector = db.inspect(db.engine)
    columns = inspector.get_columns('material')
    column_names = [col['name'] for col in columns]

    # 检查并添加duration列
    if 'duration' not in column_names:
        with db.engine.connect() as conn:
            with conn.begin():
                conn.execute(text('ALTER TABLE material ADD COLUMN duration INTEGER'))
        print('已成功添加duration列到material表')
    else:
        print('duration列已存在')

    # 检查并添加difficulty列
    if 'difficulty' not in column_names:
        with db.engine.connect() as conn:
            with conn.begin():
                conn.execute(text('ALTER TABLE material ADD COLUMN difficulty INTEGER'))
        print('已成功添加difficulty列到material表')
    else:
        print('difficulty列已存在')

    # 检查并添加tags列
    if 'tags' not in column_names:
        with db.engine.connect() as conn:
            with conn.begin():
                conn.execute(text('ALTER TABLE material ADD COLUMN tags VARCHAR(200)'))
        print('已成功添加tags列到material表')
    else:
        print('tags列已存在')

    # 检查并添加file_path列
    if 'file_path' not in column_names:
        with db.engine.connect() as conn:
            with conn.begin():
                conn.execute(text('ALTER TABLE material ADD COLUMN file_path VARCHAR(200)'))
        print('已成功添加file_path列到material表')
    else:
        print('file_path列已存在')

    # 确保所有表结构都已更新
    db.create_all()
    print('数据库表结构已更新')