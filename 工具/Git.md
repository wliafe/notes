---
title: Git
date: 2022-03-16 09:15:57
categories:
    - 工具
tags:
---

Git作为版本管理工具是每一个程序员必备的技能，学会使用Git对我有很大的帮助。

- 版本管理工具，它可以将我写的代码存档，便于我在已编写好的代码上尝试下一步开发，出现错误时可以及时回退。
- 控制代码上传，在一个项目里，需要上传的代码其实是少数，占用空间并不大，而项目中很大一部分是软件包、执行文件、缓存等，这些文件并不需要上传到GitHub，Git提供了`.gitignore`文件，将不需要上传的文件添加到该文件中，可以避免上传不需要的文件。

当然Git还有其他功能例如团队合作、分支管理等，但目前我只用到上述这些功能，以后用到了会继续更新。

<!--more-->

## 安装Git

Git的安装教程网上数不胜数，其中[Git 详细安装教程（详解 Git 安装过程的每一个步骤）](https://blog.csdn.net/mukes/article/details/115693833)这一篇讲的非常详细，虽然他之后也可能会过时，但我仍想在这里引用他，我在这里就只提一下我自己在安装过程中修改的配置。

这是[Git下载地址](https://git-scm.com/)，选择最新版本下载后点击安装。

这里我选择全选

![Git选择安装组件](1.png)

这里我选择用main，这也是主流的选择，因为**Black Lives Matter（黑人的命也是命）**运动，很多人认为master不尊重黑人，因此改为main。

![初始化仓库主干名](2.png)

这里我选第二个

![Git 调整环境变量](3.png)

之后就一路next直到结束了。

## 配置Git

单机右键，打开Git Bush Here然后通过输入命令配置用户名和邮箱。

配置用户名

```bash
git config --global user.name <仓库的用户名>
```

配置用户邮箱

```bash
git config --global user.email <仓库的绑定邮箱>
```

查看用户名

```bash
git config --global user.name
```

查看用户邮箱

```bash
git config --global user.email
```

## Git链接仓库

一般的选择是使用ssh公私钥，但是现在可以直接使用账号密码登录的方式上传代码（无论是GitHub还是Gitee），只需要一次登录就可以上传多次，因此我不再配置ssh了，至于创建`.git`文件，我现在比较喜欢先创建仓库，然后clone仓库，克隆下来的仓库自带`.git`文件，不需要自己创建。

如下图，获取仓库HTTP网址。

![仓库HTTP网址](4.png)

### 直接克隆仓库

```bash
git clone <仓库HTTP网址>
```

### 创建`.git`文件，添加仓库网址

创建Git文件

```bash
git init
```

添加仓库网址

```bash
git remote add origin <仓库HTTP网址>
```

### 编写代码提交到仓库

从仓库中拉取文件覆盖本地文件夹

```bash
git pull origin main
```

添加本地的所有文件放入缓存区

```bash
git add .
```

为放入缓存中的文件添加说明

```bash
git commit -m <注释>
```

上传缓存中的文件到远程仓库

```bash
git push origin main
```

### 分支管理

查看本地分支

```bash
git branch
```

在本地新建分支

```bash
git branch <分支名>
```

切换本地分支

```bash
git checkout <分支名>
```

删除本地分支

```bash
git branch -d <分支名>
```

### 其他

取消文件或文件夹的版本控制

```bash
git rm -r --cached <要取消版本控制的文件或文件夹>
```

查看文件修改历史

```bash
git blame <file>
```

## Git代理设置

如果要用Git同步GitHub仓库，推荐使用代理客户端软件。

## `.gitignore`文件

`.gitignore`文件用于指定Git不应该跟踪的文件，详细的语法规则可以参考[`.gitignore`的官方文档](https://git-scm.com/docs/gitignore/zh_HANS-CN)。

我一般在创建仓库时使用仓库提供的`.gitignore`文件，或者创建的项目自带`.gitignore`文件，然后我会根据自己的需要添加部分配置。

例如，如果想忽略`node_modules`文件夹，忽略所有`.log`文件，那么就在`.gitignore`文件中添加以下内容：

```conf .gitignore
node_modules/
*.log
```

每一个程序员都应该养成在项目中设置`.gitignore`文件的习惯。

## git配置镜像

### Github镜像

[镜像链接](https://freevaults.com/github-mirror-daily-updates.html)

命令配置

```bash
git config --global url."https://bgithub.xyz/".insteadOf "https://github.com/"
```

或配置文件配置

```conf .gitconfig
[url "https://bgithub.xyz/"]
    insteadOf = https://github.com/
```

### Hugging Face镜像

命令配置

```bash
git config --global url."https://hf-mirror.com/".insteadOf "https://huggingface.co/"
```

或配置文件配置

```conf .gitconfig
[url "https://hf-mirror.com/"]
    insteadOf = https://huggingface.co/
```
