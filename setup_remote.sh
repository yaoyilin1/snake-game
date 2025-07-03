#!/bin/bash

echo "========================================"
echo "贪吃蛇游戏 - 远程仓库设置工具"
echo "========================================"
echo ""

echo "请选择您要使用的Git托管服务："
echo "1. GitHub"
echo "2. GitLab"
echo "3. Gitee (码云)"
echo "4. 自定义URL"
echo ""
read -p "请输入选择 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "请按照以下步骤操作："
        echo "1. 访问 https://github.com"
        echo "2. 登录您的账户"
        echo "3. 点击右上角的 \"+\" 号，选择 \"New repository\""
        echo "4. 输入仓库名称（例如：snake-game）"
        echo "5. 选择公开或私有"
        echo "6. 不要勾选 \"Initialize this repository with a README\""
        echo "7. 点击 \"Create repository\""
        echo "8. 复制仓库URL（格式如：https://github.com/用户名/仓库名.git）"
        echo ""
        read -p "请输入您的GitHub仓库URL: " repo_url
        ;;
    2)
        echo ""
        echo "请按照以下步骤操作："
        echo "1. 访问 https://gitlab.com"
        echo "2. 登录您的账户"
        echo "3. 点击 \"New project\""
        echo "4. 输入项目名称"
        echo "5. 选择可见性级别"
        echo "6. 点击 \"Create project\""
        echo "7. 复制项目URL"
        echo ""
        read -p "请输入您的GitLab项目URL: " repo_url
        ;;
    3)
        echo ""
        echo "请按照以下步骤操作："
        echo "1. 访问 https://gitee.com"
        echo "2. 登录您的账户"
        echo "3. 点击 \"新建仓库\""
        echo "4. 输入仓库名称"
        echo "5. 选择公开或私有"
        echo "6. 点击 \"创建\""
        echo "7. 复制仓库URL"
        echo ""
        read -p "请输入您的Gitee仓库URL: " repo_url
        ;;
    4)
        echo ""
        read -p "请输入您的自定义仓库URL: " repo_url
        ;;
    *)
        echo "无效选择！"
        exit 1
        ;;
esac

echo ""
echo "正在设置远程仓库..."
git remote add origin "$repo_url"

echo ""
echo "正在推送到远程仓库..."
git push -u origin master

echo ""
echo "========================================"
echo "设置完成！"
echo "========================================"
echo "您的项目已成功推送到远程仓库。"
echo "仓库URL: $repo_url"
echo ""
echo "后续操作："
echo "- 查看仓库状态: git status"
echo "- 查看提交历史: git log"
echo "- 推送新更改: git push"
echo "- 拉取远程更改: git pull"
echo "" 