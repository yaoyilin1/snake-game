import pygame

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