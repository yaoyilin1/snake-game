#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试食物配置
验证食物类型、增长量和颜色是否按配置正确工作
"""

import sys
import os
import pygame

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import ConfigManager
from entities.food import Food

def test_food_config():
    """测试食物配置功能"""
    print("=== 食物配置测试 ===")
    
    # 初始化pygame（食物类需要）
    pygame.init()
    
    # 创建配置管理器
    config = ConfigManager()
    
    # 创建食物对象
    food = Food(720, 480, config)
    
    print(f"当前食物类型: {food.type}")
    print(f"食物名称: {food.type.get('name', 'unknown')}")
    print(f"增长量: {food.type.get('length_increase', 0)}")
    print(f"颜色: {food.type.get('color', [255,255,255])}")
    print(f"概率: {food.type.get('probability', 0)}")
    
    # 测试多次生成，验证不同类型
    print("\n=== 生成多个食物测试 ===")
    food_counts = {'small': 0, 'medium': 0, 'large': 0}
    
    for i in range(100):
        food.spawn()
        food_name = food.type.get('name', 'unknown')
        if food_name in food_counts:
            food_counts[food_name] += 1
    
    print("100次生成结果:")
    for name, count in food_counts.items():
        print(f"  {name}: {count}次 ({count}%)")
    
    # 测试消息
    print("\n=== 消息测试 ===")
    for food_type in food.food_types:
        food.type = food_type
        message = food.get_message()
        print(f"{food_type['name']}: {message}")
    
    pygame.quit()
    print("\n✓ 食物配置测试完成")

if __name__ == "__main__":
    test_food_config() 