---
title: Nuitka
date: 2025-08-05 14:18:29
categories:
    - 工具
tags:
    - Python
---

Nuitka是一个将Python代码编译为C/C++并生成高效可执行文件的工具，显著提升运行性能且无需依赖Python环境。

<!--more-->

## 文档

[官方文档](https://nuitka.net/)

关于Nuitka的命令行参数信息我在官方文档并没有找到，这里是[`nuitka --help`文档中文翻译](https://nuitka-doc-zh.erduotong.com/docs/--help.html)

英文命令行参数文档

```bash
nuitka --help
```

## 安装

```bash
uv add nuitka
```

## 编译

```bash
nuitka --onefile --remove-output main.py
```
