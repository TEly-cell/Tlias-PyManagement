from app import app, db
from app import User
from werkzeug.security import generate_password_hash

# 应用上下文
with app.app_context():
    # 获取所有用户
    users = User.query.all()
    
    # 更新每个用户的密码哈希
    for user in users:
        # 假设当前password_hash字段存储的是明文密码
        plain_password = user.password_hash
        # 生成新的哈希
        new_hash = generate_password_hash(plain_password)
        # 更新用户的password_hash
        user.password_hash = new_hash
        print(f'更新用户 {user.username} 的密码哈希')
    
    # 提交更改
    db.session.commit()
    print('所有用户的密码哈希已更新完成')