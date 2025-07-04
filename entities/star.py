import pygame
import random
import os

class Star:
    """星星奖励类，管理星星的生成、位置、计时"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = None
        self.timer = 0
        self.duration = 3000  # 星星存在时间（毫秒）
        self.spawn_probability = 0.01  # 每帧生成概率
        
        # 加载星星图片
        self.image = None
        self.load_image()
        
    def load_image(self):
        """加载星星图片，如果加载失败则使用None（回退到方块绘制）"""
        try:
            image_path = os.path.join("images", "star.png")
            if os.path.exists(image_path):
                # 加载图片并缩放到10x10像素
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (10, 10))
                print(f"[+] 成功加载星星图片: {image_path}")
            else:
                print(f"[!] 星星图片不存在: {image_path}，将使用默认方块绘制")
                self.image = None
        except Exception as e:
            print(f"[!] 加载星星图片失败: {e}，将使用默认方块绘制")
            self.image = None
            
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
        
    def draw(self, game_window):
        """绘制星星 - 如果有图片则绘制图片，否则绘制黄色方块"""
        if self.pos is not None:
            if self.image is not None:
                # 使用图片绘制
                game_window.blit(self.image, (self.pos[0], self.pos[1]))
            else:
                # 回退到方块绘制
                pygame.draw.rect(game_window, (255, 215, 0), 
                               pygame.Rect(self.pos[0], self.pos[1], 10, 10)) 