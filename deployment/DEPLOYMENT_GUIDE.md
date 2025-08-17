# 项目部署指南

## 部署方案选择

### 方案1：PythonAnywhere（推荐新手）

**步骤：**

1. **注册账号**
   - 访问 https://www.pythonanywhere.com
   - 注册免费账号

2. **上传代码**
   - 使用GitHub集成或手动上传
   - 确保包含所有文件

3. **配置Web应用**
   - Source code: `/home/yourusername/PyManagement`
   - Working directory: `/home/yourusername/PyManagement`
   - WSGI configuration file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

4. **安装依赖**
   - 在Bash控制台运行：
   ```bash
   pip install --user -r requirements.txt
   ```

5. **配置数据库**
   - PythonAnywhere提供MySQL数据库
   - 修改配置使用生产数据库

### 方案2：Heroku部署

**步骤：**

1. **准备Heroku配置**
   ```bash
   # 安装Heroku CLI
   # 登录Heroku
   heroku login
   
   # 创建Heroku应用
   heroku create your-app-name
   
   # 添加数据库
   heroku addons:create heroku-postgresql:hobby-dev
   ```

2. **创建必要文件**
   - Procfile
   - runtime.txt

3. **部署**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### 方案3：Railway部署（现代推荐）

**步骤：**

1. **注册Railway**
   - 访问 https://railway.app
   - 连接GitHub仓库

2. **一键部署**
   - Railway会自动检测Python项目
   - 自动配置数据库和依赖

## 生产环境配置

### 1. 环境变量设置

创建生产环境变量：

```bash
# .env.production
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=your-production-db-url
SERVER_NAME=your-domain.com
```

### 2. 数据库迁移

```bash
# 初始化迁移
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. 静态文件处理

对于生产环境，需要配置静态文件服务：

```python
# 在配置中添加
app.config['STATIC_FOLDER'] = 'static'
```

## 具体部署步骤

### PythonAnywhere详细步骤

1. **文件上传**
   ```bash
   # 在本地项目目录
   git archive --format=zip HEAD -o PyManagement.zip
   ```

2. **数据库配置**
   ```python
   # 修改config.py
   class ProductionConfig(Config):
       SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
           'mysql+mysqlconnector://username:password@host/database'
   ```

3. **WSGI配置**
   ```python
   # /var/www/yourusername_pythonanywhere_com_wsgi.py
   import sys
   import os
   
   path = '/home/yourusername/PyManagement'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['FLASK_ENV'] = 'production'
   os.environ['SECRET_KEY'] = 'your-secret-key'
   
   from run import app as application
   ```

### Heroku详细步骤

1. **创建必要文件**

   **Procfile**
   ```
   web: gunicorn run:app
   ```

   **runtime.txt**
   ```
   python-3.12.0
   ```

2. **配置环境变量**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   ```

3. **部署命令**
   ```bash
   git add Procfile runtime.txt
   git commit -m "Add Heroku deployment files"
   git push heroku main
   heroku run flask db upgrade
   ```

## 安全注意事项

1. **环境变量**
   - 永远不要提交敏感信息到Git
   - 使用环境变量存储敏感配置

2. **HTTPS**
   - 所有平台都支持自动HTTPS
   - 确保在生产环境启用

3. **数据库安全**
   - 使用强密码
   - 限制数据库访问权限

4. **CSRF保护**
   - 确保WTF_CSRF_ENABLED=True

## 监控和日志

### 1. 日志配置

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### 2. 错误处理

```python
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
```

## 性能优化

1. **数据库索引**
   - 确保常用查询字段有索引

2. **静态文件压缩**
   - 使用CDN服务
   - 启用gzip压缩

3. **缓存**
   - 考虑使用Redis缓存

## 故障排除

### 常见问题

1. **数据库连接错误**
   - 检查DATABASE_URL格式
   - 确保数据库服务运行

2. **静态文件404**
   - 检查STATIC_FOLDER路径
   - 确保文件权限正确

3. **CSRF令牌错误**
   - 检查SECRET_KEY设置
   - 确保HTTPS配置正确

### 调试命令

```bash
# 查看日志
heroku logs --tail

# 数据库检查
heroku pg:info

# 运行诊断
heroku run python -c "from run import app; print(app.config)"
```

## 域名配置

### 自定义域名

1. **PythonAnywhere**
   - 在Web标签页配置自定义域名
   - 添加CNAME记录指向yourusername.pythonanywhere.com

2. **Heroku**
   ```bash
   heroku domains:add www.yourdomain.com
   ```

3. **Railway**
   - 在Settings中添加自定义域名
   - 配置DNS CNAME记录

## 备份策略

1. **数据库备份**
   ```bash
   # PostgreSQL
   heroku pg:backups:capture
   
   # MySQL (PythonAnywhere)
   mysqldump -u username -p database > backup.sql
   ```

2. **文件备份**
   - 定期备份上传文件
   - 使用云存储服务

## 总结

推荐部署顺序：
1. **新手**：PythonAnywhere（免费且简单）
2. **现代**：Railway（GitHub集成好）
3. **专业**：Heroku（功能强大）

选择最适合你需求的方案，按照对应步骤操作即可成功部署！