---
title: Java后端
date: 2022-09-15 20:35:05
categories:
    - 后端
tags:
    - Java
---

这是一篇Java后端学习的博客，讲述Java的一些配置，文章是基于Ubuntu系统配置的。

<!--more-->

## 安装OpenJDK（Java环境）

{% note info %}
headless是OpenJDK的无头版本，即没有图形用户界面(GUI)的版本。无头版本通常用于服务器环境或不需要图形界面的应用程序。它们不包含与图形相关的库和工具，因此可以减少安装的大小和资源消耗。所以，openjdk-9-jre-headless中的headless表示没有图形界面。
{% endnote %}

可根据需要选择不同的jdk版本

```bash
apt install openjdk-11-jre-headless
```

## shell脚本

为了方便且快速地配置Java环境，这里我提供了自己编写的shell脚本，脚本的仓库为[java-web-environment](https://github.com/wliafe/java-web-environment)

## IntelliJ IDEA

IntelliJ IDEA的安装破解方法在我的博客{% post_link JetBrains %}里。

## Maven（Java包管理工具）

Java的包管理工具就是Maven，这是[Maven的官方网站](https://mvnrepository.com/)所有的Maven包都可以查到。

### Hutool

一个Java后端综合工具，这是他的[官方网址](https://www.hutool.cn/)
