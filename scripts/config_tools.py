#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置工具脚本
提供配置验证、导出、重置等功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import ConfigManager

def validate_config():
    """验证配置文件"""
    print("=== 配置验证工具 ===")
    
    try:
        config = ConfigManager()
        print("✓ 配置文件加载成功")
        
        # 验证关键配置项
        window_config = config.get_window_config()
        print(f"✓ 窗口配置: {window_config.get('game_width')}x{window_config.get('game_height')}")
        
        speed_config = config.get_speed_config()
        print(f"✓ 速度等级数: {len(speed_config.get('levels', []))}")
        
        food_config = config.get_food_config()
        food_types = food_config.get('types', [])
        print(f"✓ 食物类型数: {len(food_types)}")
        
        # 验证概率总和
        total_prob = sum(food_type.get('probability', 0) for food_type in food_types)
        if abs(total_prob - 1.0) < 0.001:
            print("✓ 食物概率配置正确")
        else:
            print(f"⚠ 食物概率总和为 {total_prob}，应该为 1.0")
            
        controls = config.get_controls_config()
        print(f"✓ 控制键配置: {len(controls)} 个控制类型")
        
        messages = config.get_messages_config()
        print(f"✓ 消息配置: {len(messages)} 个消息")
        
        print("\n配置验证完成！")
        return True
        
    except Exception as e:
        print(f"✗ 配置验证失败: {e}")
        return False

def show_config_info():
    """显示配置信息"""
    print("=== 当前配置信息 ===")
    
    config = ConfigManager()
    
    print("\n【窗口配置】")
    window = config.get_window_config()
    for key, value in window.items():
        print(f"  {key}: {value}")
        
    print("\n【游戏配置】")
    gameplay = config.get_gameplay_config()
    for key, value in gameplay.items():
        print(f"  {key}: {value}")
        
    print("\n【速度配置】")
    speed = config.get_speed_config()
    for key, value in speed.items():
        print(f"  {key}: {value}")
        
    print("\n【食物配置】")
    food = config.get_food_config()
    types = food.get('types', [])
    for i, food_type in enumerate(types):
        name = food_type.get('name', 'unknown')
        length = food_type.get('length_increase', 0)
        prob = food_type.get('probability', 0)
        print(f"  类型{i+1}: {name}, 增长: {length}, 概率: {prob}")

def export_config_template():
    """导出配置模板"""
    print("=== 导出配置模板 ===")
    
    config = ConfigManager()
    template_file = "config/game_config_template.json"
    
    if config.save_config(template_file):
        print(f"✓ 配置模板已导出到: {template_file}")
    else:
        print("✗ 导出失败")

def reset_config():
    """重置配置为默认值"""
    print("=== 重置配置 ===")
    
    config = ConfigManager()
    config.reset_to_default()
    
    if config.save_config():
        print("✓ 配置已重置为默认值")
    else:
        print("✗ 重置失败")

def modify_config():
    """交互式修改配置"""
    print("=== 配置修改工具 ===")
    
    config = ConfigManager()
    
    print("可修改的配置项:")
    print("1. 窗口标题")
    print("2. 游戏区域尺寸")
    print("3. 初始生命数")
    print("4. 胜利条件长度")
    print("5. 敌人数量")
    print("0. 退出")
    
    while True:
        try:
            choice = input("\n请选择要修改的配置项 (0-5): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                title = input("请输入新的窗口标题: ").strip()
                if title:
                    config.update_config('window.title', title)
                    print("✓ 窗口标题已更新")
            elif choice == '2':
                width = int(input("请输入游戏区域宽度: "))
                height = int(input("请输入游戏区域高度: "))
                config.update_config('window.game_width', width)
                config.update_config('window.game_height', height)
                print("✓ 游戏区域尺寸已更新")
            elif choice == '3':
                lives = int(input("请输入初始生命数: "))
                config.update_config('gameplay.initial_lives', lives)
                print("✓ 初始生命数已更新")
            elif choice == '4':
                length = int(input("请输入胜利条件长度: "))
                config.update_config('gameplay.win_condition_length', length)
                print("✓ 胜利条件已更新")
            elif choice == '5':
                count = int(input("请输入敌人数量: "))
                config.update_config('enemies.person_count', count)
                print("✓ 敌人数量已更新")
            else:
                print("无效选择，请重试")
                
        except (ValueError, KeyboardInterrupt):
            print("\n操作已取消")
            break
    
    # 保存配置
    save = input("\n是否保存修改? (y/n): ").strip().lower()
    if save == 'y':
        if config.save_config():
            print("✓ 配置已保存")
        else:
            print("✗ 保存失败")

def main():
    """主函数"""
    print("游戏配置管理工具")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'validate':
            validate_config()
        elif command == 'info':
            show_config_info()
        elif command == 'export':
            export_config_template()
        elif command == 'reset':
            reset_config()
        elif command == 'modify':
            modify_config()
        else:
            print(f"未知命令: {command}")
    else:
        print("使用方法:")
        print("  python scripts/config_tools.py validate  - 验证配置")
        print("  python scripts/config_tools.py info      - 显示配置信息")
        print("  python scripts/config_tools.py export    - 导出配置模板")
        print("  python scripts/config_tools.py reset     - 重置为默认配置")
        print("  python scripts/config_tools.py modify    - 交互式修改配置")

if __name__ == "__main__":
    main() 