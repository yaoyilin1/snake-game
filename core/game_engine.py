import pygame, sys, time

# 导入所有游戏组件
from .snake import Snake
from entities.food import Food
from entities.star import Star
from entities.person import PersonManager
from entities.obstacles import ObstacleGroup
from ui.ui_manager import UIManager

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