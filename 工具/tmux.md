---
title: tmux
date: 2025-10-30 10:10:30
categories: 工具
tags:
---

tmux 是一个终端复用器，它可以在一个终端窗口中运行多个会话。可以在远程连接退出后，重新连接到之前的会话。

<!-- more -->

## 安装

```bash
sudo apt install tmux
```

## 配置文件

### 启用鼠标支持（拖动滚动、选择文本）

实现在tmux中使用鼠标滚动查看历史输出。

在`~/.tmux.conf`文件中添加以下内容。

```conf .tmux.conf
set -g mouse on
```
