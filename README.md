# 贪吃蛇游戏 - 面向对象版本

## 项目简介

这是一个使用Python和Pygame开发的贪吃蛇游戏，采用面向对象编程和模块化设计。

## 项目结构

```
snake-pygame/
├── main.py              # 主程序入口
├── core/                # 核心游戏组件
│   ├── __init__.py
│   ├── snake.py        # 贪吃蛇类
│   └── game_engine.py  # 游戏主引擎
├── entities/           # 游戏实体
│   ├── __init__.py
│   ├── food.py         # 食物类
│   ├── star.py         # 星星奖励类
│   ├── person.py       # 小人类和管理器
│   └── obstacles.py    # 障碍物组类
├── ui/                 # 用户界面
│   ├── __init__.py
│   └── ui_manager.py   # UI管理器
├── utils/              # 工具包（预留）
│   └── __init__.py
├── Snake Game.py       # 原始单文件版本（保留）
└── README.md           # 项目说明
```

## 功能特性

### 核心游戏功能
- **三条生命系统**：玩家有3条生命，撞墙或撞障碍物会扣生命
- **9级速度系统**：每分钟自动提升一级速度，最高9级
- **胜利条件**：蛇长度达到100时获胜

### 食物系统
- **三种食物类型**：
  - 小食物（白色）：增加1个长度，出现概率60%
  - 中食物（深天蓝）：增加3个长度，出现概率30%
  - 大食物（橙红色）：增加5个长度，出现概率10%

### 奖励系统
- **星星奖励**：随机出现的黄色星星，吃到可增加1条生命
- **底部消息框**：显示游戏状态和提示信息

### 障碍系统
- **50个障碍物**：分成5组，每组10个相连的障碍物
- **动态刷新**：按R键可重新生成障碍物布局

### 敌人系统
- **3个移动小人**：紫色方块，会自动移动，碰到会死亡
- **智能避障**：小人遇到障碍物或边界会自动换方向

## 控制说明

- **WASD键** 或 **方向键**：控制蛇的移动
- **R键**：刷新障碍物布局
- **ESC键**：退出游戏

## 类设计说明

### Snake类
- 管理蛇的身体、移动、增长
- 提供碰撞检测方法
- 支持重置功能

### Food类
- 管理三种食物类型的生成
- 按概率选择食物类型
- 避免与蛇、障碍物重叠

### Star类
- 管理星星奖励的生成和计时
- 自动消失机制
- 收集功能

### Person类 & PersonManager类
- Person：单个小人的位置和移动逻辑
- PersonManager：管理所有小人，处理移动和碰撞

### ObstacleGroup类
- 生成和管理障碍物组
- 支持重新生成功能

### UIManager类
- 管理所有UI显示
- 分数、生命、速度、长度显示
- 底部消息系统

### SnakeGameEngine类
- 游戏主引擎，负责整体调度
- 事件处理、状态更新、渲染
- 碰撞检测和游戏逻辑

## 运行方法

1. 确保已安装Python和Pygame
2. 运行主程序：
   ```bash
   python main.py
   ```

## Git仓库管理

### 初始化Git仓库

**Windows用户：**
```bash
# 双击运行 init_git.bat 文件
# 或者在命令行中运行：
git init
git add .
git commit -m "初始提交：贪吃蛇游戏项目"
```

**Linux/Mac用户：**
```bash
# 给脚本执行权限并运行
chmod +x init_git.sh
./init_git.sh

# 或者手动执行：
git init
git add .
git commit -m "初始提交：贪吃蛇游戏项目"
```

### 连接到远程仓库

#### 方法1：使用设置脚本（推荐）

**Windows用户：**
```bash
# 双击运行 setup_remote.bat 文件
# 按照提示选择Git托管服务并输入仓库URL
```

**Linux/Mac用户：**
```bash
# 给脚本执行权限并运行
chmod +x setup_remote.sh
./setup_remote.sh
```

#### 方法2：手动设置

```bash
# 添加远程仓库（替换为您的仓库URL）
git remote add origin <您的远程仓库URL>

# 推送到远程仓库
git push -u origin master
```

#### 支持的Git托管服务

- **GitHub**: https://github.com
- **GitLab**: https://gitlab.com  
- **Gitee (码云)**: https://gitee.com
- **自定义URL**: 任何Git服务器

### 常用Git命令

```bash
git status          # 查看仓库状态
git log             # 查看提交历史
git diff            # 查看文件变更
git branch          # 查看分支
git checkout -b feature  # 创建新分支
```

## 技术特点

- **模块化设计**：每个功能独立成类，便于维护和扩展
- **面向对象**：充分利用OOP特性，代码结构清晰
- **详细注释**：所有类和方法都有中文注释
- **可扩展性**：易于添加新功能或修改现有功能
- **代码复用**：各模块可独立使用

## 开发环境

- Python 3.6+
- Pygame 1.9+

## 作者

基于原始贪吃蛇游戏重构，采用面向对象编程和模块化设计。
