# 贪吃蛇游戏 - 面向对象版本

## 项目简介

这是一个使用Python和Pygame开发的贪吃蛇游戏，采用面向对象编程和模块化设计。具有完整的配置系统、精美的图形界面、丰富的游戏功能和全面的测试覆盖。

## 项目结构

```
snake-pygame/
├── main.py                 # 主程序入口
├── Snake Game.py           # 原始单文件版本（保留）
├── requirements.txt        # 项目依赖
├── config/                 # 配置系统
│   ├── __init__.py
│   ├── config_manager.py   # 配置管理器
│   ├── game_config.json    # 游戏配置文件
│   └── README.md           # 配置系统说明
├── core/                   # 核心游戏组件
│   ├── __init__.py
│   ├── snake.py            # 贪吃蛇类
│   └── game_engine.py      # 游戏主引擎
├── entities/               # 游戏实体
│   ├── __init__.py
│   ├── food.py             # 食物类
│   ├── star.py             # 星星奖励类
│   ├── person.py           # 小人类和管理器
│   └── obstacles.py        # 障碍物组类
├── ui/                     # 用户界面
│   ├── __init__.py
│   └── ui_manager.py       # UI管理器
├── utils/                  # 工具包
│   ├── __init__.py
│   └── sprite_manager.py   # 精灵管理器
├── images/                 # 图片资源
│   ├── snake_head.png      # 蛇头图片
│   ├── snake_body.png      # 蛇身图片
│   ├── food_small.png      # 小食物图片
│   ├── food_medium.png     # 中食物图片
│   ├── food_large.png      # 大食物图片
│   ├── star.png            # 星星图片
│   ├── enemy.png           # 敌人图片
│   ├── obstacle.png        # 障碍物图片
│   ├── heart.png           # 生命图标
│   ├── ui_background.png   # UI背景
│   ├── score_background.png # 分数背景
│   └── icon.png.png        # 游戏图标
├── scripts/                # 脚本工具
│   ├── __init__.py
│   ├── config_tools.py     # 配置工具
│   └── draw_ui/            # UI绘制工具
│       ├── __init__.py
│       ├── create_game_sprites.py  # 生成游戏精灵
│       └── create_star_image.py    # 生成星星图片
├── tests/                  # 测试系统
│   ├── __init__.py
│   ├── README.md           # 测试说明文档
│   ├── test_game_integration.py  # 游戏完整性测试
│   ├── test_sprites.py     # 精灵系统测试
│   ├── test_food_config.py # 食物配置测试
│   └── test_imports.py     # 模块导入测试
├── git_branch_guide.md     # Git分支管理指南
├── git_remote_guide.md     # Git远程仓库指南
├── setup_remote.sh         # 远程仓库设置脚本(Linux/Mac)
├── setup_remote.bat        # 远程仓库设置脚本(Windows)
├── init_git.sh             # Git初始化脚本(Linux/Mac)
├── init_git.bat            # Git初始化脚本(Windows)
└── README.md               # 项目说明
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

### 配置系统
- **JSON配置文件**：所有游戏参数可通过配置文件调整
- **动态配置加载**：支持运行时配置更新
- **配置验证**：自动验证配置文件的正确性

### 图形系统
- **精美精灵**：所有游戏元素都有对应的图片精灵
- **自动生成**：通过脚本自动生成所需的图片资源
- **精灵管理**：统一的精灵加载和管理系统

## 控制说明

- **WASD键** 或 **方向键**：控制蛇的移动
- **R键**：刷新障碍物布局
- **ESC键**：退出游戏

## 类设计说明

### 核心类

#### Snake类
- 管理蛇的身体、移动、增长
- 提供碰撞检测方法
- 支持重置功能

#### Food类
- 管理三种食物类型的生成
- 按概率选择食物类型
- 避免与蛇、障碍物重叠

#### Star类
- 管理星星奖励的生成和计时
- 自动消失机制
- 收集功能

#### Person类 & PersonManager类
- Person：单个小人的位置和移动逻辑
- PersonManager：管理所有小人，处理移动和碰撞

#### ObstacleGroup类
- 生成和管理障碍物组
- 支持重新生成功能

#### UIManager类
- 管理所有UI显示
- 分数、生命、速度、长度显示
- 底部消息系统

#### SnakeGameEngine类
- 游戏主引擎，负责整体调度
- 事件处理、状态更新、渲染
- 碰撞检测和游戏逻辑

### 系统类

#### ConfigManager类
- 配置文件加载和管理
- 配置验证和错误处理
- 动态配置更新

#### SpriteManager类
- 精灵图片加载和管理
- 图片缓存和优化
- 精灵渲染支持

## 运行方法

### 基本运行
1. 确保已安装Python和Pygame：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行主程序：
   ```bash
   python main.py
   ```

### 生成图片资源
如果图片资源缺失，可以运行以下脚本生成：
```bash
python scripts/draw_ui/create_game_sprites.py
```

### 运行测试
```bash
# 运行所有测试
python tests/test_game_integration.py  # 主要完整性测试
python tests/test_imports.py          # 模块导入测试
python tests/test_sprites.py          # 精灵可视化测试
python tests/test_food_config.py      # 食物配置测试
```

## 配置说明

游戏配置文件位于 `config/game_config.json`，包含以下主要配置：

- **游戏设置**：窗口大小、FPS、网格大小等
- **食物配置**：各种食物的属性和生成概率
- **星星配置**：星星的生成间隔和持续时间
- **敌人配置**：敌人数量和移动速度
- **障碍物配置**：障碍物组数量和每组大小

详细配置说明请参考 `config/README.md`。

## 开发工具

### 配置工具
- `scripts/config_tools.py`：配置文件管理工具

### 图形工具
- `scripts/draw_ui/create_game_sprites.py`：生成游戏精灵图片
- `scripts/draw_ui/create_star_image.py`：生成星星图片

### 测试工具
- `tests/`：完整的测试套件，包含功能测试和可视化测试

## 技术特点

- **模块化设计**：每个功能独立成类，便于维护和扩展
- **面向对象**：充分利用OOP特性，代码结构清晰
- **配置驱动**：通过配置文件控制游戏行为，无需修改代码
- **精美图形**：使用精灵图片，提供更好的视觉体验
- **完整测试**：包含单元测试、集成测试和可视化测试
- **详细注释**：所有类和方法都有中文注释
- **可扩展性**：易于添加新功能或修改现有功能
- **代码复用**：各模块可独立使用

## 开发环境

- Python 3.6+
- Pygame 2.0+

## 项目管理

本项目使用Git进行版本控制，包含以下分支管理工具：

- `git_branch_guide.md`：分支管理指南
- `git_remote_guide.md`：远程仓库管理指南
- `setup_remote.sh/.bat`：远程仓库设置脚本
- `init_git.sh/.bat`：Git初始化脚本

## 作者

基于原始贪吃蛇游戏重构，采用面向对象编程和模块化设计，加入配置系统、图形系统和完整的测试覆盖。
