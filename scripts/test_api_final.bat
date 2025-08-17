@echo off
chcp 65001

:: 清理旧文件
if exist cookies.txt del cookies.txt
if exist login_page.html del login_page.html

:: 获取CSRF令牌
echo 获取CSRF令牌...
curl http://localhost:5000/login -o login_page.html --cookie-jar cookies.txt

:: 提取CSRF令牌
for /f "tokens=2 delims==" %%a in ('findstr /C:csrf_token login_page.html') do (
    set csrf_token=%%a
)
set csrf_token=%csrf_token:~1,-1%
echo CSRF令牌: %csrf_token%

:: 测试登录状态检查API
 echo.
echo 测试登录状态检查API...
curl http://localhost:5000/api/check_login --cookie cookies.txt

:: 测试登录
 echo.
echo 测试登录...
curl -X POST http://localhost:5000/login --data "username=admin&password=password123&csrf_token=%csrf_token%" --cookie-jar cookies.txt --cookie cookies.txt

:: 再次测试登录状态检查API
 echo.
echo 再次测试登录状态检查API...
curl http://localhost:5000/api/check_login --cookie cookies.txt

:: 测试创建游戏API
 echo.
echo 测试创建游戏API...
curl http://localhost:5000/api/games/create?type=match3 --cookie cookies.txt

:: 清理临时文件
del login_page.html

pause