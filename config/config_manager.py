import json
import os
import pygame

class ConfigManager:
    """配置管理器，负责加载和管理游戏配置"""
    
    def __init__(self, config_file="config/game_config.json"):
        """初始化配置管理器"""
        self.config_file = config_file
        self.config = {}
        self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.config_file)
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"[+] 成功加载配置文件: {self.config_file}")
        except FileNotFoundError:
            print(f"[!] 配置文件不存在: {self.config_file}，使用默认配置")
            self._load_default_config()
        except json.JSONDecodeError as e:
            print(f"[!] 配置文件格式错误: {e}，使用默认配置")
            self._load_default_config()
        except Exception as e:
            print(f"[!] 加载配置文件失败: {e}，使用默认配置")
            self._load_default_config()
            
    def _load_default_config(self):
        """加载默认配置"""
        self.config = {
            "window": {"title": "Snake Eater", "game_width": 720, "game_height": 480, "ui_height": 80},
            "snake": {"initial_position": [100, 50], "cell_size": 10, "color": [0, 255, 0]},
            "speed": {"levels": [10, 15, 20, 25, 30, 40, 60, 90, 120], "max_level": 9},
            "gameplay": {"initial_lives": 3, "win_condition_length": 100}
        }
        
    def get(self, key_path, default=None):
        """获取配置值，支持点分隔的路径"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def get_window_config(self):
        """获取窗口配置"""
        return self.get('window') or {}
        
    def get_snake_config(self):
        """获取蛇配置"""
        return self.get('snake') or {}
        
    def get_speed_config(self):
        """获取速度配置"""
        return self.get('speed') or {}
        
    def get_food_config(self):
        """获取食物配置"""
        return self.get('food') or {}
        
    def get_star_config(self):
        """获取星星配置"""
        return self.get('star') or {}
        
    def get_obstacles_config(self):
        """获取障碍物配置"""
        return self.get('obstacles') or {}
        
    def get_enemies_config(self):
        """获取敌人配置"""
        return self.get('enemies') or {}
        
    def get_gameplay_config(self):
        """获取游戏玩法配置"""
        return self.get('gameplay') or {}
        
    def get_ui_config(self):
        """获取UI配置"""
        return self.get('ui') or {}
        
    def get_controls_config(self):
        """获取控制配置"""
        return self.get('controls') or {}
        
    def get_messages_config(self):
        """获取消息配置"""
        return self.get('messages') or {}
        
    def get_color(self, color_path):
        """获取颜色配置并转换为pygame.Color对象"""
        color_value = self.get(color_path)
        if color_value and isinstance(color_value, list) and len(color_value) >= 3:
            return pygame.Color(color_value[0], color_value[1], color_value[2])
        return pygame.Color(255, 255, 255)  # 默认白色
        
    def get_colors_dict(self):
        """获取所有UI颜色的字典"""
        ui_colors = self.get('ui.colors', {})
        colors = {}
        
        # 基本颜色映射
        color_mapping = {
            'black': 'ui.colors.background',
            'white': [255, 255, 255],
            'red': 'ui.colors.lives_text', 
            'green': 'snake.color',
            'blue': 'obstacles.color',
            'yellow': 'star.color',
            'purple': 'enemies.color',
            'dark_gray': 'ui.colors.ui_background',
            'light_gray': 'ui.colors.separator'
        }
        
        for name, path in color_mapping.items():
            if isinstance(path, str):
                colors[name] = self.get_color(path)
            else:
                colors[name] = pygame.Color(path[0], path[1], path[2])
                
        return colors
        
    def save_config(self, config_file=None):
        """保存配置到文件"""
        if config_file is None:
            config_file = self.config_file
            
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_file)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print(f"[+] 配置已保存到: {config_file}")
            return True
        except Exception as e:
            print(f"[!] 保存配置失败: {e}")
            return False
            
    def update_config(self, key_path, value):
        """更新配置值"""
        keys = key_path.split('.')
        config = self.config
        
        # 导航到父级
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
            
        # 设置值
        config[keys[-1]] = value
        
    def reset_to_default(self):
        """重置为默认配置"""
        self._load_default_config()
        print("[+] 配置已重置为默认值") 