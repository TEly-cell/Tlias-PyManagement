# 设置编码为UTF-8
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding

# 清除之前的cookie
Remove-Item -Path .\cookies.txt -ErrorAction SilentlyContinue

# 获取CSRF令牌
Write-Host "获取CSRF令牌..."
$loginPage = Invoke-WebRequest -Uri http://localhost:5000/login -SessionVariable session
$csrfToken = $loginPage.ParsedHtml.getElementsByName("csrf_token")[0].value
Write-Host "CSRF令牌: $csrfToken"

# 测试登录状态检查API
Write-Host "
测试登录状态检查API..."
Invoke-WebRequest -Uri http://localhost:5000/api/check_login -WebSession $session

# 测试登录
Write-Host "
测试登录..."
# 确保使用正确的用户名和密码
$loginResult = Invoke-WebRequest -Uri http://localhost:5000/login -Method POST -Body @{"username"="admin"; "password"="password123"; "csrf_token"=$csrfToken} -WebSession $session -MaximumRedirection 0 -ErrorAction SilentlyContinue
Write-Host "登录状态码: $($loginResult.StatusCode)"
Write-Host "登录描述: $($loginResult.StatusDescription)"
Write-Host "登录响应头: $($loginResult.Headers)"
Write-Host "登录响应内容: $($loginResult.Content)"

# 检查会话状态
Write-Host "
检查会话状态..."
Write-Host "会话ID: $($session.SessionId)"
Write-Host "会话Cookie: $($session.Cookies)"

# 再次测试登录状态检查API
Write-Host "
再次测试登录状态检查API..."
$checkLoginResult = Invoke-WebRequest -Uri http://localhost:5000/api/check_login -WebSession $session
Write-Host "登录状态检查结果: $($checkLoginResult.StatusDescription)"
Write-Host "响应内容: $($checkLoginResult.Content)"

# 测试创建游戏API
Write-Host "
测试创建游戏API..."
$createGameResult = Invoke-WebRequest -Uri "http://localhost:5000/api/games/create?type=match3" -WebSession $session
Write-Host "创建游戏结果: $($createGameResult.StatusDescription)"
Write-Host "响应内容: $($createGameResult.Content)"

Write-Host "
测试完成，请按任意键退出..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')