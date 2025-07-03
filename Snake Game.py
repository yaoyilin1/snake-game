import pygame, sys, time, random

class Snake:
    """贪吃蛇类，管理蛇的身体、移动、增长等"""
    
    def __init__(self, init_pos=[100, 50]):
        self.pos = list(init_pos)  # 蛇头位置
        self.body = [[100, 50], [90, 50], [80, 50]]  # 蛇身坐标列表
        self.direction = 'RIGHT'  # 当前移动方向
        self.change_to = 'RIGHT'  # 待改变的方向
        
    def reset(self):
        """重置蛇到初始状态"""
        self.pos = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.change_to = 'RIGHT'
        
    def update_direction(self, new_direction):
        """更新移动方向，防止反向移动"""
        if new_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif new_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif new_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif new_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
            
    def move(self):
        """移动蛇头"""
        if self.direction == 'UP':
            self.pos[1] -= 10
        elif self.direction == 'DOWN':
            self.pos[1] += 10
        elif self.direction == 'LEFT':
            self.pos[0] -= 10
        elif self.direction == 'RIGHT':
            self.pos[0] += 10
            
    def grow(self, length_increase):
        """增长蛇身，在尾部延长"""
        tail = self.body[-1]
        for _ in range(length_increase - 1):
            self.body.append(list(tail))
            
    def update_body(self):
        """更新蛇身，头部跟随蛇头移动"""
        self.body.insert(0, list(self.pos))
        
    def shrink_tail(self):
        """缩短蛇尾"""
        self.body.pop()
        
    def check_self_collision(self):
        """检查是否撞到自己"""
        return any(self.pos[0] == block[0] and self.pos[1] == block[1] for block in self.body[1:])
        
    def check_boundary_collision(self, width, height):
        """检查是否撞到边界"""
        return (self.pos[0] < 0 or self.pos[0] > width-10 or 
                self.pos[1] < 0 or self.pos[1] > height-10)
        
    def check_collision_with_pos(self, pos):
        """检查是否与指定位置碰撞"""
        return self.pos[0] == pos[0] and self.pos[1] == pos[1]
        
    def get_length(self):
        """获取蛇的长度"""
        return len(self.body)

