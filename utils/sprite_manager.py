import pygame
import os

class SpriteManager:
    """精灵图片管理器，负责加载和管理游戏中的所有图片资源"""
    
    def __init__(self, config=None):
        """初始化精灵管理器"""
        self.config = config
        self.sprites = {}
        self.load_all_sprites()
        
    def load_sprite(self, key, path, size=None):
        """加载单个精灵图片"""
        try:
            if os.path.exists(path):
                sprite = pygame.image.load(path)
                if size:
                    sprite = pygame.transform.scale(sprite, size)
                self.sprites[key] = sprite
                print(f"[+] 成功加载精灵: {key} <- {path}")
                return True
            else:
                print(f"[!] 精灵文件不存在: {path}")
                return False
        except Exception as e:
            print(f"[!] 加载精灵失败 {key}: {e}")
            return False
            
    def load_all_sprites(self):
        """加载所有精灵图片"""
        if not self.config:
            return
            
        print("=== 加载游戏精灵图片 ===")
        
        # 加载蛇的图片
        snake_config = self.config.get_snake_config()
        if snake_config:
            head_image = snake_config.get('head_image')
            body_image = snake_config.get('body_image')
            cell_size = snake_config.get('cell_size', 10)
            
            if head_image:
                self.load_sprite('snake_head', head_image, (cell_size*2, cell_size*2))
            if body_image:
                self.load_sprite('snake_body', body_image, (cell_size*2, cell_size*2))
                
        # 加载食物图片
        food_config = self.config.get_food_config()
        if food_config:
            food_types = food_config.get('types', [])
            for food_type in food_types:
                name = food_type.get('name')
                image_path = food_type.get('image')
                if name and image_path:
                    self.load_sprite(f'food_{name}', image_path, (20, 20))
                    
        # 加载障碍物图片
        obstacles_config = self.config.get_obstacles_config()
        if obstacles_config:
            obstacle_image = obstacles_config.get('image')
            if obstacle_image:
                self.load_sprite('obstacle', obstacle_image, (20, 20))
                
        # 加载敌人图片
        enemies_config = self.config.get_enemies_config()
        if enemies_config:
            enemy_image = enemies_config.get('image')
            if enemy_image:
                self.load_sprite('enemy', enemy_image, (20, 20))
                
        # 加载星星图片
        star_config = self.config.get_star_config()
        if star_config:
            star_image = star_config.get('image_path')
            if star_image:
                self.load_sprite('star', star_image, (20, 20))
                
        # 加载UI图片
        ui_config = self.config.get_ui_config()
        if ui_config:
            ui_images = ui_config.get('images', {})
            for key, path in ui_images.items():
                if key == 'background':
                    # UI背景使用实际尺寸
                    window_config = self.config.get_window_config()
                    width = window_config.get('game_width', 720)
                    height = window_config.get('ui_height', 80)
                    self.load_sprite('ui_background', path, (width, height))
                elif key == 'heart':
                    self.load_sprite('heart', path, (16, 16))
                elif key == 'score_background':
                    self.load_sprite('score_background', path, (100, 30))
                    
        print(f"✓ 精灵加载完成，共加载 {len(self.sprites)} 个精灵")
        
    def get_sprite(self, key):
        """获取精灵图片"""
        return self.sprites.get(key)
        
    def has_sprite(self, key):
        """检查是否有指定的精灵"""
        return key in self.sprites
        
    def draw_sprite(self, surface, key, pos, fallback_color=None, fallback_size=(20, 20)):
        """绘制精灵，如果没有图片则使用回退颜色绘制矩形"""
        sprite = self.get_sprite(key)
        if sprite:
            surface.blit(sprite, pos)
        elif fallback_color:
            # 回退到颜色绘制
            rect = pygame.Rect(pos[0], pos[1], fallback_size[0], fallback_size[1])
            pygame.draw.rect(surface, fallback_color, rect)
            
    def draw_sprite_centered(self, surface, key, center_pos, fallback_color=None, fallback_size=(20, 20)):
        """在指定中心位置绘制精灵"""
        sprite = self.get_sprite(key)
        if sprite:
            rect = sprite.get_rect()
            rect.center = center_pos
            surface.blit(sprite, rect)
        elif fallback_color:
            # 回退到颜色绘制
            rect = pygame.Rect(0, 0, fallback_size[0], fallback_size[1])
            rect.center = center_pos
            pygame.draw.rect(surface, fallback_color, rect)
            
    def reload_sprites(self):
        """重新加载所有精灵"""
        self.sprites.clear()
        self.load_all_sprites()
        
    def get_sprite_list(self):
        """获取所有已加载的精灵列表"""
        return list(self.sprites.keys()) 