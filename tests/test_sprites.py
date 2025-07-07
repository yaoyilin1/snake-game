#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试精灵系统
验证所有图片是否正确加载和显示
"""

import pygame
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import ConfigManager
from utils.sprite_manager import SpriteManager

def test_sprites():
    """测试精灵系统"""
    print("=== 精灵系统测试 ===")
    
    # 初始化pygame
    pygame.init()
    
    # 创建配置和精灵管理器
    config = ConfigManager()
    sprite_manager = SpriteManager(config)
    
    # 显示加载的精灵
    sprites = sprite_manager.get_sprite_list()
    print(f"已加载的精灵: {sprites}")
    
    # 创建测试窗口
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("精灵测试")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 清屏
        screen.fill((0, 0, 0))
        
        # 绘制所有精灵进行测试
        y_offset = 50
        x_offset = 50
        
        for i, sprite_name in enumerate(sprites):
            x = x_offset + (i % 10) * 80
            y = y_offset + (i // 10) * 80
            
            sprite_manager.draw_sprite(screen, sprite_name, (x, y))
            
            # 显示精灵名称
            font = pygame.font.SysFont('arial', 10)
            text = font.render(sprite_name, True, (255, 255, 255))
            screen.blit(text, (x, y + 30))
        
        # 显示说明
        font = pygame.font.SysFont('arial', 16)
        text = font.render("所有游戏精灵预览 - 按ESC退出", True, (255, 255, 0))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("✓ 精灵系统测试完成")

if __name__ == "__main__":
    test_sprites() 