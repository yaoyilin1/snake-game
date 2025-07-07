import pygame

class UIManager:
    """UI管理器，负责显示分数、生命、速度、长度、消息等"""
    
    def __init__(self, width, height, game_height, config=None, sprite_manager=None):
        self.width = width                # 总窗口宽度
        self.height = height             # 总窗口高度
        self.game_height = game_height   # 游戏区域高度
        self.ui_area_top = game_height   # UI区域顶部位置
        self.ui_height = height - game_height  # UI区域高度
        self.config = config
        self.sprite_manager = sprite_manager
        self.message = ''
        self.message_timer = 0
        
        # 从配置获取设置
        if config:
            ui_config = config.get_ui_config()
            self.message_duration = ui_config.get('message_duration', 2000)
        else:
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
            # 显示在UI区域左上角
            score_rect.topleft = (10, self.ui_area_top + 10)
        else:
            score_rect.midtop = (int(self.width/2), int(self.height/1.25))
        game_window.blit(score_surface, score_rect)
        
    def show_lives(self, game_window, lives, choice=1):
        """显示生命值"""
        if choice == 1:
            # 显示在UI区域右上角
            start_x = self.width - 10
            start_y = self.ui_area_top + 10
            
            # 使用心形图标显示生命值
            if self.sprite_manager and self.sprite_manager.has_sprite('heart'):
                for i in range(lives):
                    heart_x = start_x - (i + 1) * 20
                    self.sprite_manager.draw_sprite(game_window, 'heart', (heart_x, start_y))
            else:
                # 回退到文字显示
                lives_font = pygame.font.SysFont('consolas', 20)
                lives_surface = lives_font.render('Lives : ' + str(lives), True, (255, 0, 0))
                lives_rect = lives_surface.get_rect()
                lives_rect.topright = (start_x, start_y)
                game_window.blit(lives_surface, lives_rect)
        else:
            # 游戏结束时的显示
            lives_font = pygame.font.SysFont('consolas', 20)
            lives_surface = lives_font.render('Lives : ' + str(lives), True, (255, 0, 0))
            lives_rect = lives_surface.get_rect()
            lives_rect.midtop = (int(self.width/2), int(self.height/1.15))
            game_window.blit(lives_surface, lives_rect)
        
    def show_info(self, game_window, speed_level, snake_length):
        """显示速度和长度信息"""
        info_font = pygame.font.SysFont('consolas', 16)
        
        # 速度等级 - 显示在UI区域左下角
        speed_surface = info_font.render(f'Speed Level: {speed_level}', True, (0, 255, 255))
        speed_rect = speed_surface.get_rect()
        speed_rect.bottomleft = (10, self.height - 10)
        game_window.blit(speed_surface, speed_rect)
        
        # 蛇长度 - 显示在UI区域右下角
        length_surface = info_font.render(f'Length: {snake_length}', True, (0, 255, 255))
        length_rect = length_surface.get_rect()
        length_rect.bottomright = (self.width - 10, self.height - 10)
        game_window.blit(length_surface, length_rect)
        
    def show_message(self, game_window):
        """显示中央消息"""
        if self.message:
            msg_font = pygame.font.SysFont('simhei', 20)
            msg_surface = msg_font.render(self.message, True, (255, 255, 0))
            msg_rect = msg_surface.get_rect()
            # 显示在UI区域中央
            msg_rect.center = (int(self.width/2), self.ui_area_top + int(self.ui_height/2))
            
            # 消息框背景
            bg_rect = pygame.Rect(msg_rect.left - 10, msg_rect.top - 5, 
                                msg_rect.width + 20, msg_rect.height + 10)
            pygame.draw.rect(game_window, (50, 50, 50), bg_rect)
            pygame.draw.rect(game_window, (150, 150, 150), bg_rect, 2)
            game_window.blit(msg_surface, msg_rect)
            
    def draw_ui_background(self, game_window):
        """绘制UI区域背景"""
        # 使用精灵图片作为UI背景
        if self.sprite_manager and self.sprite_manager.has_sprite('ui_background'):
            self.sprite_manager.draw_sprite(game_window, 'ui_background', 
                                          (0, self.ui_area_top))
        else:
            # 回退到颜色绘制
            ui_rect = pygame.Rect(0, self.ui_area_top, self.width, self.ui_height)
            pygame.draw.rect(game_window, (40, 40, 40), ui_rect)
            
            # 绘制分隔线
            pygame.draw.line(game_window, (100, 100, 100), 
                            (0, self.ui_area_top), (self.width, self.ui_area_top), 2) 