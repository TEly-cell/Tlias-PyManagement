@echo off
chcp 65001

:: 测试登录状态检查API
 echo 测试登录状态检查API...
curl http://localhost:5000/api/check_login --cookie-jar cookies.txt

:: 测试登录
 echo.
echo 测试登录...
curl -X POST http://localhost:5000/login --data "username=admin&password=password123&csrf_token=test_token" --cookie-jar cookies.txt --cookie cookies.txt

:: 再次测试登录状态检查API
 echo.
echo 再次测试登录状态检查API...
curl http://localhost:5000/api/check_login --cookie cookies.txt

:: 测试创建游戏API
 echo.
echo 测试创建游戏API...
curl http://localhost:5000/api/games/create?type=match3 --cookie cookies.txt

pause