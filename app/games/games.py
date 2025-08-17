import random
import json

games = {
    'snake': {
        'title': '贪吃蛇',
        'description': '经典的贪吃蛇游戏，控制蛇头吃食物，让蛇变得更长。'
    },
    'match3': {
        'title': '消消乐',
        'description': '交换相邻的方块，匹配三个或更多相同的方块进行消除。'
    }
}

class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        # 初始化蛇的位置和方向
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = 'right'
        self.next_direction = 'right'
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        # 生成食物的位置，确保不在蛇身上
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, new_direction):
        # 确保不能直接反向移动
        opposite_directions = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }
        if new_direction != opposite_directions.get(self.direction, ''):
            self.next_direction = new_direction

    def update(self):
        if self.game_over:
            return

        # 更新方向
        self.direction = self.next_direction

        # 获取蛇头位置
        head_x, head_y = self.snake[0]

        # 根据方向移动蛇头
        if self.direction == 'up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'right':
            new_head = (head_x + 1, head_y)

        # 检查是否撞墙
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return

        # 检查是否撞到自己
        if new_head in self.snake:
            self.game_over = True
            return

        # 移动蛇
        self.snake.insert(0, new_head)

        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # 如果没吃到食物，移除尾部
            self.snake.pop()

    def get_state(self):
        # 返回游戏状态
        return {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'width': self.width,
            'height': self.height
        }


