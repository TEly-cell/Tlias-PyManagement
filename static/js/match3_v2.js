// 全局游戏对象
// 全局游戏实例
let match3Game = null;

// 确保页面加载完成后初始化游戏
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGame);
} else {
    // 页面已经加载完成，直接初始化
    setTimeout(initializeGame, 100);
}

// 初始化游戏函数
function initializeGame() {
    console.log('页面加载完成，初始化消消乐游戏...');
    if (!match3Game) {
        match3Game = new Match3Game();
        console.log('游戏初始化完成');
        console.log('提示: 若游戏未自动开始，可在控制台输入 initializeMatch3Game() 手动启动');
    } else {
        console.log('游戏实例已存在，跳过初始化');
    }
}

// 全局初始化函数，方便手动调用
window.initializeMatch3Game = function() {
    initializeGame();
}

// 测试开始按钮函数
window.testStartButton = function() {
    if (match3Game && match3Game.initGame) {
        console.log('测试开始按钮点击...');
        match3Game.initGame();
    } else {
        console.error('游戏实例未初始化或没有initGame方法');
    }
}

// 获取CSRF令牌
function getCSRFToken() {
    // 尝试从cookie中获取
    const cookieRow = document.cookie
        .split('; ') 
        .find(row => row.startsWith('XSRF-TOKEN='));
    const cookieValue = cookieRow ? cookieRow.split('=')[1] : null;
    
    if (cookieValue) {
        return decodeURIComponent(cookieValue);
    }
    
    // 尝试从meta标签中获取
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag) {
        return metaTag.getAttribute('content');
    }
    
    console.warn('未找到CSRF令牌');
    return null;
}

class Match3Game {
    constructor() {
        console.log('========== 创建Match3Game实例 ==========');
        // 游戏状态
        this.gameId = null;
        this.gameState = null;
        this.selectedCell = null;
        this.cellSize = 0;
        this.isProcessing = false;
        this.bypassLogin = false;

        // DOM 元素
        this.gameGrid = document.getElementById('game-grid');
        this.scoreElement = document.getElementById('score');
        this.startBtn = document.getElementById('start-btn');
        this.resetBtn = document.getElementById('reset-btn');

        console.log('查找DOM元素结果:');
        console.log('gameGrid:', this.gameGrid);
        console.log('scoreElement:', this.scoreElement);
        console.log('startBtn:', this.startBtn);
        console.log('resetBtn:', this.resetBtn);

        // 绑定事件
        this.bindEvents();
    }

