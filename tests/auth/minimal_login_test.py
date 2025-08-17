import requests
import re

# 登录信息
host = 'http://localhost:5000'
username = 'root'
password = 'password'

# 创建会话
session = requests.Session()

try:
    # 1. 获取登录页面
    print("获取登录页面...")
    login_page = session.get(f'{host}/login')
    print(f"登录页面状态码: {login_page.status_code}")
    
    # 2. 提取CSRF令牌
    print("提取CSRF令牌...")
    csrf_token = re.search(r'<input\s+id="csrf_token"\s+name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', login_page.text).group(1)
    print(f"CSRF令牌: {csrf_token}")
    
    # 3. 提交登录请求
    print("提交登录请求...")
    login_response = session.post(
        f'{host}/login',
        data={
            'username': username,
            'password': password,
            'csrf_token': csrf_token,
            'submit': '登录'
        },
        headers={
            'Referer': f'{host}/login',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )
    print(f"登录响应状态码: {login_response.status_code}")
    print(f"登录后URL: {login_response.url}")
    
    # 4. 检查登录是否成功
    if '/login' not in login_response.url:
        print("登录成功！")
        print(f"登录后Cookie: {session.cookies}")
        # 尝试访问首页
        home_response = session.get(f'{host}/')
        print(f"首页状态码: {home_response.status_code}")
        print(f"首页内容预览: {home_response.text[:500]}...")
    else:
        print("登录失败！")
        print(f"响应内容预览: {login_response.text[:500]}...")
        # 检查是否有错误信息
        error = re.search(r'<div\s+class="alert\s+alert-danger"\s*>(.*?)</div>', login_response.text)
        if error:
            print(f"错误信息: {error.group(1)}")

except Exception as e:
    print(f"发生错误: {e}")