class Match3Game:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.grid = []
        self.score = 0
        self.game_over = False
        self.reset()

    def reset(self):
        # 初始化游戏网格
        self.grid = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                # 随机生成1-5的方块类型
                row.append(random.randint(1, 5))
            self.grid.append(row)

        # 确保初始状态没有匹配
        while self.find_matches():
            self.resolve_matches()
            self.fill_empty_cells()

        self.score = 0
        self.game_over = False

    def find_matches(self):
        # 寻找匹配的方块
        matches = []

        # 检查水平匹配
        for y in range(self.height):
            x = 0
            while x < self.width - 2:
                if (self.grid[y][x] == self.grid[y][x+1] == self.grid[y][x+2] and
                    self.grid[y][x] != 0):
                    # 找到匹配，记录位置
                    match_length = 3
                    while x + match_length < self.width and self.grid[y][x] == self.grid[y][x+match_length]:
                        match_length += 1
                    for i in range(match_length):
                        matches.append((y, x + i))
                    x += match_length
                else:
                    x += 1

        # 检查垂直匹配
        for x in range(self.width):
            y = 0
            while y < self.height - 2:
                if (self.grid[y][x] == self.grid[y+1][x] == self.grid[y+2][x] and
                    self.grid[y][x] != 0):
                    # 找到匹配，记录位置
                    match_length = 3
                    while y + match_length < self.height and self.grid[y][x] == self.grid[y+match_length][x]:
                        match_length += 1
                    for i in range(match_length):
                        matches.append((y + i, x))
                    y += match_length
                else:
                    y += 1

        return matches

    def resolve_matches(self):
        # 处理匹配的方块
        matches = self.find_matches()
        if not matches:
            return False

        # 计算匹配的组数和奖励
        # 将匹配的方块按组分类（水平或垂直）
        match_groups = []
        processed = set()
        
        for y, x in matches:
            if (y, x) in processed:
                continue
                
            # 检查水平组
            horizontal_group = [(y, x)]
            # 向左检查
            left_x = x - 1
            while left_x >= 0 and (y, left_x) in matches and (y, left_x) not in processed:
                horizontal_group.append((y, left_x))
                processed.add((y, left_x))
                left_x -= 1
            # 向右检查
            right_x = x + 1
            while right_x < self.width and (y, right_x) in matches and (y, right_x) not in processed:
                horizontal_group.append((y, right_x))
                processed.add((y, right_x))
                right_x += 1
            
            # 检查垂直组
            vertical_group = [(y, x)]
            # 向上检查
            up_y = y - 1
            while up_y >= 0 and (up_y, x) in matches and (up_y, x) not in processed:
                vertical_group.append((up_y, x))
                processed.add((up_y, x))
                up_y -= 1
            # 向下检查
            down_y = y + 1
            while down_y < self.height and (down_y, x) in matches and (down_y, x) not in processed:
                vertical_group.append((down_y, x))
                processed.add((down_y, x))
                down_y += 1
            
            # 选择较大的组
            if len(horizontal_group) >= 3:
                match_groups.append(horizontal_group)
                for pos in horizontal_group:
                    processed.add(pos)
            elif len(vertical_group) >= 3:
                match_groups.append(vertical_group)
                for pos in vertical_group:
                    processed.add(pos)

        # 计算得分：基础分 + 组数奖励 + 长度奖励
        total_matched = len(matches)
        group_count = len(match_groups)
        
        base_score = total_matched * 50  # 提高基础分数
        group_bonus = group_count * 100  # 每组额外奖励
        length_bonus = 0
        
        # 长度奖励：超过3个的额外奖励
        for group in match_groups:
            if len(group) > 3:
                length_bonus += (len(group) - 3) * 30
        
        total_score = base_score + group_bonus + length_bonus
        
        # 增加分数并记录
        old_score = self.score
        self.score += total_score
        
        print(f"得分计算: 基础分{base_score} + 组奖励{group_bonus} + 长度奖励{length_bonus} = 总分{total_score}")
        print(f"总分数: {old_score} -> {self.score} (+{total_score})")

        # 移除匹配的方块
        for y, x in matches:
            self.grid[y][x] = 0

        return True

    def fill_empty_cells(self):
        # 填充空白格子
        for x in range(self.width):
            # 让方块下落
            for y in range(self.height-1, -1, -1):
                if self.grid[y][x] == 0:
                    # 找到上方最近的非零方块
                    for k in range(y-1, -1, -1):
                        if self.grid[k][x] != 0:
                            self.grid[y][x] = self.grid[k][x]
                            self.grid[k][x] = 0
                            break

            # 在顶部生成新方块
            for y in range(self.height):
                if self.grid[y][x] == 0:
                    self.grid[y][x] = random.randint(1, 5)

    def swap_cells(self, y1, x1, y2, x2):
        # 调试日志 - 详细记录交换过程
        print(f"\n===== 开始交换操作 =====")
        print(f"接收到的参数: y1={y1}, x1={x1}, y2={y2}, x2={x2}")
        print(f"网格尺寸: {self.width}x{self.height}")
        
        # 转换参数为整数并添加错误处理
        try:
            y1 = int(y1)
            x1 = int(x1)
            y2 = int(y2)
            x2 = int(x2)
            print(f"参数转换成功: y1={y1}, x1={x1}, y2={y2}, x2={x2}")
        except ValueError:
            # 参数不是有效整数
            print("错误: 参数不是有效整数")
            return False

        # 检查坐标是否在有效范围内
        if not (0 <= y1 < self.height and 0 <= x1 < self.width and 0 <= y2 < self.height and 0 <= x2 < self.width):
            print(f"错误: 坐标超出范围: 网格大小 {self.width}x{self.height}, 坐标1=({x1},{y1}), 坐标2=({x2},{y2})")
            return False
        print(f"坐标验证通过: 均在网格范围内")

        # 检查方块是否相邻
        if (abs(y1 - y2) + abs(x1 - x2) != 1):
            print(f"错误: 方块不相邻: 坐标1=({x1},{y1}), 坐标2=({x2},{y2})")
            return False
        print(f"方块相邻验证通过")

        # 记录交换前的值
        val1 = self.grid[y1][x1]
        val2 = self.grid[y2][x2]
        print(f"交换前值: 坐标1=({x1},{y1})={val1}, 坐标2=({x2},{y2})={val2}")

        # 执行交换
        self.grid[y1][x1], self.grid[y2][x2] = val2, val1
        print(f"交换后值: 坐标1=({x1},{y1})={self.grid[y1][x1]}, 坐标2=({x2},{y2})={self.grid[y2][x2]}")

        # 检查是否有匹配
        matches = self.find_matches()
        if not matches:
            # 如果没有匹配，交换回来
            self.grid[y1][x1], self.grid[y2][x2] = val1, val2
            print(f"错误: 没有找到匹配，交换已撤销。交换前值已恢复")
            return False
        else:
            print(f"成功: 找到 {len(matches)} 个匹配方块，交换有效")

        # 处理匹配
        print("开始处理匹配...")
        self.resolve_matches()
        self.fill_empty_cells()
        print(f"匹配处理完成，当前分数: {self.score}")

        # 检查是否还有匹配
        while self.resolve_matches():
            print("发现连锁匹配，继续处理...")
            self.fill_empty_cells()
        print("所有匹配处理完毕")

        print("===== 交换操作结束 =====")
        return True

    def get_state(self):
        # 返回游戏状态
        return {
            'grid': self.grid,
            'score': self.score,
            'game_over': self.game_over,
            'width': self.width,
            'height': self.height
        }

