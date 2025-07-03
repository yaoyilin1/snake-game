#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有模块导入是否正常
"""

def test_imports():
    """测试所有模块的导入"""
    try:
        print("测试导入...")
        
        # 测试核心模块
        from core.snake import Snake
        from core.game_engine import SnakeGameEngine
        print("✓ 核心模块导入成功")
        
        # 测试实体模块
        from entities.food import Food
        from entities.star import Star
        from entities.person import Person, PersonManager
        from entities.obstacles import ObstacleGroup
        print("✓ 实体模块导入成功")
        
        # 测试UI模块
        from ui.ui_manager import UIManager
        print("✓ UI模块导入成功")
        
        # 测试包导入
        from core import Snake, SnakeGameEngine
        from entities import Food, Star, Person, PersonManager, ObstacleGroup
        from ui import UIManager
        print("✓ 包导入成功")
        
        print("\n所有模块导入测试通过！项目结构正确。")
        return True
        
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

if __name__ == '__main__':
    test_imports() 