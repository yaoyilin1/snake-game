import pygame, sys, time

# 导入所有游戏组件
from .snake import Snake
from entities.food import Food
from entities.star import Star
from entities.person import PersonManager
from entities.obstacles import ObstacleGroup
from ui.ui_manager import UIManager
from config import ConfigManager
from utils.sprite_manager import SpriteManager

class SnakeGameEngine:
    """贪吃蛇游戏主引擎，负责游戏主循环和整体调度"""
    
    def __init__(self, config_file=None):
        """初始化游戏引擎"""
        # 加载配置
        self.config = ConfigManager(config_file) if config_file else ConfigManager()
        
        # 从配置获取游戏常量
        window_config = self.config.get_window_config() or {}
        speed_config = self.config.get_speed_config() or {}
        gameplay_config = self.config.get_gameplay_config() or {}
        
        self.SPEED_LEVELS = speed_config.get('levels', [10, 15, 20, 25, 30, 40, 60, 90, 120])
        self.MAX_LEVEL = speed_config.get('max_level', 9)
        self.GAME_WIDTH = window_config.get('game_width', 720)
        self.GAME_HEIGHT = window_config.get('game_height', 480)
        self.UI_HEIGHT = window_config.get('ui_height', 80)
        self.FRAME_WIDTH = self.GAME_WIDTH
        self.FRAME_HEIGHT = self.GAME_HEIGHT + self.UI_HEIGHT
        self.WIN_CONDITION = gameplay_config.get('win_condition_length', 100)
        self.SPEEDUP_INTERVAL = speed_config.get('speedup_interval', 60000)
        
        # 初始化PyGame
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')
            
        # 设置窗口
        window_title = window_config.get('title', 'Snake Eater')
        pygame.display.set_caption(window_title)
        self.game_window = pygame.display.set_mode((self.FRAME_WIDTH, self.FRAME_HEIGHT))
        
        # 从配置获取颜色
        self.colors = self.config.get_colors_dict()
        
        # 初始化精灵管理器
        self.sprite_manager = SpriteManager(self.config)
        
        # 游戏组件初始化（使用配置参数）
        self.snake = Snake(self.config)
        self.food = Food(self.GAME_WIDTH, self.GAME_HEIGHT, self.config)
        self.star = Star(self.GAME_WIDTH, self.GAME_HEIGHT)
        self.person_manager = PersonManager(self.GAME_WIDTH, self.GAME_HEIGHT)
        self.obstacles = ObstacleGroup(self.GAME_WIDTH, self.GAME_HEIGHT)
        self.ui = UIManager(self.FRAME_WIDTH, self.FRAME_HEIGHT, self.GAME_HEIGHT, 
                           self.config, self.sprite_manager)
        
        # 游戏状态（从配置获取初始值）
        self.score = 0
        self.lives = gameplay_config.get('initial_lives', 3)
        self.speed_level = 1
        self.last_speedup_time = pygame.time.get_ticks()
        self.running = True
        
        # 帧率控制
        fps_limit = window_config.get('fps_limit', 60)
        self.fps_controller = pygame.time.Clock()
        
        # 加载控制配置
        self.controls = self.config.get_controls_config() or {}
        self.messages = self.config.get_messages_config() or {}
        
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
                
    def handle_keydown(self, key):
        """处理按键事件（基于配置）"""
        key_name = pygame.key.name(key).upper()
        
        # 获取控制配置
        up_keys = self.controls.get('up_keys', ['UP', 'w'])
        down_keys = self.controls.get('down_keys', ['DOWN', 's'])
        left_keys = self.controls.get('left_keys', ['LEFT', 'a'])
        right_keys = self.controls.get('right_keys', ['RIGHT', 'd'])
        exit_key = self.controls.get('exit_key', 'ESCAPE')
        refresh_key = self.controls.get('refresh_key', 'r')
        
        # 获取消息配置
        turn_message = self.messages.get('turn_message', '紧急转弯！')
        refresh_message = self.messages.get('obstacle_refresh', '障碍物刷新啦！')
        
        if key_name in [k.upper() for k in up_keys]:
            if self.snake.direction != 'UP':
                self.ui.set_message(turn_message)
            self.snake.change_to = 'UP'
        elif key_name in [k.upper() for k in down_keys]:
            if self.snake.direction != 'DOWN':
                self.ui.set_message(turn_message)
            self.snake.change_to = 'DOWN'
        elif key_name in [k.upper() for k in left_keys]:
            if self.snake.direction != 'LEFT':
                self.ui.set_message(turn_message)
            self.snake.change_to = 'LEFT'
        elif key_name in [k.upper() for k in right_keys]:
            if self.snake.direction != 'RIGHT':
                self.ui.set_message(turn_message)
            self.snake.change_to = 'RIGHT'
        elif key_name == exit_key.upper():
            self.running = False
        elif key_name == refresh_key.upper():
            self.obstacles.generate()
            self.ui.set_message(refresh_message)
            
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
            length_increase = self.food.type.get('length_increase', 1)
            self.snake.grow(length_increase)
            self.food.spawn(self.snake.body, self.obstacles.obstacles, self.star.pos)
            self.ui.set_message(self.food.get_message())
            ate_food = True
            
        # 检查是否吃到星星
        if self.star.pos and self.snake.check_collision_with_pos(self.star.pos):
            self.lives += 1
            self.star.collect()
            star_message = self.messages.get('star_collected', '获得一条新生命！')
            self.ui.set_message(star_message)
            
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
        if self.speed_level < self.MAX_LEVEL and now - self.last_speedup_time >= self.SPEEDUP_INTERVAL:
            self.speed_level += 1
            self.last_speedup_time = now
            
    def check_collisions(self):
        """检查碰撞"""
        # 边界碰撞（基于游戏区域边界）
        if self.snake.check_boundary_collision(self.GAME_WIDTH, self.GAME_HEIGHT):
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
        penalty = self.config.get('gameplay.collision_penalty', 1)
        self.lives -= penalty
        if self.lives <= 0:
            self.game_over()
        else:
            self.snake.reset()
            if collision_type == 'person':
                person_message = self.messages.get('caught_by_person', '被小人抓住了！')
                self.ui.set_message(person_message)
            time.sleep(1)
            
    def check_win_condition(self):
        """检查胜利条件"""
        if self.snake.get_length() >= self.WIN_CONDITION:
            self.game_over(win=True)
            
    def draw(self):
        """绘制游戏画面"""
        # 填充整个窗口背景
        self.game_window.fill(self.colors['black'])
        
        # 绘制UI区域背景
        self.ui.draw_ui_background(self.game_window)
        
        # 绘制蛇
        snake_color = self.config.get_color('snake.color')
        for i, pos in enumerate(self.snake.body):
            if i == 0:
                # 绘制蛇头
                self.sprite_manager.draw_sprite(self.game_window, 'snake_head', pos, 
                                              snake_color, (20, 20))
            else:
                # 绘制蛇身
                self.sprite_manager.draw_sprite(self.game_window, 'snake_body', pos, 
                                              snake_color, (20, 20))
            
        # 绘制食物
        food_name = self.food.type.get('name', 'small')
        food_color = self.food.type.get('color', [255, 255, 255])
        self.sprite_manager.draw_sprite(self.game_window, f'food_{food_name}', self.food.pos, 
                                      food_color, (20, 20))
        
        # 绘制星星
        if self.star.pos:
            self.sprite_manager.draw_sprite(self.game_window, 'star', self.star.pos, 
                                          (255, 215, 0), (20, 20))
        
        # 绘制障碍物
        obstacle_color = self.config.get_color('obstacles.color')
        for obs in self.obstacles.obstacles:
            self.sprite_manager.draw_sprite(self.game_window, 'obstacle', obs, 
                                          obstacle_color, (20, 20))
        
        # 绘制小人
        person_color = self.config.get_color('enemies.color')
        for person in self.person_manager.persons:
            self.sprite_manager.draw_sprite(self.game_window, 'enemy', person.pos, 
                                          person_color, (20, 20))
        
        # 绘制UI
        self.ui.show_score(self.game_window, self.score)
        self.ui.show_lives(self.game_window, self.lives)
        self.ui.show_info(self.game_window, self.speed_level, self.snake.get_length())
        self.ui.show_message(self.game_window)
        
    def game_over(self, win=False):
        """游戏结束"""
        my_font = pygame.font.SysFont('times new roman', 60)
        if win:
            msg = self.messages.get('game_win', 'YOU WIN!')
            color = self.colors['blue']
        else:
            msg = self.messages.get('game_over', 'YOU DIED')
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