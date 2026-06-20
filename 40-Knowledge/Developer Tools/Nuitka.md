---
title: Nuitka
aliases: []
type: note
created: 2025-08-05
area: Developer Tools
status: active
review: pending
tags:
  - python
---
> [!info] 导航
> [[40-Knowledge/Developer Tools/Developer Tools|返回工具索引]]

Nuitka是一个将Python代码编译为C/C++并生成高效可执行文件的工具，显著提升运行性能且无需依赖Python环境。



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
