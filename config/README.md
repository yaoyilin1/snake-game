# 游戏配置系统

本目录包含贪吃蛇游戏的配置文件和管理工具。

## 文件结构

```
config/
├── __init__.py              # 配置包初始化
├── config_manager.py        # 配置管理器类
├── game_config.json         # 主配置文件
└── README.md               # 本说明文件
```

## 配置文件说明

### `game_config.json` - 主配置文件

包含游戏的所有可配置参数，分为以下几个部分：

#### 窗口配置 (`window`)
- `title`: 游戏窗口标题
- `game_width`: 游戏区域宽度（像素）
- `game_height`: 游戏区域高度（像素）
- `ui_height`: UI区域高度（像素）
- `fps_limit`: 帧率限制

#### 蛇配置 (`snake`)
- `initial_position`: 蛇的初始头部位置 [x, y]
- `initial_body`: 蛇的初始身体坐标列表
- `initial_direction`: 初始移动方向
- `cell_size`: 蛇身格子大小
- `color`: 蛇的颜色 [R, G, B]

#### 速度配置 (`speed`)
- `levels`: 速度等级数组（每级对应的FPS）
- `max_level`: 最大速度等级
- `speedup_interval`: 自动提速间隔（毫秒）

#### 食物配置 (`food`)
- `types`: 食物类型数组，每个包含：
  - `name`: 食物名称
  - `color`: 食物颜色 [R, G, B]
  - `length_increase`: 增加的蛇身长度
  - `probability`: 出现概率（总和应为1.0）

#### 星星配置 (`star`)
- `spawn_probability`: 每帧生成概率
- `duration`: 存在时间（毫秒）
- `color`: 星星颜色 [R, G, B]
- `image_path`: 星星图片路径

#### 障碍物配置 (`obstacles`)
- `total_count`: 障碍物总数
- `group_count`: 障碍物组数
- `color`: 障碍物颜色 [R, G, B]

#### 敌人配置 (`enemies`)
- `person_count`: 小人敌人数量
- `move_interval`: 移动间隔（帧数）
- `color`: 敌人颜色 [R, G, B]
- `directions`: 可能的移动方向列表

#### 游戏规则配置 (`gameplay`)
- `initial_lives`: 初始生命数
- `win_condition_length`: 胜利条件（蛇长度）
- `collision_penalty`: 碰撞扣除生命数

#### UI配置 (`ui`)
- `colors`: UI颜色配置
  - `background`: 游戏背景色
  - `ui_background`: UI区域背景色
  - `separator`: 分隔线颜色
  - `score_text`: 分数文字颜色
  - `lives_text`: 生命文字颜色
  - `info_text`: 信息文字颜色
  - `message_text`: 消息文字颜色
  - `message_bg`: 消息背景色
  - `message_border`: 消息边框色
- `fonts`: 字体配置
  - `score_size`: 分数字体大小
  - `info_size`: 信息字体大小
  - `message_size`: 消息字体大小
  - `score_font`: 分数字体名称
  - `message_font`: 消息字体名称
- `message_duration`: 消息显示时间（毫秒）

#### 控制配置 (`controls`)
- `up_keys`: 向上移动键列表
- `down_keys`: 向下移动键列表
- `left_keys`: 向左移动键列表
- `right_keys`: 向右移动键列表
- `exit_key`: 退出游戏键
- `refresh_key`: 刷新障碍物键

#### 消息配置 (`messages`)
- `turn_message`: 转弯时的提示消息
- `obstacle_refresh`: 刷新障碍物消息
- `star_collected`: 收集星星消息
- `caught_by_person`: 被敌人抓住消息
- `food_messages`: 不同食物的消息
- `game_over`: 游戏结束消息
- `game_win`: 游戏胜利消息

## 配置管理工具

使用 `scripts/config_tools.py` 可以管理配置：

```bash
# 验证配置文件
python scripts/config_tools.py validate

# 查看当前配置
python scripts/config_tools.py info

# 导出配置模板
python scripts/config_tools.py export

# 重置为默认配置
python scripts/config_tools.py reset

# 交互式修改配置
python scripts/config_tools.py modify
```

## 在代码中使用配置

```python
from config import ConfigManager

# 创建配置管理器
config = ConfigManager()

# 获取配置值
window_title = config.get('window.title')
snake_color = config.get_color('snake.color')
initial_lives = config.get('gameplay.initial_lives', 3)

# 获取整个配置组
window_config = config.get_window_config()
food_config = config.get_food_config()

# 更新配置
config.update_config('gameplay.initial_lives', 5)
config.save_config()
```

## 自定义配置

1. **修改现有配置**: 直接编辑 `game_config.json` 文件
2. **使用配置工具**: 运行 `python scripts/config_tools.py modify`
3. **程序化修改**: 使用 `ConfigManager` 类的方法

## 注意事项

- 修改配置后需要重启游戏才能生效
- 食物类型的概率总和应该为 1.0
- 颜色值应该在 0-255 范围内
- 坐标值应该是 10 的倍数（对应格子大小）
- 速度等级数组长度应该等于 max_level

## 备份和恢复

- 配置文件支持版本控制
- 可以创建多个配置文件用于不同难度
- 使用配置工具可以快速重置为默认值 