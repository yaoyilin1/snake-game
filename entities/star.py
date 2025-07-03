import pygame
import random

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