    // 绑定事件监听器
    bindEvents() {
        console.log('========== 开始绑定事件 ==========');
        // 重新获取按钮元素，确保DOM已经加载完成
        this.startBtn = document.getElementById('start-btn');
        this.resetBtn = document.getElementById('reset-btn');

        console.log('查找按钮元素结果:');
        console.log('startBtn:', this.startBtn);
        console.log('resetBtn:', this.resetBtn);

        if (this.startBtn) {
            console.log('成功找到开始按钮，绑定点击事件...');
            // 使用箭头函数确保this上下文正确
            this.startBtn.addEventListener('click', () => this.initGame());
            console.log('开始按钮事件绑定完成');
            // 添加样式变化，确认按钮已激活
            this.startBtn.style.backgroundColor = '#4CAF50';
            this.startBtn.style.cursor = 'pointer';
        } else {
            console.error('未找到开始按钮元素! 检查HTML中是否存在id为start-btn的元素');
            alert('错误: 未找到开始按钮，请刷新页面重试');
            // 创建一个临时按钮用于调试
            this.createDebugStartButton();
        }

        if (this.resetBtn) {
            console.log('成功找到重置按钮，绑定点击事件...');
            this.resetBtn.addEventListener('click', () => this.resetGame());
            console.log('重置按钮事件绑定完成');
        } else {
            console.error('未找到重置按钮元素! 检查HTML中是否存在id为reset-btn的元素');
        }

        // 键盘事件支持
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && this.startBtn) {
                console.log('按下Enter键，触发开始游戏...');
                this.startBtn.click();
            }
        });
        console.log('========== 事件绑定完成 ==========');
    }

    // 创建调试用的开始按钮
    createDebugStartButton() {
        console.warn('创建调试用的开始按钮...');
        const debugBtn = document.createElement('button');
        debugBtn.id = 'debug-start-btn';
        debugBtn.className = 'btn-morandi-primary btn-lg fw-bold';
        debugBtn.textContent = '调试开始游戏';
        debugBtn.style.position = 'fixed';
        debugBtn.style.top = '20px';
        debugBtn.style.right = '20px';
        debugBtn.style.zIndex = '1000';
        debugBtn.addEventListener('click', () => this.initGame());
        document.body.appendChild(debugBtn);
    }

    // 初始化游戏
    async initGame() {
        console.log('========== 开始初始化游戏 ==========');
        this.gameId = null;
        this.gameState = null;
        this.selectedCell = null;
        this.scoreElement.textContent = '0';
        this.isProcessing = false;

        try {
            // 检查登录状态
            console.log('检查用户登录状态...');
            const isLoggedIn = await this.checkLoginStatus();
            console.log('登录状态检查结果:', isLoggedIn);

            if (isLoggedIn) {
                console.log('用户已登录，继续创建游戏...');
                // 请求创建游戏
                const gameData = await this.createGame();
                console.log('创建游戏响应:', gameData);
                if (gameData && gameData.game_id) {
                    this.gameId = gameData.game_id;
                    console.log('获取到游戏ID:', this.gameId);
                    // 获取游戏状态
                    await this.updateGameState();
                } else {
                    console.error('创建游戏响应中没有game_id字段!');
                    alert('创建游戏失败: 无效的游戏数据');
                }
            } else {
                console.error('用户未登录，无法创建游戏!');
                // 为了调试方便，添加一个绕过登录的选项
                if (confirm('您未登录，无法创建游戏。是否尝试绕过登录限制？')) {
                    console.log('绕过登录检查，直接创建游戏...');
                    // 直接创建游戏
                    const gameData = await this.createGame();
                    console.log('创建游戏响应:', gameData);
                    if (gameData && gameData.game_id) {
                        this.gameId = gameData.game_id;
                        console.log('获取到游戏ID:', this.gameId);
                        // 获取游戏状态
                        await this.updateGameState();
                    } else {
                        console.error('创建游戏响应中没有game_id字段!');
                        alert('创建游戏失败: 无效的游戏数据');
                    }
                } else {
                    window.location.href = '/login';
                }
            }
        } catch (error) {
            console.error('初始化游戏失败:', error);
            alert('初始化游戏失败，请重试: ' + error.message);
        }
    }

    // 检查登录状态
    async checkLoginStatus() {
        console.log('========== 检查登录状态 ==========');
        console.log('bypassLogin:', this.bypassLogin);
        if (this.bypassLogin) {
            console.log('绕过登录检查，直接返回true');
            return true;
        }
        try {
            console.log('发送登录状态检查请求...');
            const response = await fetch('/api/check_login', {
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log('登录状态检查响应状态:', response.status);

            if (!response.ok) {
                throw new Error(`登录状态检查失败! 状态码: ${response.status}`);
            }

            const data = await response.json();
            console.log('登录状态检查响应数据:', data);
            return data.logged_in;
        } catch (error) {
            console.error('检查登录状态失败:', error);
            // 为了调试方便，在开发环境下返回true
            console.log('开发环境下绕过登录检查，返回true');
            return true;
        }
    }

    // 创建游戏
    async createGame() {
        console.log('========== 创建游戏 ==========');
        try {
            const csrfToken = getCSRFToken();
            console.log('CSRF Token:', csrfToken);
            console.log('发送创建游戏请求...');
            const response = await fetch('/api/games/create?type=match3', {
                credentials: 'same-origin',
                headers: {
                    'X-CSRF-Token': csrfToken
                }
            });
            console.log('创建游戏响应状态:', response.status);

            if (!response.ok) {
                throw new Error(`创建游戏失败! 状态码: ${response.status}`);
            }

            const data = await response.json();
            console.log('创建游戏响应数据:', data);
            return data;
        } catch (error) {
            console.error('创建游戏失败:', error);
            throw error;
        }
    }

    // 更新游戏状态
    async updateGameState(action = null) {
        if (!this.gameId) {
            console.error('没有游戏ID');
            return;
        }

        try {
            this.isProcessing = true;
            let url = `/api/games/${this.gameId}/state`;
            if (action) {
                url += `?action=${action}`;
            }

            console.log('更新游戏状态:', url);
            const response = await fetch(url, {
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`获取游戏状态失败! 状态码: ${response.status}`);
            }

            const data = await response.json();
            console.log('游戏状态更新成功:', data);

            if (data) {
                this.gameState = data;
                
                // 验证游戏状态数据
                if (!data || !data.grid) {
                    console.error('游戏状态数据格式错误:', data);
                    alert('游戏数据格式错误，请重试');
                    return;
                }
                
                console.log('游戏网格尺寸:', data.grid.length, 'x', data.grid[0]?.length || 0);
                
                this.renderGame();
                this.updateScore();
                this.selectedCell = null; // 交换后清除选择
                
                // 显示游戏已准备好的提示
                if (this.gameState && this.gameState.grid) {
                    console.log('游戏已准备就绪，可以开始点击方块了！');
                    // 添加视觉提示
                    this.showReadyMessage();
                }
            }
        } catch (error) {
            console.error('更新游戏状态失败:', error);
            alert('游戏操作失败，请重试: ' + error.message);
        } finally {
            this.isProcessing = false;
        }
    }

    // 显示游戏就绪提示
    showReadyMessage() {
        const message = document.createElement('div');
        message.textContent = '游戏已就绪！点击相邻的两个方块进行交换';
        message.style.position = 'fixed';
        message.style.top = '50%';
        message.style.left = '50%';
        message.style.transform = 'translate(-50%, -50%)';
        message.style.backgroundColor = 'rgba(76, 175, 80, 0.9)';
        message.style.color = 'white';
        message.style.padding = '15px 20px';
        message.style.borderRadius = '8px';
        message.style.zIndex = '1000';
        message.style.fontSize = '16px';
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 2000);
    }

    // 渲染游戏
    renderGame() {
        if (!this.gameState || !this.gameState.grid) {
            console.error('游戏状态或网格为空，无法渲染');
            return;
        }

        console.log('渲染游戏网格:', this.gameState.grid);
        console.log('游戏网格容器:', this.gameGrid);
        
        // 验证游戏网格容器是否存在
        if (!this.gameGrid) {
            console.error('游戏网格容器未找到！检查DOM中是否存在id为game-grid的元素');
            return;
        }

        // 清空游戏网格
        this.gameGrid.innerHTML = '';

        // 设置网格样式
        const gridSize = this.gameState.grid.length;
        this.gameGrid.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`;
        this.gameGrid.style.gridTemplateRows = `repeat(${gridSize}, 1fr)`;

        // 计算格子大小 - 使用实际容器宽度
        const gameArea = document.getElementById('game-area');
        const containerWidth = Math.min(600, gameArea.clientWidth || window.innerWidth - 40);
        this.cellSize = Math.floor(containerWidth / gridSize); // 使用完整宽度
        console.log('容器宽度:', containerWidth, '格子大小:', this.cellSize);

        // 渲染网格
        const { grid } = this.gameState;
        let cellCount = 0;
        grid.forEach((row, y) => {
            row.forEach((cellType, x) => {
                const cell = document.createElement('div');
                cell.className = `game-cell game-cell-type-${cellType}`;
                cell.dataset.x = x;
                cell.dataset.y = y;
                cell.style.width = `${this.cellSize}px`;
                cell.style.height = `${this.cellSize}px`;
                
                // 添加数字标签用于调试
                cell.setAttribute('title', `方块 (${x},${y}) 类型: ${cellType}`);

                if (cellType !== 0) {
                    // 添加点击事件
                    cell.addEventListener('click', () => this.handleCellClick(x, y));
                    cell.style.cursor = 'pointer';
                    cellCount++;
                } else {
                    cell.style.visibility = 'hidden';
                }

                this.gameGrid.appendChild(cell);
            });
        });

        console.log(`已渲染 ${cellCount} 个可点击的方块`);
        
        // 验证点击事件是否绑定成功
        const cells = this.gameGrid.querySelectorAll('.game-cell');
        console.log('游戏网格中的总格子数:', cells.length);
    }

    // 处理格子点击
    handleCellClick(x, y) {
        console.log('点击格子:', x, y);

        if (this.isProcessing) {
            console.log('正在处理中，请等待...');
            return;
        }

        if (!this.gameState) {
            console.error('游戏状态为空!');
            alert('游戏未初始化，请先点击开始游戏');
            return;
        }

        // 添加点击效果
        const cell = document.querySelector(`.game-cell[data-x=\"${x}\"][data-y=\"${y}\"]`);
        if (!cell) return;

        // 第一次选择
        if (!this.selectedCell) {
            this.selectedCell = { x, y };
            this.highlightCell(x, y);
            console.log('第一次选择:', this.selectedCell);
        } else if (this.selectedCell.x === x && this.selectedCell.y === y) {
            // 取消选择
            this.unhighlightCell(x, y);
            this.selectedCell = null;
            console.log('取消选择');
        } else {
            // 第二次选择，检查是否相邻
            if (this.isAdjacent(this.selectedCell.x, this.selectedCell.y, x, y)) {
                console.log('相邻格子，尝试交换');
                // 交换格子
                this.swapCells(this.selectedCell.x, this.selectedCell.y, x, y);
            } else {
                // 不相邻，取消第一次选择，选择新格子
                this.unhighlightCell(this.selectedCell.x, this.selectedCell.y);
                this.selectedCell = { x, y };
                this.highlightCell(x, y);
                console.log('取消上次选择，新选择:', this.selectedCell);
            }
        }
    }

    // 检查格子是否相邻
    isAdjacent(x1, y1, x2, y2) {
        const dx = Math.abs(x1 - x2);
        const dy = Math.abs(y1 - y2);
        return (dx === 1 && dy === 0) || (dx === 0 && dy === 1);
    }

    // 交换格子
    async swapCells(x1, y1, x2, y2) {
        this.isProcessing = true;
        this.showLoadingIndicator();

        try {
            // 发送交换请求到服务器
            // 注意：参数顺序需要匹配Python的swap_cells方法，即(y, x)格式
            console.log(`发送交换请求: game_id=${this.gameId}, y1=${y1}, x1=${x1}, y2=${y2}, x2=${x2}`);
            const response = await fetch(`/api/games/swap?game_id=${this.gameId}&y1=${y1}&x1=${x1}&y2=${y2}&x2=${x2}`, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'X-CSRF-Token': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`交换失败! 状态码: ${response.status}`);
            }

            const data = await response.json();
            console.log('交换结果:', data);

            if (data.success) {
                // 交换成功
                this.highlightSwapSuccess(x1, y1, x2, y2);
                // 更新游戏状态
                await this.updateGameState();
            } else {
                // 交换失败
                console.log('交换无效，没有匹配的三个相同元素');
                // 取消选择
                this.unhighlightCell(x1, y1);
                this.selectedCell = null;
            }
        } catch (error) {
            console.error('交换失败:', error);
            alert('交换失败，请重试: ' + error.message);
        } finally {
            this.hideLoadingIndicator();
            this.isProcessing = false;
        }
    }

    // 高亮选中的格子
    highlightCell(x, y) {
        const cell = document.querySelector(`.game-cell[data-x=\"${x}\"][data-y=\"${y}\"]`);
        if (cell) {
            cell.classList.add('selected');
        }
    }

    // 取消高亮
    unhighlightCell(x, y) {
        const cell = document.querySelector(`.game-cell[data-x="${x}"][data-y="${y}"]`);
        if (cell) {
            cell.classList.remove('selected');
        }
    }

    // 高亮交换成功效果
    highlightSwapSuccess(x1, y1, x2, y2) {
        const cell1 = document.querySelector(`.game-cell[data-x=\"${x1}\"][data-y=\"${y1}\"]`);
        const cell2 = document.querySelector(`.game-cell[data-x=\"${x2}\"][data-y=\"${y2}\"]`);
        
        if (cell1 && cell2) {
            // 先清除之前的动画类
            cell1.classList.remove('消除-animation');
            cell2.classList.remove('消除-animation');
            
            // 强制重绘
            void cell1.offsetWidth;
            void cell2.offsetWidth;
            
            // 添加消除动画类
            cell1.classList.add('eliminate-animation');
            cell2.classList.add('eliminate-animation');
        }
    }

    // 更新分数
    updateScore() {
        if (this.gameState) {
            const newScore = this.gameState.score;
            const oldScore = parseInt(this.scoreElement.textContent) || 0;
            
            // 创建得分动画效果
            this.animateScoreChange(oldScore, newScore);
            
            // 更新显示
            this.scoreElement.textContent = newScore;
            
            // 添加得分提示
            if (newScore > oldScore) {
                this.showScorePopup(newScore - oldScore);
            }
        }
    }

    // 分数变化动画
    animateScoreChange(oldScore, newScore) {
        const scoreContainer = this.scoreElement.parentElement;
        
        // 添加高亮效果
        scoreContainer.style.transition = 'transform 0.3s ease';
        scoreContainer.style.transform = 'scale(1.2)';
        
        // 恢复原始大小
        setTimeout(() => {
            scoreContainer.style.transform = 'scale(1)';
        }, 300);
        
        // 添加颜色变化
        if (newScore > oldScore) {
            scoreContainer.style.color = '#28a745';
            setTimeout(() => {
                scoreContainer.style.color = '';
            }, 1000);
        }
    }

    // 显示得分弹窗
    showScorePopup(points) {
        const popup = document.createElement('div');
        popup.textContent = `+${points}`;
        popup.style.position = 'fixed';
        popup.style.top = '30%';
        popup.style.left = '50%';
        popup.style.transform = 'translate(-50%, -50%)';
        popup.style.fontSize = '24px';
        popup.style.fontWeight = 'bold';
        popup.style.color = '#28a745';
        popup.style.zIndex = '1001';
        popup.style.pointerEvents = 'none';
        popup.style.animation = 'score-popup 1.5s ease-out forwards';
        
        // 添加动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes score-popup {
                0% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                50% { opacity: 1; transform: translate(-50%, -60%) scale(1.2); }
                100% { opacity: 0; transform: translate(-50%, -70%) scale(0.8); }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(popup);
        
        // 移除弹窗
        setTimeout(() => {
            if (popup.parentNode) {
                popup.parentNode.removeChild(popup);
            }
            if (style.parentNode) {
                style.parentNode.removeChild(style);
            }
        }, 1500);
    }

    // 重置游戏
    async resetGame() {
        console.log('重置游戏...');
        if (this.gameId) {
            try {
                this.isProcessing = true;
                this.showLoadingIndicator();
                const response = await fetch(`/api/games/reset?game_id=${this.gameId}`);

                if (!response.ok) {
                    throw new Error(`重置游戏失败! 状态码: ${response.status}`);
                }

                const data = await response.json();
                console.log('游戏重置成功:', data);
                this.gameState = data;
                this.renderGame();
                this.updateScore();
                this.selectedCell = null; // 重置选择
            } catch (error) {
                console.error('重置游戏失败:', error);
                alert('游戏重置失败，请重试: ' + error.message);
            } finally {
                this.hideLoadingIndicator();
                this.isProcessing = false;
            }
        } else {
            // 如果没有游戏ID，直接初始化游戏
            this.initGame();
        }
    }

    // 显示加载指示器
    showLoadingIndicator() {
        let indicator = document.getElementById('loading-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'loading-indicator';
            indicator.style.position = 'fixed';
            indicator.style.top = '50%';
            indicator.style.left = '50%';
            indicator.style.transform = 'translate(-50%, -50%)';
            indicator.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            indicator.style.color = 'white';
            indicator.style.padding = '15px 25px';
            indicator.style.borderRadius = '5px';
            indicator.style.zIndex = '1000';
            indicator.textContent = '交换中...';
            document.body.appendChild(indicator);
        } else {
            indicator.style.display = 'block';
        }
    }

    // 隐藏加载指示器
    hideLoadingIndicator() {
        const indicator = document.getElementById('loading-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }
}

// 页面加载完成后初始化游戏
initializeGame();

// 全局初始化函数，确保在全局作用域可用
window.initializeMatch3Game = function(bypassLogin = true) {
    console.log('========== 手动初始化消消乐游戏 ==========');
    console.log('bypassLogin:', bypassLogin);
    if (!match3Game) {
        match3Game = new Match3Game();
    } else {
        console.log('游戏实例已存在，重置游戏');
    }
    match3Game.bypassLogin = bypassLogin;
    match3Game.initGame();
    return match3Game;
};

// 添加一个可见的调试按钮到页面
function addDebugButton() {
    console.log('添加调试按钮到页面...');
    const debugButton = document.createElement('button');
    debugButton.id = 'debug-initialize-game';
    debugButton.textContent = '手动初始化游戏';
    debugButton.style.position = 'fixed';
    debugButton.style.top = '20px';
    debugButton.style.right = '20px';
    debugButton.style.zIndex = '1000';
    debugButton.style.padding = '10px 20px';
    debugButton.style.backgroundColor = '#ff9800';
    debugButton.style.color = 'white';
    debugButton.style.border = 'none';
    debugButton.style.borderRadius = '5px';
    debugButton.style.cursor = 'pointer';
    debugButton.onclick = function() {
        initializeMatch3Game();
    };
    document.body.appendChild(debugButton);
}

// 页面加载完成后添加调试按钮
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addDebugButton);
} else {
    addDebugButton();
}

// 添加一个简单的调试按钮，直接在控制台输出信息
console.log('消消乐游戏脚本已加载');
console.log('可在控制台调用 initializeMatch3Game() 手动初始化游戏');
console.log('可在控制台调用 testStartButton() 测试开始按钮');

// 测试开始按钮的函数
window.testStartButton = function() {
    console.log('========== 测试开始按钮 ==========');
    const startButton = document.getElementById('start-btn');
    console.log('找到开始按钮:', startButton);
    if (startButton) {
        console.log('触发开始按钮点击事件...');
        startButton.click();
    } else {
        console.error('未找到开始按钮!');
    }
};