class Food:
    """食物类，管理食物的生成、类型、位置"""
    
    # 食物类型配置
    FOOD_TYPES = [
        {'name': 'small', 'color': (255,255,255), 'length': 1, 'prob': 0.6},   # 小食物，白色
        {'name': 'medium', 'color': (0,191,255), 'length': 3, 'prob': 0.3},    # 中食物，深天蓝
        {'name': 'large', 'color': (255,69,0), 'length': 5, 'prob': 0.1}       # 大食物，橙红色
    ]
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = [0, 0]
        self.type = self.FOOD_TYPES[0]  # 默认小食物
        self.spawn()
        
    def spawn(self, snake_body=None, obstacles=None, star_pos=None):
        """生成新食物"""
        # 按概率选择食物类型
        r = random.random()
        acc = 0
        for food_type in self.FOOD_TYPES:
            acc += food_type['prob']
            if r <= acc:
                self.type = food_type
                break
                
        # 生成不与蛇、障碍物、星星重叠的位置
        while True:
            pos = [random.randrange(1, (self.width//10)) * 10, 
                   random.randrange(1, (self.height//10)) * 10]
            if (snake_body is None or pos not in snake_body) and \
               (obstacles is None or pos not in obstacles) and \
               (star_pos is None or pos != star_pos):
                self.pos = pos
                break
                
    def get_message(self):
        """根据食物类型返回提示消息"""
        if self.type['name'] == 'large':
            return '哇！吃到大餐啦！'
        elif self.type['name'] == 'medium':
            return '中号美味，真不错！'
        else:
            return '小点心也不错~'

class Star:
    """星星奖励类，管理星星的生成、位置、计时"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = None
        self.timer = 0
        self.duration = 3000  # 星星存在时间（毫秒）
        self.spawn_probability = 0.01  # 每帧生成概率
        
    def maybe_spawn(self, snake_body, food_pos, obstacles):
        """可能生成星星奖励"""
        if self.pos is None and random.random() < self.spawn_probability:
            while True:
                pos = [random.randrange(1, (self.width//10)) * 10, 
                       random.randrange(1, (self.height//10)) * 10]
                if (pos not in snake_body and pos != food_pos and 
                    pos not in obstacles):
                    self.pos = pos
                    self.timer = pygame.time.get_ticks()
                    break
                    
    def update(self):
        """更新星星状态，超时则消失"""
        if self.pos is not None and pygame.time.get_ticks() - self.timer > self.duration:
            self.pos = None
            
    def collect(self):
        """收集星星"""
        self.pos = None

class Person:
    """小人类，管理单个小人的位置和移动"""
    
    def __init__(self, pos, direction):
        self.pos = list(pos)
        self.dir = list(direction)
        
    def move(self, obstacles, width, height):
        """移动小人"""
        new_x = self.pos[0] + self.dir[0]
        new_y = self.pos[1] + self.dir[1]
        
        # 检查边界和障碍物
        if (new_x < 0 or new_x > width-10 or new_y < 0 or new_y > height-10 or 
            [new_x, new_y] in obstacles):
            # 随机换方向
            self.dir = random.choice([(10,0),(-10,0),(0,10),(0,-10)])
        else:
            self.pos[0] = new_x
            self.pos[1] = new_y

class PersonManager:
    """小人管理器，管理所有小人"""
    
    def __init__(self, width, height, person_num=3):
        self.width = width
        self.height = height
        self.person_num = person_num
        self.persons = []
        self.move_interval = 10  # 移动间隔
        self.move_counter = 0
        self.init_persons()
        
    def init_persons(self):
        """初始化小人"""
        self.persons = []
        tries = 0
        while len(self.persons) < self.person_num and tries < 1000:
            tries += 1
            pos = [random.randrange(1, (self.width//10)) * 10, 
                   random.randrange(1, (self.height//10)) * 10]
            if pos not in [p.pos for p in self.persons]:
                direction = random.choice([(10,0),(-10,0),(0,10),(0,-10)])
                self.persons.append(Person(pos, direction))
                
    def update(self, obstacles):
        """更新所有小人位置"""
        self.move_counter += 1
        if self.move_counter >= self.move_interval:
            for person in self.persons:
                person.move(obstacles, self.width, self.height)
            self.move_counter = 0
            
    def check_collision(self, pos):
        """检查是否与指定位置碰撞"""
        return any(person.pos[0] == pos[0] and person.pos[1] == pos[1] 
                  for person in self.persons)

class ObstacleGroup:
    """障碍物组类，管理所有障碍物"""
    
    def __init__(self, width, height, obstacle_num=50, group_num=5):
        self.width = width
        self.height = height
        self.obstacle_num = obstacle_num
        self.group_num = group_num
        self.group_size = obstacle_num // group_num
        self.obstacles = []
        self.generate()
        
    def generate(self):
        """生成障碍物组"""
        self.obstacles = []
        tries = 0
        while len(self.obstacles) < self.obstacle_num and tries < 1000:
            tries += 1
            start_x = random.randrange(1, (self.width//10)-self.group_size) * 10
            start_y = random.randrange(1, (self.height//10)-self.group_size) * 10
            direction = random.choice(['H', 'V'])
            group = []
            for i in range(self.group_size):
                if direction == 'H':
                    pos = [start_x + i*10, start_y]
                else:
                    pos = [start_x, start_y + i*10]
                if pos in self.obstacles:
                    break
                group.append(pos)
            if len(group) == self.group_size:
                self.obstacles.extend(group)
            if len(self.obstacles) >= self.obstacle_num:
                break

class UIManager:
    """UI管理器，负责显示分数、生命、速度、长度、消息等"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.message = ''
        self.message_timer = 0
        self.message_duration = 2000
        
    def set_message(self, msg):
        """设置显示消息"""
        self.message = msg
        self.message_timer = pygame.time.get_ticks()
        
    def update_message(self):
        """更新消息状态，超时则清空"""
        if self.message and pygame.time.get_ticks() - self.message_timer > self.message_duration:
            self.message = ''
            
    def show_score(self, game_window, score, choice=1):
        """显示分数"""
        score_font = pygame.font.SysFont('consolas', 20)
        score_surface = score_font.render('Score : ' + str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (int(self.width/10), 15)
        else:
            score_rect.midtop = (int(self.width/2), int(self.height/1.25))
        game_window.blit(score_surface, score_rect)
        
    def show_lives(self, game_window, lives, choice=1):
        """显示生命值"""
        lives_font = pygame.font.SysFont('consolas', 20)
        lives_surface = lives_font.render('Lives : ' + str(lives), True, (255, 0, 0))
        lives_rect = lives_surface.get_rect()
        if choice == 1:
            lives_rect.midtop = (int(self.width*0.8), 15)
        else:
            lives_rect.midtop = (int(self.width/2), int(self.height/1.15))
        game_window.blit(lives_surface, lives_rect)
        
    def show_info(self, game_window, speed_level, snake_length):
        """显示速度和长度信息"""
        info_font = pygame.font.SysFont('consolas', 20)
        # 速度等级
        speed_surface = info_font.render(f'Speed Level: {speed_level}', True, (0, 0, 255))
        speed_rect = speed_surface.get_rect()
        speed_rect.topleft = (int(self.width*0.8), 40)
        game_window.blit(speed_surface, speed_rect)
        # 蛇长度
        length_surface = info_font.render(f'Length: {snake_length}', True, (0, 0, 255))
        length_rect = length_surface.get_rect()
        length_rect.midtop = (int(self.width/2), int(self.height/1.25)+30)
        game_window.blit(length_surface, length_rect)
        
    def show_message(self, game_window):
        """显示底部消息"""
        if self.message:
            msg_font = pygame.font.SysFont('simhei', 24)
            msg_surface = msg_font.render(self.message, True, (255, 0, 0))
            msg_rect = msg_surface.get_rect()
            msg_rect.midbottom = (int(self.width/2), self.height-10)
            # 消息框背景
            pygame.draw.rect(game_window, (30,30,30), (0, self.height-40, self.width, 40))
            game_window.blit(msg_surface, msg_rect)

class SnakeGameEngine:
    """贪吃蛇游戏主引擎，负责游戏主循环和整体调度"""
    
    # 游戏配置常量
    SPEED_LEVELS = [10, 15, 20, 25, 30, 40, 60, 90, 120]  # 9级速度
    MAX_LEVEL = 9  # 最大速度等级
    FRAME_WIDTH = 720
    FRAME_HEIGHT = 480
    
    def __init__(self):
        """初始化游戏引擎"""
        # 初始化PyGame
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')
            
        # 设置窗口
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.FRAME_WIDTH, self.FRAME_HEIGHT))
        
        # 颜色定义
        self.colors = {
            'black': pygame.Color(0, 0, 0),
            'white': pygame.Color(255, 255, 255),
            'red': pygame.Color(255, 0, 0),
            'green': pygame.Color(0, 255, 0),
            'blue': pygame.Color(0, 0, 255),
            'yellow': pygame.Color(255, 215, 0),
            'purple': pygame.Color(160, 32, 240)
        }
        
        # 游戏组件初始化
        self.snake = Snake()
        self.food = Food(self.FRAME_WIDTH, self.FRAME_HEIGHT)
        self.star = Star(self.FRAME_WIDTH, self.FRAME_HEIGHT)
        self.person_manager = PersonManager(self.FRAME_WIDTH, self.FRAME_HEIGHT)
        self.obstacles = ObstacleGroup(self.FRAME_WIDTH, self.FRAME_HEIGHT)
        self.ui = UIManager(self.FRAME_WIDTH, self.FRAME_HEIGHT)
        
        # 游戏状态
        self.score = 0
        self.lives = 3
        self.speed_level = 1
        self.last_speedup_time = pygame.time.get_ticks()
        self.running = True
        
        # 帧率控制
        self.fps_controller = pygame.time.Clock()
        
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
                
    def handle_keydown(self, key):
        """处理按键事件"""
        if key == pygame.K_UP or key == ord('w'):
            if self.snake.direction != 'UP':
                self.ui.set_message('紧急转弯！')
            self.snake.change_to = 'UP'
        elif key == pygame.K_DOWN or key == ord('s'):
            if self.snake.direction != 'DOWN':
                self.ui.set_message('紧急转弯！')
            self.snake.change_to = 'DOWN'
        elif key == pygame.K_LEFT or key == ord('a'):
            if self.snake.direction != 'LEFT':
                self.ui.set_message('紧急转弯！')
            self.snake.change_to = 'LEFT'
        elif key == pygame.K_RIGHT or key == ord('d'):
            if self.snake.direction != 'RIGHT':
                self.ui.set_message('紧急转弯！')
            self.snake.change_to = 'RIGHT'
        elif key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_r:
            self.obstacles.generate()
            self.ui.set_message('障碍物刷新啦！')
            
    def update_game_state(self):
        """更新游戏状态"""
        # 更新蛇的方向
        self.snake.update_direction(self.snake.change_to)
        
        # 移动蛇头
        self.snake.move()
        
        # 更新蛇身
        self.snake.update_body()
        
        # 检查是否吃到食物
        ate_food = False
        if self.snake.check_collision_with_pos(self.food.pos):
            self.score += 1
            self.snake.grow(self.food.type['length'])
            self.food.spawn(self.snake.body, self.obstacles.obstacles, self.star.pos)
            self.ui.set_message(self.food.get_message())
            ate_food = True
            
        # 检查是否吃到星星
        if self.star.pos and self.snake.check_collision_with_pos(self.star.pos):
            self.lives += 1
            self.star.collect()
            self.ui.set_message('获得一条新生命！')
            
        # 如果没有吃到食物，缩短蛇尾
        if not ate_food:
            self.snake.shrink_tail()
            
        # 更新星星状态
        self.star.maybe_spawn(self.snake.body, self.food.pos, self.obstacles.obstacles)
        self.star.update()
        
        # 更新小人位置
        self.person_manager.update(self.obstacles.obstacles)
        
        # 更新UI消息
        self.ui.update_message()
        
        # 速度提升
        now = pygame.time.get_ticks()
        if self.speed_level < self.MAX_LEVEL and now - self.last_speedup_time >= 60000:
            self.speed_level += 1
            self.last_speedup_time = now
            
    def check_collisions(self):
        """检查碰撞"""
        # 边界碰撞
        if self.snake.check_boundary_collision(self.FRAME_WIDTH, self.FRAME_HEIGHT):
            return 'boundary'
            
        # 自身碰撞
        if self.snake.check_self_collision():
            return 'self'
            
        # 障碍物碰撞
        if self.snake.pos in self.obstacles.obstacles:
            return 'obstacle'
            
        # 小人碰撞
        if self.person_manager.check_collision(self.snake.pos):
            return 'person'
            
        return None
        
    def handle_collision(self, collision_type):
        """处理碰撞"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over()
        else:
            self.snake.reset()
            if collision_type == 'person':
                self.ui.set_message('被小人抓住了！')
            time.sleep(1)
            
    def check_win_condition(self):
        """检查胜利条件"""
        if self.snake.get_length() >= 100:
            self.game_over(win=True)
            
    def draw(self):
        """绘制游戏画面"""
        # 填充背景
        self.game_window.fill(self.colors['black'])
        
        # 绘制蛇
        for pos in self.snake.body:
            pygame.draw.rect(self.game_window, self.colors['green'], 
                           pygame.Rect(pos[0], pos[1], 10, 10))
            
        # 绘制食物
        pygame.draw.rect(self.game_window, self.food.type['color'], 
                        pygame.Rect(self.food.pos[0], self.food.pos[1], 10, 10))
        
        # 绘制星星
        if self.star.pos:
            pygame.draw.rect(self.game_window, self.colors['yellow'], 
                           pygame.Rect(self.star.pos[0], self.star.pos[1], 10, 10))
        
        # 绘制障碍物
        for obs in self.obstacles.obstacles:
            pygame.draw.rect(self.game_window, self.colors['blue'], 
                           pygame.Rect(obs[0], obs[1], 10, 10))
        
        # 绘制小人
        for person in self.person_manager.persons:
            pygame.draw.rect(self.game_window, self.colors['purple'], 
                           pygame.Rect(person.pos[0], person.pos[1], 10, 10))
        
        # 绘制UI
        self.ui.show_score(self.game_window, self.score)
        self.ui.show_lives(self.game_window, self.lives)
        self.ui.show_info(self.game_window, self.speed_level, self.snake.get_length())
        self.ui.show_message(self.game_window)
        
    def game_over(self, win=False):
        """游戏结束"""
        my_font = pygame.font.SysFont('times new roman', 60)
        if win:
            msg = 'YOU WIN!'
            color = self.colors['blue']
        else:
            msg = 'YOU DIED'
            color = self.colors['red']
            
        game_over_surface = my_font.render(msg, True, color)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (int(self.FRAME_WIDTH/2), int(self.FRAME_HEIGHT/4))
        
        self.game_window.fill(self.colors['black'])
        self.game_window.blit(game_over_surface, game_over_rect)
        self.ui.show_score(self.game_window, self.score, 0)
        self.ui.show_lives(self.game_window, self.lives, 0)
        
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
        
    def run(self):
        """游戏主循环"""
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新游戏状态
            self.update_game_state()
            
            # 检查胜利条件
            self.check_win_condition()
            
            # 检查碰撞
            collision = self.check_collisions()
            if collision:
                self.handle_collision(collision)
                continue
                
            # 绘制画面
            self.draw()
            
            # 刷新显示
            pygame.display.update()
            
            # 控制帧率
            self.fps_controller.tick(self.SPEED_LEVELS[self.speed_level-1])

# 主程序入口
if __name__ == '__main__':
    engine = SnakeGameEngine()
    engine.run() 