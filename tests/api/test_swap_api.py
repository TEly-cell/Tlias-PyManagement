import requests
import re
import uuid

# 登录信息
username = 'root'
password = 'password123'  # 使用重置后的正确密码

# 创建会话
session = requests.Session()

# 访问首页获取初始Cookie
home_response = session.get('http://localhost:5000/')
print(f"首页响应状态码: {home_response.status_code}")
print(f"首页Cookie: {session.cookies}")

# 获取登录页面
login_page_response = session.get('http://localhost:5000/login')
print(f"登录页面响应状态码: {login_page_response.status_code}")

# 从HTML表单中提取CSRF令牌（使用BeautifulSoup更可靠）
from bs4 import BeautifulSoup
soup = BeautifulSoup(login_page_response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})['value'] if soup.find('input', {'name': 'csrf_token'}) else None
print(f"提取的CSRF令牌: {csrf_token}")

# 登录
login_data = {
    'username': username,
    'password': password,
    'submit': '登录'
}

if csrf_token:
    login_data['csrf_token'] = csrf_token
    print(f"添加CSRF令牌到登录数据: {csrf_token}")
else:
    print("未找到CSRF令牌，无法添加到登录数据")

print(f"登录数据: {login_data}")

login_response = session.post(
    'http://localhost:5000/login',
    data=login_data,
    headers={
        'Referer': 'http://localhost:5000/login',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    allow_redirects=True  # 自动跟随重定向
)

print(f"登录响应状态码: {login_response.status_code}")
print(f"登录后最终URL: {login_response.url}")
print(f"登录后Cookie: {session.cookies}")

# 检查登录是否成功
if '/login' not in login_response.url:
    print("登录成功！")
    # 尝试访问游戏页面 (使用正确的match3游戏URL)
    game_response = session.get('http://localhost:5000/game/match3')
    print(f"游戏页面响应状态码: {game_response.status_code}")

    # 注意：match3.html模板中没有CSRF令牌字段，我们将使用登录时获取的CSRF令牌
    print(f"使用登录时获取的CSRF令牌: {csrf_token}")

    # 尝试创建游戏（使用正确的API参数）
    create_game_url = f'http://localhost:5000/api/games/create?type=match3'
    create_game_headers = {
        'X-CSRF-Token': csrf_token,
        'Referer': 'http://localhost:5000/game/match3'
    }
    create_game_response = session.get(create_game_url, headers=create_game_headers)
    print(f"创建游戏状态码: {create_game_response.status_code}")
    print(f"创建游戏响应内容: {create_game_response.text[:500]}...")

    # 解析创建游戏响应，获取游戏ID
    try:
        create_game_data = create_game_response.json()
        game_id = create_game_data.get('game_id')
        print(f"从响应中获取的游戏ID: {game_id}")
    except ValueError:
        print("无法解析创建游戏响应为JSON")
        game_id = None

    # 创建游戏后添加短暂延迟，确保游戏已初始化
    import time
    time.sleep(1)

    # 使用与前端相同的/api/games/swap路由执行交换操作
    # 重置swap_url为基础URL
    swap_url = 'http://localhost:5000/api/games/swap'
    if game_id:
        # 尝试不同的坐标组合 (垂直相邻方块)，注意：参数顺序与前端完全匹配
        # 注意：后端期望的参数名称是x1、y1、x2、y2，但在调用swap_cells方法时，参数顺序是(y1, x1, y2, x2)
        # 尝试交换第三行中相邻的两个1方块 (row=2, column=5 和 row=2, column=6)
        swap_params = {
            'game_id': game_id,
            'x1': 5,  # 对应后端的y1 (row=5)
            'y1': 2,  # 对应后端的x1 (column=2)
            'x2': 6,  # 对应后端的y2 (row=6)
            'y2': 2   # 对应后端的x2 (column=2)
        }
        print(f"交换请求参数: {swap_params}")
        # 打印游戏ID以确认它被正确设置
        print(f"游戏ID: {game_id}")
        # 确保所有参数都有值
        print(f"参数检查: x1={swap_params.get('x1')}, y1={swap_params.get('y1')}, x2={swap_params.get('x2')}, y2={swap_params.get('y2')}")
        print(f"交换请求参数: {swap_params}")
    else:
        # 尝试不同的坐标组合 (同一行相邻方块)
        swap_params = {
            'game_id': 'test_game_id',
            'action': 'swap',
            'x1': 0,
            'y1': 0,
            'x2': 0,
            'y2': 1
        }
        print("未获取到有效游戏ID，使用测试ID")
    # 使用简单的请求头
    swap_headers = {
        'X-CSRF-Token': csrf_token,
        'Referer': 'http://localhost:5000/game/match3'
    }
    # 使用POST请求，参数通过params参数传递
    swap_response = session.post(swap_url, params=swap_params, headers=swap_headers)
    # 打印完整的请求URL和参数
    print(f"完整请求URL: {swap_response.url}")

    # 打印响应
    print(f'交换请求URL: {swap_url}')
    print(f'交换响应状态码: {swap_response.status_code}')
    print(f'交换响应内容: {swap_response.text}')
else:
    print("登录失败！")
    print(f"登录响应内容: {login_response.text[:500]}...")