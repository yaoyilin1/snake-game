# Git 分支管理指南

## 什么是Git分支？

Git分支是Git版本控制系统的核心功能，它允许您在不影响主代码的情况下进行开发。每个分支都是代码的一个独立版本，可以独立开发、测试和合并。

## 分支的基本概念

### 分支类型
- **主分支（master/main）**: 项目的稳定版本
- **开发分支（develop）**: 开发中的功能集成
- **功能分支（feature）**: 开发新功能
- **修复分支（hotfix）**: 紧急修复
- **发布分支（release）**: 准备发布

## 分支操作命令

### 查看分支
```bash
# 查看本地分支（当前分支用*标记）
git branch

# 查看所有分支（包括远程分支）
git branch -a

# 查看远程分支
git branch -r

# 查看分支详细信息
git branch -v
```

### 创建分支
```bash
# 创建新分支（不切换）
git branch <分支名>

# 创建并切换到新分支
git checkout -b <分支名>

# 创建基于特定提交的分支
git branch <分支名> <提交ID>

# 创建基于远程分支的本地分支
git checkout -b <本地分支名> origin/<远程分支名>
```

### 切换分支
```bash
# 切换到指定分支
git checkout <分支名>

# 切换到主分支
git checkout master
git checkout main

# 使用新的switch命令（Git 2.23+）
git switch <分支名>

# 创建并切换到新分支
git switch -c <分支名>
```

### 删除分支
```bash
# 删除本地分支（已合并）
git branch -d <分支名>

# 强制删除本地分支（未合并）
git branch -D <分支名>

# 删除远程分支
git push origin --delete <分支名>
```

### 合并分支
```bash
# 将指定分支合并到当前分支
git merge <分支名>

# 使用rebase合并（保持线性历史）
git rebase <分支名>

# 解决冲突后继续rebase
git rebase --continue

# 取消rebase
git rebase --abort
```

## 实际应用场景

### 场景1：开发新功能
```bash
# 1. 确保在主分支
git checkout master

# 2. 拉取最新代码
git pull origin master

# 3. 创建功能分支
git checkout -b feature/new-game-mode

# 4. 开发功能
# ... 编写代码 ...

# 5. 提交更改
git add .
git commit -m "Add new game mode feature"

# 6. 推送到远程
git push origin feature/new-game-mode

# 7. 创建Pull Request（在GitHub/GitLab上）
# 8. 合并后删除分支
git checkout master
git pull origin master
git branch -d feature/new-game-mode
```

### 场景2：修复Bug
```bash
# 1. 从主分支创建修复分支
git checkout master
git checkout -b hotfix/bug-fix

# 2. 修复Bug
# ... 修复代码 ...

# 3. 提交修复
git add .
git commit -m "Fix: 修复游戏崩溃问题"

# 4. 推送到远程
git push origin hotfix/bug-fix

# 5. 合并到主分支
git checkout master
git merge hotfix/bug-fix

# 6. 删除修复分支
git branch -d hotfix/bug-fix
```

### 场景3：版本发布
```bash
# 1. 创建发布分支
git checkout develop
git checkout -b release/v1.2.0

# 2. 版本号更新
# ... 更新版本号 ...

# 3. 提交版本更新
git add .
git commit -m "Bump version to v1.2.0"

# 4. 合并到主分支
git checkout master
git merge release/v1.2.0

# 5. 打标签
git tag -a v1.2.0 -m "Release version 1.2.0"

# 6. 合并到开发分支
git checkout develop
git merge release/v1.2.0

# 7. 删除发布分支
git branch -d release/v1.2.0
```

## 分支切换的注意事项

### 1. **工作区状态**
```bash
# 切换分支前确保工作区干净
git status

# 如果有未提交的更改，可以选择：
# 1. 提交更改
git add .
git commit -m "Save current work"

# 2. 暂存更改
git stash

# 3. 丢弃更改
git checkout -- .
```

### 2. **冲突处理**
```bash
# 合并时出现冲突
git merge feature/branch

# 查看冲突文件
git status

# 手动解决冲突后
git add <冲突文件>
git commit -m "Resolve merge conflicts"
```

### 3. **远程分支同步**
```bash
# 获取远程分支信息
git fetch origin

# 查看所有分支
git branch -a

# 创建本地分支跟踪远程分支
git checkout -b <本地分支名> origin/<远程分支名>
```

## 常用分支命名规范

### 功能分支
```
feature/user-authentication
feature/game-multiplayer
feature/leaderboard-system
```

### 修复分支
```
hotfix/crash-fix
hotfix/security-patch
hotfix/performance-issue
```

### 发布分支
```
release/v1.0.0
release/v2.1.0
release/v3.0.0-beta
```

### 开发分支
```
develop
staging
testing
```

## 高级分支操作

### 1. **分支重命名**
```bash
# 重命名当前分支
git branch -m <新分支名>

# 重命名指定分支
git branch -m <旧分支名> <新分支名>
```

### 2. **分支比较**
```bash
# 比较两个分支的差异
git diff branch1..branch2

# 查看分支合并图
git log --graph --oneline --all
```

### 3. **分支备份**
```bash
# 创建分支备份
git branch backup/feature-branch feature-branch

# 推送到远程备份
git push origin backup/feature-branch
```

## 最佳实践

### 1. **分支策略**
- 主分支保持稳定
- 功能开发使用独立分支
- 及时删除已合并的分支
- 使用有意义的分支名称

### 2. **提交规范**
```bash
# 使用清晰的提交信息
git commit -m "feat: 添加新游戏模式"
git commit -m "fix: 修复碰撞检测bug"
git commit -m "docs: 更新README文档"
```

### 3. **定期清理**
```bash
# 删除已合并的本地分支
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d

# 删除已合并的远程分支引用
git remote prune origin
```

## 常见问题解决

### 问题1：切换分支失败
```bash
# 错误：error: Your local changes would be overwritten
# 解决：暂存或提交更改
git stash
git checkout <分支名>
git stash pop  # 恢复更改
```

### 问题2：分支不存在
```bash
# 错误：error: pathspec 'branch-name' did not match any file(s)
# 解决：检查分支名称
git branch -a
git checkout <正确的分支名>
```

### 问题3：远程分支更新
```bash
# 获取远程分支更新
git fetch origin
git checkout <分支名>
git pull origin <分支名>
```

## 总结

Git分支管理是团队协作开发的核心技能：

✅ **分支创建和切换** - 独立开发环境
✅ **分支合并和冲突解决** - 代码集成
✅ **分支命名规范** - 团队协作效率
✅ **分支清理和维护** - 仓库整洁

掌握这些操作，您就能高效地进行团队协作和项目管理！ 