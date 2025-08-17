from app import db
import sqlite3

# 连接到数据库
conn = sqlite3.connect('tlias.db')
cursor = conn.cursor()

# 检查并删除临时表
try:
    cursor.execute('DROP TABLE IF EXISTS _alembic_tmp_user')
    conn.commit()
    print('临时表 _alembic_tmp_user 已成功删除')
except Exception as e:
    print(f'删除临时表时出错: {e}')
finally:
    conn.close()