import requests
import re

# 登录信息
username = 'root'
password = 'password'

# 创建会话
session = requests.Session()

# 1. 访问首页获取初始Cookie
home_response = session.get('http://localhost:5000/')
print(f"首页响应状态码: {home_response.status_code}")
print(f"首页Cookie: {session.cookies}")

# 2. 获取登录页面
dev_response = session.get('http://localhost:5000/login', headers={'User-Agent': 'Mozilla/5.0'})
print(f"登录页面响应状态码: {dev_response.status_code}")

# 3. 从HTML中提取CSRF令牌
csrf_token_match = re.search(r'<input\s+id="csrf_token"\s+name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', dev_response.text)
csrf_token = csrf_token_match.group(1) if csrf_token_match else None
print(f"提取的CSRF令牌: {csrf_token}")

# 4. 准备登录数据
login_data = {
    'username': username,
    'password': password,
    'csrf_token': csrf_token,
    'submit': '登录'
}

# 5. 发送登录请求
login_response = session.post(
    'http://localhost:5000/login',
    data=login_data,
    headers={
        'Referer': 'http://localhost:5000/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    },
    allow_redirects=True
)

# 6. 检查登录结果
print(f"登录响应状态码: {login_response.status_code}")
print(f"登录后最终URL: {login_response.url}")
print(f"登录后Cookie: {session.cookies}")

if '/login' not in login_response.url:
    print("登录成功！")
    # 尝试访问受保护页面
    profile_response = session.get('http://localhost:5000/profile')
    print(f"个人资料页面响应状态码: {profile_response.status_code}")
    print(f"个人资料页面内容: {profile_response.text[:500]}...")
else:
    print("登录失败！")
    print(f"登录响应内容: {login_response.text[:500]}...")