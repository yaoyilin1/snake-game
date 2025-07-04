# 脚本目录

这个目录包含各种工具脚本，用于游戏开发和资源生成。

## 目录结构

```
scripts/
├── __init__.py          # 脚本包初始化文件
├── draw_ui/             # UI绘制相关脚本
│   ├── __init__.py      # draw_ui包初始化文件
│   └── create_star_image.py  # 生成五角星图片的脚本
└── README.md            # 本说明文件
```

## 使用方法

### 生成五角星图片

要重新生成星星图片，可以运行：

```bash
# 方法1：直接运行脚本
cd scripts/draw_ui
python create_star_image.py

# 方法2：作为模块导入使用
python -c "from scripts.draw_ui import create_star_image; create_star_image()"
```

## 扩展说明

这个目录结构为将来添加更多工具脚本提供了良好的组织方式：

- `draw_ui/`: 用于生成UI相关图像资源的脚本
- 将来可以添加：
  - `audio/`: 音频处理脚本
  - `map_generator/`: 地图生成脚本
  - `asset_tools/`: 资源管理工具
  - 等等... 