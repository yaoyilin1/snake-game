import pygame
import math
import os

def create_star_image():
    """创建一个五角星图片"""
    # 初始化pygame
    pygame.init()
    
    # 设置图片大小
    size = 10
    surface = pygame.Surface((size, size), pygame.SRCALPHA)  # 支持透明度
    
    # 五角星的颜色 - 金黄色
    star_color = (255, 215, 0)  # 金黄色
    outline_color = (255, 140, 0)  # 橙色边框
    
    # 计算五角星的顶点坐标
    center_x, center_y = size // 2, size // 2
    outer_radius = 4  # 外半径
    inner_radius = 1.5  # 内半径
    
    # 五角星的10个顶点（5个外顶点 + 5个内顶点）
    points = []
    for i in range(10):
        angle = math.pi * 2 * i / 10 - math.pi / 2  # 从顶部开始
        if i % 2 == 0:  # 外顶点
            radius = outer_radius
        else:  # 内顶点
            radius = inner_radius
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    # 绘制五角星
    pygame.draw.polygon(surface, star_color, points)
    pygame.draw.polygon(surface, outline_color, points, 1)  # 边框
    
    # 保存图片 - 需要回退到项目根目录
    image_path = os.path.join("..", "..", "images", "star.png")
    pygame.image.save(surface, image_path)
    print(f"[+] 成功创建五角星图片: {image_path}")
    
    pygame.quit()

if __name__ == "__main__":
    create_star_image() 