import requests
from bs4 import BeautifulSoup

# 创建会话
session = requests.Session()

# 获取登录页面
print("获取登录页面...")
login_page = session.get('http://localhost:5000/login')

# 使用BeautifulSoup解析HTML并获取CSRF令牌
print("提取CSRF令牌...")
soup = BeautifulSoup(login_page.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
print(f"CSRF令牌: {csrf_token}")

# 测试登录状态检查API
print("\n测试登录状态检查API...")
check_login_response = session.get('http://localhost:5000/api/check_login')
print(f"登录状态检查响应: {check_login_response.status_code}")
print(f"响应内容: {check_login_response.text}")

# 测试登录
print("\n测试登录...")
login_data = {
    'username': 'admin',
    'password': 'password123',
    'csrf_token': csrf_token
}
login_response = session.post('http://localhost:5000/login', data=login_data)
print(f"登录响应: {login_response.status_code}")
print(f"响应内容: {login_response.text[:500]}...")  # 只显示前500个字符

# 再次测试登录状态检查API
print("\n再次测试登录状态检查API...")
check_login_response_after = session.get('http://localhost:5000/api/check_login')
print(f"登录状态检查响应: {check_login_response_after.status_code}")
print(f"响应内容: {check_login_response_after.text}")

# 测试创建游戏API
print("\n测试创建游戏API...")
create_game_response = session.get('http://localhost:5000/api/games/create?type=match3')
print(f"创建游戏响应: {create_game_response.status_code}")
print(f"响应内容: {create_game_response.text}")

print("\n测试完成。")