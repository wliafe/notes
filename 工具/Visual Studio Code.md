---
title: Visual Studio Code
date: 2022-03-15 23:27:00
categories:
    - 工具
tags:
---

Visual Studio Code简称（VSCode）是微软开发的一款免费的代码编辑器，支持多种编程语言，支持插件扩展。当我要编写简单C语言、C++语言、Python语言、Markdown文件时，使用VSCode是非常方便的。由于VSCode功能强大，本身自带的功能就很多，而我个人对VSCode功能的发掘并不深，因此这里记录一些我对VSCode发掘的内容，方便日后使用。

<!--more-->

## 插件

VSCode有几个必用的插件，并不服务于某个语言，是通用插件。

### Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code

语言插件，提供简体中文语言支持。

![Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code](1.png)

### Trae AI (formerly MarsCode): Coding Assistant

现在是AI时代，这是我比较喜欢使用的AI代码插件，提供代码补全、代码解释、代码格式化等功能，他是免费的。

![Trae AI (formerly MarsCode): Coding Assistant](2.png)

## 工作区

工作区是VSCode管理项目的工具，设置工作区有多种好处。通过打开工作区可以一次性打开电脑中的多个项目，而不需要每次都打开一个项目。工作区还是一个配置空间，工作区的配置对工作区内的项目都有效。设置一个工作去非常简单。

点击`文件`->`新建窗口`，就打开了一个新的工作区。

![打开工作区](3.gif)

选择`文件`->`将工作区另存为`，就可以将工作区保存为一个文件。

![保存工作区](4.gif)

添加项目到工作区。

![添加项目到工作区](5.gif)

之后点击保存的工作区，就可看到工作区内添加的项目了。

## 配置文件

我们都知道可以在VSCode的设置中配置VSCode的一些功能，比如主题、字体、插件等，但VSCode的设置内容浩如烟海，我们如何知道自己修改了那些配置呢？又如何知道自己修改的配置的作用范围呢？接下来的内容会告诉你答案。

VSCode的配置文件设置非常巧妙，首先VSCode下载安装后有自己的默认配置，当我们修改配置时，VSCode会将用户修改的部分写入一个`.json`文件，这个文件就是`settings.json`。

![打开`settings.json`文件](6.gif)

`settings.json`文件的内容就是我们修改的VSCode的配置内容，在`settings.json`中修改配置和在设置中修改配置是一样的。

![`settings.json`文件图](7.png)

VSCode的配置设置很像代码语言的命名空间，简单的说，用户设置相当于全局作用域，工作区相当于一个小一点的作用域，再往下还有项目一级的作用域。而配置文件的优先级为`项目配置文件`>`工作区配置文件`>`用户配置文件`>`默认配置`。而用户配置文件是可以云同步的，所以一般的设置我会选择修改用户配置，而针对某台电脑的配置我会选择修改工作区配置文件，针对项目的设置我才会选择生成并修改项目配置文件。

可以通过设置页面打开不同的配置文件。

![设置页面图](8.png)

## 代码片段

编写代码可以自己定义代码片段，代码片段可以在不同的语言中使用。

比如我想定义一个Markdown语言的代码片段。

![代码片段图](9.gif)

根据文件注释中的样例配置自己的代码片段。

![代码片段](10.png)

## 远程服务器`.vscode-server`下载失败问题

当我们使用VSCode远程连接服务器时，VSCode会在服务器上安装一个`.vscode-server`目录，如果网络不好，可能会导致下载失败，从而无法连接服务器。解决方法是手动下载`.vscode-server`目录并上传到服务器上。

首先查看`帮助->关于`，查看VSCode的提交版本号`commit_id`。

![关于图](11.png)

记下提交版本号`commit_id`，然后将`https://update.code.visualstudio.com/commit:${commit_id}/server-linux-x64/stable`中的`commit_id`替换为自己的`commit_id`，下载对应的文件。

```bash
mkdir -p ~/.vscode-server/bin # 创建目录
```

```bash
rm -rf ~/.vscode-server/bin/* # 清空原有文件
```

```bash
tar -zxf vscode-server-linux-x64.tar.gz # 解压程序包
```

```bash
mv vscode-server-linux-x64  ~/.vscode-server/bin/${commit_id} # 移动并重命名程序
```

重启VSCode，即可连接服务器。
