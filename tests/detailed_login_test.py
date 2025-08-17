import requests
import re
import urllib.parse

# 登录信息
username = 'root'
password = 'password'

# 创建会话
session = requests.Session()
# 设置用户代理
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'})

# 1. 访问首页
print("=== 访问首页 ===")
home_response = session.get('http://localhost:5000/')
print(f"状态码: {home_response.status_code}")
print(f"URL: {home_response.url}")
print(f"Cookie: {session.cookies}")
print(f"响应头: {home_response.headers}")
print(f"响应内容长度: {len(home_response.text)}")

# 2. 访问登录页面
print("\n=== 访问登录页面 ===")
login_page_response = session.get('http://localhost:5000/login')
print(f"状态码: {login_page_response.status_code}")
print(f"URL: {login_page_response.url}")
print(f"Cookie: {session.cookies}")
print(f"响应头: {login_page_response.headers}")

# 3. 提取CSRF令牌
print("\n=== 提取CSRF令牌 ===")
csrf_token_match = re.search(r'<input\s+id="csrf_token"\s+name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', login_page_response.text)
csrf_token = csrf_token_match.group(1) if csrf_token_match else None
print(f"CSRF令牌: {csrf_token}")

# 4. 准备登录数据
print("\n=== 准备登录数据 ===")
login_data = {
    'username': username,
    'password': password,
    'csrf_token': csrf_token,
    'submit': '登录'
}
print(f"登录数据: {login_data}")

# 5. 发送登录请求
print("\n=== 发送登录请求 ===")
login_response = session.post(
    'http://localhost:5000/login',
    data=login_data,
    headers={
        'Referer': 'http://localhost:5000/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://localhost:5000',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    },
    allow_redirects=True
)

# 6. 检查登录结果
print("\n=== 登录结果 ===")
print(f"状态码: {login_response.status_code}")
print(f"最终URL: {login_response.url}")
print(f"Cookie: {session.cookies}")
print(f"响应头: {login_response.headers}")

if '/login' not in login_response.url:
    print("登录成功！")
    # 尝试访问受保护页面
    profile_response = session.get('http://localhost:5000/profile')
    print(f"个人资料页面状态码: {profile_response.status_code}")
    print(f"个人资料页面URL: {profile_response.url}")
    print(f"个人资料页面内容: {profile_response.text[:500]}...")
else:
    print("登录失败！")
    # 检查响应中是否有错误信息
    error_match = re.search(r'<div\s+class="alert\s+alert-danger"\s*>(.*?)</div>', login_response.text)
    if error_match:
        print(f"错误信息: {error_match.group(1)}")
    else:
        print(f"响应内容: {login_response.text[:500]}...")

# 7. 尝试直接访问游戏页面
print("\n=== 尝试访问游戏页面 ===")
game_response = session.get('http://localhost:5000/game')
print(f"状态码: {game_response.status_code}")
print(f"URL: {game_response.url}")
print(f"响应内容长度: {len(game_response.text)}")