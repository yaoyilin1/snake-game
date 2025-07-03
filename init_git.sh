#!/bin/bash

echo "正在初始化Git仓库..."

# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 创建初始提交
git commit -m "初始提交：贪吃蛇游戏项目

- 完整的模块化贪吃蛇游戏
- 包含多种食物类型（小、中、大）
- 星星奖励系统（增加生命值）
- 移动的小人敌人
- 障碍物系统
- 9级速度系统
- 3条生命系统
- 胜利条件（蛇长度达到100）
- 完整的UI显示系统
- 中文注释和提示"

echo "Git仓库初始化完成！"
echo ""
echo "可用的Git命令："
echo "  git status          - 查看仓库状态"
echo "  git log             - 查看提交历史"
echo "  git remote add origin <远程仓库URL>  - 添加远程仓库"
echo "  git push -u origin main  - 推送到远程仓库"
echo "" 