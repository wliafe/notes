---
title: Windows Subsystem for Linux (WSL)
date: 2025-05-26 12:41:16
categories: 
    - 工具
tags:
    - Windows
    - Linux
---

在Windows上直接编写代码存在不少问题，例如:

- 环境污染: 多个python版本，每个版本不同环境等
- 软件杂而多: 各种软件，多次修改环境变量，导致Windows环境变量乱七八糟
- 运行环境不匹配: 很多软件例如MySQL, Redis等，都比较适合运行在Linux上，但为了在Windows上运行，需要修改环境变量，安装软件，修改配置文件等，非常麻烦

Windows Subsystem for Linux (WSL)就可以很好地解决这些问题。

WSL是微软推出的一个功能，它允许用户在Windows上运行Linux环境，而不需要安装虚拟机，最详细的功能介绍和使用说明还是得看[微软的官方文档](https://learn.microsoft.com/zh-cn/windows/wsl/)

<!-- more -->

## WSL安装

这里只介绍一个安装命令

```bash
wsl --install
```

## Linux环境

当你执行了WSL安装命令，你的电脑会自动安装一个Linux发行版，默认情况下是Ubuntu，你也可以选择其他的Linux发行版。

### Linux安装

#### 命令安装

```bash
wsl --install [Linux发行版名称]
```

#### 图形化安装

打开Windows Store，搜索Ubuntu，点击安装。

![Windows Store 安装图](1.png)

安装完成后，你可以在Windows的开始菜单中找到Ubuntu，点击打开。

### Linux卸载

如果你使用命令安装的话，你可以使用以下命令卸载。

```bash
wsl --unregister <Linux发行版名称>
```

如果你使用图形化安装的话可以使用这个命令格式化Linux。

{% note warning %}
如果你想完全卸载图形化安装的Linux，就必须先使用这个命令注销Linux，目的是将注册表中有关Linux的信息删除，然后在Windows的开始菜单中找到Ubuntu，点击卸载。
{% endnote %}

#### 出错原因以及解决方案

{% note danger %}
Wsl/Service/CreateInstance/MountVhd/HCS/ERROR_FILE_NOT_FOUND
{% endnote %}

出现这个错误的可能原因是你曾经图形化安装过这个Linux发行版，但你卸载时没有使用`wsl --unregister <DistributionName>`命令注销Linux，导致注册表中有关Linux的信息没有删除，这时候你需要在注册表中将有关这个Linux的信息删除，然后再安装。

注册表路径如下

{% note info %}
\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Lxss\{特定标识符}
{% endnote %}

可以根据注册表内容判断特定标识符属于哪个Linux。

{% note danger %}
还有一种错误是你卸载了图形化安装的Linux，但因为某些原因你的Linux目录某些内容并没有删除，这就需要你手动删除Linux目录才能解决。
{% endnote %}

图形化安装的Linux的目录如下

{% note info %}
C:\Users\<UserName>\AppData\Local\Packages\(目录名含有Linux发行版名称)
{% endnote %}

命令安装的Linux的目录如下

{% note info %}
C:\Users\<UserName>\AppData\Local\wsl
{% endnote %}
