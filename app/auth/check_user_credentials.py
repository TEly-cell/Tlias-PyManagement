import sqlite3
import hashlib
import os

# 连接到数据库
def check_database_users():
    db_path = os.path.join(os.path.dirname(__file__), 'tlias.db')
    print(f"连接到数据库: {db_path}")

    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 查询用户表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        table_exists = cursor.fetchone()

        if not table_exists:
            print("错误: 用户表不存在")
            return

        # 查询所有用户
        cursor.execute("SELECT id, username, email, password_hash FROM user")
        users = cursor.fetchall()

        if not users:
            print("数据库中没有用户记录")
            print("建议: 创建一个新用户账户")
            return

        print(f"找到 {len(users)} 个用户记录:")
        for user in users:
            user_id, username, email, password_hash = user
            print(f"\n用户ID: {user_id}")
            print(f"用户名: {username}")
            print(f"邮箱: {email}")
            print(f"密码哈希: {password_hash}")
            print("-" * 50)

        print("\n提示: 如果您不知道用户密码，可以尝试重置密码")
        print("使用以下命令创建一个新用户或重置现有用户密码:")
        print("python update_user_passwords.py")

    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if conn:
            conn.close()

# 运行检查
if __name__ == '__main__':
    check_database_users()