import requests
import re
import uuid

# 登录信息
username = 'root'
password = 'password'

# 创建会话
session = requests.Session()

# 访问首页获取初始Cookie
home_response = session.get('http://localhost:5000/')
print(f"首页响应状态码: {home_response.status_code}")
print(f"首页Cookie: {session.cookies}")

# 获取登录页面
login_page_response = session.get('http://localhost:5000/login')
print(f"登录页面响应状态码: {login_page_response.status_code}")

# 从HTML表单中提取CSRF令牌（使用更精确的正则表达式）
csrf_token_match = re.search(r'<input\s+id="csrf_token"\s+name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', login_page_response.text)
csrf_token = csrf_token_match.group(1) if csrf_token_match else None
print(f"提取的CSRF令牌: {csrf_token}")

# 登录
login_data = {
    'username': username,
    'password': password
}

# 如果获取到CSRF令牌，则添加到登录数据中
if csrf_token:
    login_data['csrf_token'] = csrf_token

login_response = session.post(
    'http://localhost:5000/login',
    data=login_data,
    headers={
        'Referer': 'http://localhost:5000/login',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
)

print(f"登录状态码: {login_response.status_code}")
print(f"登录响应内容: {login_response.text[:500]}...")
print(f"登录后的Cookie: {session.cookies}")

# 检查是否登录成功（访问一个需要登录的页面）
profile_response = session.get('http://localhost:5000/profile')
print(f"个人资料页面响应状态码: {profile_response.status_code}")

# 生成随机游戏ID
game_id = str(uuid.uuid4())
print(f"生成的游戏ID: {game_id}")

# 创建游戏
create_game_response = session.get(
    f'http://localhost:5000/api/games/create?type=match3&game_id={game_id}'
)

print(f"创建游戏状态码: {create_game_response.status_code}")
print(f"创建游戏响应内容: {create_game_response.text[:500]}...")

try:
    # 尝试解析JSON响应
    response_json = create_game_response.json()
    print(f"解析JSON成功: {response_json}")
    game_id = response_json.get('game_id')
    if game_id:
        print(f"获取到游戏ID: {game_id}")
except Exception as e:
    print(f"解析JSON失败: {e}")