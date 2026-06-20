---
title: Visual Studio
aliases: []
type: note
created: 2021-01-25
area: Developer Tools
status: active
review: reviewed
tags:
  - c
  - cpp
---
> [!info] 导航
> [[40-Knowledge/Developer Tools/Developer Tools|返回工具索引]]

Visual Studio是微软公司的集成开发环境（IDE），用于开发Windows应用程序。它提供了丰富的工具和功能，用于编写、调试和部署C++代码。



## Visual Studio使用scanf和printf函数出现报错的解决方法

在文件头部加入下面这段代码

```cpp
#define _CRT_SECURE_NO_WARNINGS
```

## 创建新文件时自动生成#define _CRT_SECURE_NO_WARNINGS的方法

在newc++file文件中加入下面这段代码

```cpp
#define _CRT_SECURE_NO_WARNINGS
```

newc++file文件位置在`Microsoft Visual Studio\Common7\IDE\VC\vcprojectitems\newc++file`
