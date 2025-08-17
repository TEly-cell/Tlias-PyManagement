import requests

# 创建会话
session = requests.Session()

# 获取登录页面
response = session.get('http://localhost:5000/login')

print(f"响应状态码: {response.status_code}")
print(f"Cookie: {session.cookies}")

# 保存页面内容到文件
with open('login_page.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("登录页面HTML已保存到login_page.html文件")