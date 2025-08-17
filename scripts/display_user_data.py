import sqlite3
import os

# 获取数据库路径
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'data', 'tlias.db'))

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 查询用户数据
    cursor.execute("SELECT id, username, email, created_at FROM user;")
    users = cursor.fetchall()
    
    # 获取列名
    columns = [desc[0] for desc in cursor.description]
    
    # 打印表头
    print("\n用户数据列表:\n")
    print(f"{columns[0]:<6} {columns[1]:<15} {columns[2]:<30} {columns[3]:<20}")
    print("-" * 70)
    if users:
        for user in users:
            print(f"{user[0]:<6} {user[1]:<15} {user[2]:<30} {user[3]:<20}")
    else:
        print("没有找到用户数据。")
except Exception as e:
    print(f"查询出错: {e}")
finally:
    # 关闭连接
    conn.close()