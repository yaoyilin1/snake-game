@echo off
chcp 65001 >nul
echo 正在初始化Git仓库...

REM 初始化Git仓库
git init

REM 添加所有文件到暂存区
git add .

REM 创建初始提交
git commit -m "Initial commit: Snake Game Project

- Complete modular snake game
- Multiple food types (small, medium, large)
- Star reward system (increase lives)
- Moving person enemies
- Obstacle system
- 9-level speed system
- 3 lives system
- Win condition (snake length reaches 100)
- Complete UI display system
- Chinese comments and prompts"

echo Git仓库初始化完成！
echo.
echo 可用的Git命令：
echo   git status          - 查看仓库状态
echo   git log             - 查看提交历史
echo   git remote add origin ^<远程仓库URL^>  - 添加远程仓库
echo   git push -u origin main  - 推送到远程仓库
echo.
pause 