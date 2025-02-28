# Git

## 参考资料

* [Git book](https://git-scm.com/book/zh/v2) - 标准的文档 - 4
* [How to Write a Git Commit Message](https://github.com/jlevy/the-art-of-command-line/blob/master/README-zh.md) - 教你写提交信息 - 5

## 概念

* Git 是一种分布式版本管理工具, 在中央服务器保存所有文件与历史快照的同时, **每次建立分支都克隆整个仓库**
* Git 中所有的数据在存储前都计算校验和,Git 数据库中保存的信息都是以文件内容的 SHA-1 哈希值来索引
* Git 有三种状态 modified staged committed 对应工作区 暂存区 (只是索引) 以及 Git 目录
* `~/.gitconfig` 配置忽略文件
* `~/.config/git/config` 配置文件
* 安装完 Git 之后, 要做的第一件事就是设置你的用户名和邮件地址

```shell
git --version # 看一眼

git config --global user.name "Your Name Here"
git config --global user.email "your_email@youremail.com"
# 设置 name & email

git config --global credential.helper osxkeychain
# 设置缓存凭据工具
```

## Git 基本操作

### 创建, 提交, 配置

* `git init` 在当前目录建立 `.git` 初始化
* `git clone <url> name` 克隆到当前目录, name 可选
* `git status` 检查文件状态
* `git add name` 跟踪并暂存新文件, 暂存已修改文件, 暂存只保存当前版本, 未提交之前再次修改, 需要再次暂存
* `git status -s` 检查文件状态, 只显示简短信息
* `.gitignore` 指明需要忽视的文件, 标准的 glob 模式匹配, 递归地应用在整个工作区中
* `git diff` 比较工作目录中当前文件和暂存区域快照之间的差异
* `git diff -staged` 将比对已暂存文件与最后一次提交的文件差异
* `git commit` 将提交修改并调用 shell 的默认编辑器写提交消息 -a 自动 add 并提交

### 撤销

* `git rm name` 删除文件
* `git mv` 相当于重命名
* `git log` 看历史更改提交人, mail, 提交消息
* `git reset --soft name` 回退版本, 保留工作区, 保留暂存区
* `git reset --hard name` 都不保留
* `git reset --mixed name` 保留工作区, 不保留暂存区
* `git checkout -- rope_name` 用仓库中的版本替换

### 仓库

* `git remote -v` 看仓库
* `git remote add <shortname> <url>` 添加一个新的远程 Git 仓库, 可以用 shortname 代替该仓库 url
* `git fetch <url>` 拉取差异, 但是不自动合并
* `git pull <url>` 并且自动合并
* `git push origin master` 推送到某仓库某分支, 这是默认的 name
* `git remote show <remote>` 看仓库信息
* `git remote rename` 重命名
* `git remote rm` 删除仓库

### 分支

* `git branch name` 建立分支
* `git branch` 列出分支
* `git checkout testing` 移动到该分支
* `git merge hotfix` 将当前分支和某分支合并
* `git banch --merged` 列出已合并的分支
* `git branch -d name` 删除分支
* `git branch -m old new` 重命名分支
* `git checkout -b sf origin/serverfix` 从远程分支创建跟踪并切换到新分支
* `git push origin --delete serverfix` 删除远程分支
* `git rebase master serverfix` 合并分支 (变基)

## GitHub

* 交友网站

## GitLab

* 私有化部署
