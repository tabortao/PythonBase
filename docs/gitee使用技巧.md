# Gitee简易入门教程
```bash
# Git 全局设置:
git config --global user.name "tabor"
git config --global user.email "15750647+tabortao@user.noreply.gitee.com"

# 创建 git 仓库:
mkdir PythonBase
cd PythonBase
git init 
touch README.md
git add README.md
git commit -m "first commit"
git remote add origin https://gitee.com/tabortao/PythonBase.git
git push -u origin "master"

# 已有仓库?
cd existing_git_repo
git remote add origin https://gitee.com/tabortao/PythonBase.git
git push -u origin "master" # git push -u origin "main"
```
## 如何把GitHub换位Gitee
```bash
git remote remove origin # 删除远程仓库
git remote add origin git remote add origin https://gitee.com/tabortao/PythonBase.git # 添加新的远程仓库
```
