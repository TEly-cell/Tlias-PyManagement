import requests
from bs4 import BeautifulSoup

def test_login_credentials(username, password):
    # 创建会话
    session = requests.Session()
    print(f"=== 测试登录凭据: {username}/{password} ===")

    # 访问登录页面获取CSRF令牌
    login_url = 'http://localhost:5000/login'
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    # 准备登录数据
    login_data = {
        'username': username,
        'password': password,
        'csrf_token': csrf_token,
        'submit': '登录'
    }

    # 发送登录请求
    response = session.post(login_url, data=login_data, allow_redirects=True)

    # 检查是否登录成功
    if '/dashboard' in response.url:
        print("✅ 登录成功! 已重定向到仪表盘")
        print(f"登录后URL: {response.url}")
        return True
    else:
        print("❌ 登录失败!")
        print(f"登录后URL: {response.url}")
        # 检查是否有错误消息
        soup = BeautifulSoup(response.text, 'html.parser')
        errors = soup.find_all('div', class_='flash')
        if errors:
            print("错误消息:")
            for error in errors:
                print(f"- {error.text.strip()}")
        return False


def test_multiple_credentials():
    # 测试多组凭据
    credentials = [
        ('test', 'test'),  # 假设的测试账户
        ('admin', 'admin'),  # 假设的管理员账户
        ('user', 'password')  # 假设的普通用户账户
    ]

    for username, password in credentials:
        if test_login_credentials(username, password):
            print(f"✅ 找到有效的凭据: {username}/{password}")
            return
    print("❌ 没有找到有效的凭据")


if __name__ == '__main__':
    test_multiple_credentials()