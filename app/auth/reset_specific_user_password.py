from app import app, db
from app import User
from werkzeug.security import generate_password_hash
import sys

def reset_user_password(username, new_password):
    with app.app_context():
        # 查找用户
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"错误: 未找到用户 '{username}'")
            return False

        # 更新密码
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        print(f"成功重置用户 '{username}' 的密码")
        print(f"新密码: {new_password}")
        return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python reset_specific_user_password.py <用户名> <新密码>")
        print("示例: python reset_specific_user_password.py root password123")
    else:
        username = sys.argv[1]
        new_password = sys.argv[2]
        reset_user_password(username, new_password)