#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏完整性测试
测试游戏的所有核心功能和系统集成
"""

import sys
import os
import pygame

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import ConfigManager
from core.game_engine import SnakeGameEngine
from utils.sprite_manager import SpriteManager

def test_config_loading():
    """测试配置加载"""
    print("=== 配置加载测试 ===")
    
    try:
        config = ConfigManager()
        
        # 测试各个配置组
        window_config = config.get_window_config()
        snake_config = config.get_snake_config()
        food_config = config.get_food_config()
        
        assert window_config is not None, "窗口配置加载失败"
        assert snake_config is not None, "蛇配置加载失败"
        assert food_config is not None, "食物配置加载失败"
        
        print("✓ 配置加载测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 配置加载测试失败: {e}")
        return False

def test_sprite_loading():
    """测试精灵加载"""
    print("=== 精灵加载测试 ===")
    
    try:
        pygame.init()
        config = ConfigManager()
        sprite_manager = SpriteManager(config)
        
        # 检查关键精灵是否加载
        required_sprites = ['snake_head', 'snake_body', 'food_small', 'obstacle', 'enemy']
        
        for sprite_name in required_sprites:
            assert sprite_manager.has_sprite(sprite_name), f"精灵 {sprite_name} 未加载"
        
        print(f"✓ 精灵加载测试通过，共加载 {len(sprite_manager.get_sprite_list())} 个精灵")
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ 精灵加载测试失败: {e}")
        pygame.quit()
        return False

def test_game_engine_init():
    """测试游戏引擎初始化"""
    print("=== 游戏引擎初始化测试 ===")
    
    try:
        # 初始化游戏引擎
        engine = SnakeGameEngine()
        
        # 检查关键组件
        assert engine.snake is not None, "蛇对象未初始化"
        assert engine.food is not None, "食物对象未初始化"
        assert engine.sprite_manager is not None, "精灵管理器未初始化"
        assert engine.ui is not None, "UI管理器未初始化"
        
        # 检查配置是否正确应用
        assert engine.GAME_WIDTH > 0, "游戏宽度配置错误"
        assert engine.GAME_HEIGHT > 0, "游戏高度配置错误"
        assert len(engine.SPEED_LEVELS) > 0, "速度等级配置错误"
        
        print("✓ 游戏引擎初始化测试通过")
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"✗ 游戏引擎初始化测试失败: {e}")
        pygame.quit()
        return False

def test_snake_functionality():
    """测试蛇的功能"""
    print("=== 蛇功能测试 ===")
    
    try:
        config = ConfigManager()
        from core.snake import Snake
        
        snake = Snake(config)
        
        # 测试基本属性
        assert len(snake.body) > 0, "蛇身体为空"
        assert snake.direction in ['UP', 'DOWN', 'LEFT', 'RIGHT'], "蛇方向无效"
        
        # 测试移动
        initial_pos = snake.pos.copy()
        snake.move()
        assert snake.pos != initial_pos, "蛇移动失败"
        
        # 测试增长
        initial_length = snake.get_length()
        snake.grow(2)
        snake.update_body()
        snake.shrink_tail()  # 正常游戏中如果没吃到食物会缩短
        assert snake.get_length() == initial_length + 1, "蛇增长功能异常"
        
        print("✓ 蛇功能测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 蛇功能测试失败: {e}")
        return False

def test_food_functionality():
    """测试食物功能"""
    print("=== 食物功能测试 ===")
    
    try:
        config = ConfigManager()
        from entities.food import Food
        
        food = Food(720, 480, config)
        
        # 测试食物类型
        assert food.type is not None, "食物类型为空"
        assert 'name' in food.type, "食物类型缺少名称"
        assert 'length_increase' in food.type, "食物类型缺少增长量"
        
        # 测试食物生成
        old_pos = food.pos.copy()
        food.spawn()
        # 位置可能相同，但不应该出错
        
        # 测试消息
        message = food.get_message()
        assert isinstance(message, str), "食物消息不是字符串"
        assert len(message) > 0, "食物消息为空"
        
        print("✓ 食物功能测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 食物功能测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("贪吃蛇游戏完整性测试")
    print("=" * 50)
    
    tests = [
        test_config_loading,
        test_sprite_loading,
        test_game_engine_init,
        test_snake_functionality,
        test_food_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"测试异常: {e}")
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！游戏系统运行正常。")
    else:
        print("⚠️ 部分测试失败，请检查相关功能。")
    
    print("=" * 50)
    
    return passed == total

if __name__ == "__main__":
    run_all_tests() 