#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏精灵图片生成器
生成贪吃蛇游戏所需的各种图片素材
"""

import pygame
import os
import math

def create_snake_head(size=20, color=(0, 255, 0)):
    """创建蛇头图片 - 带眼睛和嘴巴"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 绘制头部轮廓
    pygame.draw.circle(surface, color, (size//2, size//2), size//2-1)
    pygame.draw.circle(surface, (0, 100, 0), (size//2, size//2), size//2-1, 2)
    
    # 绘制眼睛
    eye_size = size // 6
    eye_y = size // 3
    # 左眼
    pygame.draw.circle(surface, (255, 255, 255), (size//3, eye_y), eye_size)
    pygame.draw.circle(surface, (0, 0, 0), (size//3, eye_y), eye_size//2)
    # 右眼
    pygame.draw.circle(surface, (255, 255, 255), (size*2//3, eye_y), eye_size)
    pygame.draw.circle(surface, (0, 0, 0), (size*2//3, eye_y), eye_size//2)
    
    # 绘制嘴巴
    mouth_rect = pygame.Rect(size//3, size*2//3, size//3, size//8)
    pygame.draw.ellipse(surface, (255, 100, 100), mouth_rect)
    
    return surface

def create_snake_body(size=20, color=(0, 255, 0)):
    """创建蛇身图片 - 带纹理"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 绘制身体
    pygame.draw.rect(surface, color, (1, 1, size-2, size-2))
    pygame.draw.rect(surface, (0, 150, 0), (1, 1, size-2, size-2), 2)
    
    # 添加纹理
    pygame.draw.rect(surface, (100, 255, 100), (3, 3, size-6, size-6))
    
    return surface

def create_food_sprite(size=20, color=(255, 255, 255), food_type="small"):
    """创建食物图片"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if food_type == "small":
        # 小食物 - 圆形
        pygame.draw.circle(surface, color, (size//2, size//2), size//2-1)
        pygame.draw.circle(surface, (200, 200, 200), (size//2, size//2), size//2-1, 2)
    elif food_type == "medium":
        # 中食物 - 方形
        pygame.draw.rect(surface, color, (2, 2, size-4, size-4))
        pygame.draw.rect(surface, (0, 150, 200), (2, 2, size-4, size-4), 2)
    elif food_type == "large":
        # 大食物 - 菱形
        points = [
            (size//2, 1),
            (size-1, size//2),
            (size//2, size-1),
            (1, size//2)
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (200, 50, 0), points, 2)
    
    return surface

def create_obstacle_sprite(size=20):
    """创建障碍物图片 - 木箱样式"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 木箱底色
    brown = (139, 69, 19)
    pygame.draw.rect(surface, brown, (0, 0, size, size))
    
    # 木纹纹理
    dark_brown = (101, 67, 33)
    for i in range(0, size, 4):
        pygame.draw.line(surface, dark_brown, (i, 0), (i, size), 1)
        pygame.draw.line(surface, dark_brown, (0, i), (size, i), 1)
    
    # 钉子
    nail_color = (64, 64, 64)
    pygame.draw.circle(surface, nail_color, (3, 3), 1)
    pygame.draw.circle(surface, nail_color, (size-3, 3), 1)
    pygame.draw.circle(surface, nail_color, (3, size-3), 1)
    pygame.draw.circle(surface, nail_color, (size-3, size-3), 1)
    
    return surface

def create_enemy_sprite(size=20):
    """创建敌人图片 - 小怪物"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 身体
    purple = (160, 32, 240)
    pygame.draw.ellipse(surface, purple, (2, 4, size-4, size-6))
    
    # 眼睛
    eye_size = size // 8
    pygame.draw.circle(surface, (255, 255, 255), (size//3, size//3), eye_size)
    pygame.draw.circle(surface, (0, 0, 0), (size//3, size//3), eye_size//2)
    
    # 嘴巴
    mouth_points = [
        (size//4, size*2//3),
        (size//2, size*3//4),
        (size*3//4, size*2//3)
    ]
    pygame.draw.polygon(surface, (255, 100, 100), mouth_points)
    
    # 触角
    pygame.draw.line(surface, purple, (size//3, 2), (size//3-2, 0), 2)
    pygame.draw.line(surface, purple, (size*2//3, 2), (size*2//3+2, 0), 2)
    pygame.draw.circle(surface, (255, 255, 0), (size//3-2, 0), 1)
    pygame.draw.circle(surface, (255, 255, 0), (size*2//3+2, 0), 1)
    
    return surface

def create_ui_background(width, height):
    """创建UI背景图片"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 渐变背景
    for y in range(height):
        alpha = int(255 * (1 - y / height))
        color = (40, 40, 40, alpha)
        pygame.draw.line(surface, color, (0, y), (width, y))
    
    # 边框
    pygame.draw.rect(surface, (100, 100, 100), (0, 0, width, height), 2)
    
    return surface

def create_heart_icon(size=16):
    """创建生命值心形图标"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # 心形的点
    points = []
    for angle in range(0, 360, 5):
        rad = math.radians(angle)
        # 心形参数方程
        x = 16 * math.sin(rad) ** 3
        y = 13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad)
        
        # 缩放和平移到合适位置
        x = int(x * size / 32 + size / 2)
        y = int(-y * size / 32 + size / 2)
        
        if 0 <= x < size and 0 <= y < size:
            points.append((x, y))
    
    if len(points) > 2:
        pygame.draw.polygon(surface, (255, 0, 0), points)
        pygame.draw.polygon(surface, (200, 0, 0), points, 1)
    
    return surface

def create_score_background(width, height):
    """创建分数背景框"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 半透明背景
    pygame.draw.rect(surface, (0, 0, 0, 128), (0, 0, width, height))
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, width, height), 2)
    
    return surface

def main():
    """主函数 - 生成所有游戏精灵"""
    print("=== 游戏精灵图片生成器 ===")
    
    # 初始化pygame
    pygame.init()
    
    # 确保images目录存在
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"创建目录: {images_dir}")
    
    # 生成蛇的图片
    print("生成蛇的图片...")
    snake_head = create_snake_head(20, (0, 255, 0))
    pygame.image.save(snake_head, os.path.join(images_dir, "snake_head.png"))
    
    snake_body = create_snake_body(20, (0, 255, 0))
    pygame.image.save(snake_body, os.path.join(images_dir, "snake_body.png"))
    
    # 生成食物图片
    print("生成食物图片...")
    food_small = create_food_sprite(20, (255, 255, 255), "small")
    pygame.image.save(food_small, os.path.join(images_dir, "food_small.png"))
    
    food_medium = create_food_sprite(20, (0, 191, 255), "medium")
    pygame.image.save(food_medium, os.path.join(images_dir, "food_medium.png"))
    
    food_large = create_food_sprite(20, (255, 69, 0), "large")
    pygame.image.save(food_large, os.path.join(images_dir, "food_large.png"))
    
    # 生成障碍物图片
    print("生成障碍物图片...")
    obstacle = create_obstacle_sprite(20)
    pygame.image.save(obstacle, os.path.join(images_dir, "obstacle.png"))
    
    # 生成敌人图片
    print("生成敌人图片...")
    enemy = create_enemy_sprite(20)
    pygame.image.save(enemy, os.path.join(images_dir, "enemy.png"))
    
    # 生成UI图片
    print("生成UI图片...")
    ui_bg = create_ui_background(720, 80)
    pygame.image.save(ui_bg, os.path.join(images_dir, "ui_background.png"))
    
    heart = create_heart_icon(16)
    pygame.image.save(heart, os.path.join(images_dir, "heart.png"))
    
    score_bg = create_score_background(100, 30)
    pygame.image.save(score_bg, os.path.join(images_dir, "score_background.png"))
    
    pygame.quit()
    
    print("✓ 所有游戏精灵图片生成完成！")
    print("生成的文件:")
    for filename in os.listdir(images_dir):
        if filename.endswith('.png'):
            print(f"  - {filename}")

if __name__ == "__main__":
    main() 