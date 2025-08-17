@echo off
chcp 65001

:: 获取CSRF令牌
echo 获取CSRF令牌...
curl http://localhost:5000/login --cookie-jar cookies.txt > login_page.html
echo 提取CSRF令牌...
for /f "tokens=2 delims==" %%a in ('findstr /C:csrf_token login_page.html') do (
    set csrf_token=%%a
)
set csrf_token=%csrf_token:~1,-1%
echo CSRF令牌: %csrf_token%

echo.
echo 测试登录状态检查API...
curl http://localhost:5000/api/check_login --cookie cookies.txt

echo.
echo 测试登录...
curl -X POST http://localhost:5000/login --data "username=test&password=test&csrf_token=%csrf_token%" --cookie-jar cookies.txt --cookie cookies.txt

echo.
echo 再次测试登录状态检查API...
curl http://localhost:5000/api/check_login --cookie cookies.txt

echo.
echo 测试创建游戏API...
curl http://localhost:5000/api/games/create?type=match3 --cookie cookies.txt

del login_page.html
pause