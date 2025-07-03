#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪吃蛇游戏主程序入口
使用面向对象编程，模块化设计
"""

from core.game_engine import SnakeGameEngine

def main():
    """主函数"""
    print("=== 贪吃蛇游戏启动 ===")
    print("游戏说明：")
    print("- 使用WASD或方向键控制蛇的移动")
    print("- 吃到不同颜色的食物可以增加不同长度")
    print("- 黄色星星可以增加生命")
    print("- 紫色小人是敌人，碰到会死亡")
    print("- 蓝色方块是障碍物")
    print("- 按R键刷新障碍物")
    print("- 按ESC键退出游戏")
    print("==================")
    
    # 创建游戏引擎并运行
    engine = SnakeGameEngine()
    engine.run()

if __name__ == '__main__':
    main() 