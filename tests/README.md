# 测试文件夹

本目录包含贪吃蛇游戏的所有测试脚本，用于验证游戏功能的正确性。

## 测试文件说明

### `test_game_integration.py` - 游戏完整性测试
**主要测试脚本**，测试游戏的所有核心功能和系统集成：

- 配置系统加载测试
- 精灵图片加载测试  
- 游戏引擎初始化测试
- 蛇的基本功能测试
- 食物系统功能测试

**运行方式：**
```bash
python tests/test_game_integration.py
```

### `test_sprites.py` - 精灵系统测试
测试游戏中所有图片精灵的加载和显示：

- 验证所有精灵图片是否正确加载
- 可视化显示所有精灵
- 交互式精灵预览窗口

**运行方式：**
```bash
python tests/test_sprites.py
```

### `test_food_config.py` - 食物配置测试
测试食物系统的配置功能：

- 验证食物类型配置
- 测试食物生成概率
- 检查食物消息系统
- 统计食物生成分布

**运行方式：**
```bash
python tests/test_food_config.py
```

### `test_imports.py` - 模块导入测试
测试项目中所有模块的导入功能：

- 验证核心模块导入
- 验证实体模块导入  
- 验证UI模块导入
- 验证包级别导入

**运行方式：**
```bash
python tests/test_imports.py
```

## 快速测试

### 运行所有测试
```bash
# 主要完整性测试
python tests/test_game_integration.py

# 模块导入测试
python tests/test_imports.py

# 如果需要可视化测试
python tests/test_sprites.py
python tests/test_food_config.py
```

### 测试结果说明

**完整性测试结果：**
- ✓ 表示测试通过
- ✗ 表示测试失败
- 最终会显示通过率和总结

**精灵测试结果：**
- 会打开一个窗口显示所有加载的精灵
- 按ESC键退出预览

**食物测试结果：**
- 显示食物配置信息
- 显示100次生成的统计结果
- 显示各种食物的消息

## 测试覆盖范围

### 配置系统
- [x] 配置文件加载
- [x] 各模块配置获取
- [x] 配置验证

### 图片系统  
- [x] 精灵图片加载
- [x] 精灵管理器功能
- [x] 图片显示功能

### 游戏核心
- [x] 游戏引擎初始化
- [x] 蛇的移动和增长
- [x] 食物生成和类型
- [x] UI系统集成

### 系统集成
- [x] 配置与游戏逻辑集成
- [x] 精灵与渲染系统集成
- [x] 各模块间通信

## 添加新测试

1. 在 `tests/` 目录下创建新的测试文件
2. 文件命名格式：`test_<功能名>.py`
3. 添加必要的路径设置：
   ```python
   import sys
   import os
   sys.path.append(os.path.dirname(os.path.dirname(__file__)))
   ```
4. 编写测试函数并在 `if __name__ == "__main__":` 中调用

## 注意事项

- 测试脚本需要pygame环境
- 确保在项目根目录下运行测试
- 精灵测试需要图形界面支持
- 测试过程中会临时初始化pygame，测试完成后会自动清理

## 故障排除

**常见问题：**

1. **模块导入错误**
   - 确保在项目根目录运行测试
   - 检查Python路径设置

2. **pygame初始化失败**
   - 确保已安装pygame：`pip install pygame`
   - 检查系统音视频驱动

3. **配置文件错误**
   - 检查 `config/game_config.json` 是否存在
   - 验证JSON格式是否正确

4. **图片文件缺失**
   - 运行 `python scripts/draw_ui/create_game_sprites.py` 生成图片
   - 检查 `images/` 目录是否存在 