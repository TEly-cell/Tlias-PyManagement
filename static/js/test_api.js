// 测试API交互功能
console.log('测试脚本已加载');

// 测试登录状态检查
function testLoginStatus() {
    console.log('测试登录状态检查...');
    fetch('/api/check_login')
        .then(response => response.json())
        .then(data => {
            console.log('登录状态检查结果:', data);
            document.getElementById('login-status').textContent = `登录状态: ${data.logged_in ? '已登录' : '未登录'}`;
        })
        .catch(error => console.error('登录状态检查失败:', error));
}

// 测试创建游戏
function testCreateGame() {
    console.log('测试创建游戏...');
    // 确保用户已登录
    fetch('/api/check_login')
        .then(response => response.json())
        .then(loginData => {
            if (!loginData.logged_in) {
                console.log('用户未登录，无法创建游戏');
                document.getElementById('game-status').textContent = '错误: 用户未登录';
                return;
            }

            fetch('/api/games/create?type=match3')
                .then(response => response.json())
                .then(data => {
                    console.log('创建游戏结果:', data);
                    document.getElementById('game-status').textContent = `游戏已创建，ID: ${data.game_id}`;
                    window.gameId = data.game_id;
                })
                .catch(error => console.error('创建游戏失败:', error));
        })
        .catch(error => console.error('登录状态检查失败:', error));
}

// 页面加载完成后执行测试
window.onload = function() {
    console.log('页面加载完成，准备执行测试');
    // 添加按钮事件
    document.getElementById('test-login').addEventListener('click', testLoginStatus);
    document.getElementById('test-create-game').addEventListener('click', testCreateGame);
}