# 创建游戏实例字典
active_games = {}

def create_game(game_type, game_id, width=None, height=None):
    if game_type == 'snake':
        active_games[game_id] = SnakeGame(width=width, height=height)
    elif game_type == 'match3':
        active_games[game_id] = Match3Game(width=width, height=height)
    return game_id

def get_game(game_id):
    return active_games.get(game_id)

def update_game(game_id, action=None):
    game = get_game(game_id)
    if not game:
        return {'success': False, 'error': '游戏不存在'}

    if isinstance(game, SnakeGame):
        if action in ['up', 'down', 'left', 'right']:
            game.change_direction(action)
        game.update()
        game_state = game.get_state()
        game_state['success'] = True
        return game_state
    elif isinstance(game, Match3Game):
        if isinstance(action, dict) and action.get('action') == 'swap':
            # 通过字典参数传递坐标
            x1 = action.get('x1')
            y1 = action.get('y1')
            x2 = action.get('x2')
            y2 = action.get('y2')
            
            # 调试日志：打印接收到的坐标及其类型
            print(f"从前端接收的坐标: x1={x1} ({type(x1)}), y1={y1} ({type(y1)}), x2={x2} ({type(x2)}), y2={y2} ({type(y2)})")

            # 验证坐标参数是否存在（不使用all()因为0是有效的坐标值）
            if x1 is None or y1 is None or x2 is None or y2 is None:
                print("错误: 缺少坐标参数")
                return {'success': False, 'error': '缺少坐标参数'}
            
            try:
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
            except ValueError:
                print("错误: 坐标参数不是有效整数")
                return {'success': False, 'error': '坐标参数不是有效整数'}
            
            # 调用swap_cells方法，参数顺序是(y, x)
            print(f"调用swap_cells方法: y1={y1}, x1={x1}, y2={y2}, x2={x2}")
            swap_result = game.swap_cells(y1, x1, y2, x2)
            print(f"交换结果: {'成功' if swap_result else '失败'}")
            # 在游戏状态中添加交换结果
            game_state = game.get_state()
            game_state['success'] = swap_result
            if not swap_result:
                print(f"交换失败: y1={y1}, x1={x1}, y2={y2}, x2={x2}")
                game_state['error'] = '交换失败，可能是因为方块不相邻或没有匹配'
            return game_state
        else:
            # 非交换操作
            game_state = game.get_state()
            game_state['success'] = True
            return game_state

    # 默认返回
    game_state = game.get_state()
    game_state['success'] = True
    return game_state

def reset_game(game_id):
    game = get_game(game_id)
    if game:
        game.reset()
        return game.get_state()
    return None

def get_game_state(game_id):
    """获取游戏状态
    
    Args:
        game_id: 游戏ID（字符串格式）
        
    Returns:
        游戏状态字典，如果游戏不存在返回None
    """
    game = get_game(game_id)
    if game:
        state = game.get_state()
        state['success'] = True
        return state
    return None