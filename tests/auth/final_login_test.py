import requests
from bs4 import BeautifulSoup
import time
import re

def test_login():
    # 创建会话
    session = requests.Session()
    print("=== 开始登录测试 ===")

    # 访问登录页面获取CSRF令牌
    login_url = 'http://localhost:5000/login'
    print(f"访问登录页面: {login_url}")
    response = session.get(login_url)
    print(f"登录页面响应状态码: {response.status_code}")
    print(f"登录页面响应URL: {response.url}")
    print(f"登录页面Cookie: {session.cookies}")

    # 提取CSRF令牌
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    print(f"提取到的CSRF令牌: {csrf_token}")

    # 准备登录数据
    login_data = {
        'username': 'test',
        'password': 'test',
        'csrf_token': csrf_token,
        'submit': '登录'
    }
    print(f"登录数据: {login_data}")

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': login_url,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 发送登录请求
    print("发送登录请求...")
    response = session.post(login_url, data=login_data, headers=headers, allow_redirects=True)
    print(f"登录响应状态码: {response.status_code}")
    print(f"登录响应URL: {response.url}")
    print(f"登录后Cookie: {session.cookies}")
    print(f"登录响应头: {response.headers}")

    # 检查是否登录成功
    if '/dashboard' in response.url:
        print("登录成功! 已重定向到仪表盘")
        # 测试访问需要登录的API
        test_api(session)
    elif '/login' in response.url:
        print("登录失败! 仍在登录页面")
        # 检查是否有错误消息
        soup = BeautifulSoup(response.text, 'html.parser')
        errors = soup.find_all('div', class_='flash')
        if errors:
            print("错误消息:")
            for error in errors:
                print(f"- {error.text.strip()}")
        else:
            print("没有找到明确的错误消息")
            # 打印部分响应内容以调试
            print("响应内容预览 (前500字符):")
            print(response.text[:500])
    else:
        print(f"登录后重定向到未知页面: {response.url}")


def test_api(session):
    print("=== 测试访问受保护的API ===")
    # 测试检查登录状态API
    check_login_url = 'http://localhost:5000/api/check_login'
    response = session.get(check_login_url)
    print(f"检查登录状态API响应: {response.status_code}")
    print(f"响应内容: {response.json()}")

    # 测试创建游戏API
    create_game_url = 'http://localhost:5000/api/games/create?type=snake'
    response = session.get(create_game_url)
    print(f"创建游戏API响应: {response.status_code}")
    if response.status_code == 200:
        game_id = response.json().get('game_id')
        print(f"创建的游戏ID: {game_id}")
    else:
        print(f"创建游戏失败: {response.text}")


if __name__ == '__main__':
    test_login()