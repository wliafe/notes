---
title: Conda
date: 2025-05-25 16:53:57
categories:
    - 工具
tags:
    - Python
---

本文主要介绍Conda这个工具，Conda是一个用于管理Python环境的工具，它可以帮助我们创建、管理和切换不同的Python环境，避免环境冲突。同时，Conda还可以作为Python包管理器使用，我们可以使用Conda来安装、升级、卸载Python包。然而，pip也可以作为Python包管理器使用，pip与Conda相比，他的包会更加丰富，因为pip有着更大的开源社区。但Conda对包的依赖管理更加严格，使用Conda可以有效避免包之间的冲突。建议优先使用conda安装包。

关于Conda的详细内容，我们可以参考[Conda官方文档](https://www.anaconda.com/docs/main)。

<!-- more -->

## Miniconda安装

Miniconda的安装比较简单，从[Miniconda官网](https://www.anaconda.com/download/success)下载适用于Windows、macOS或Linux的Miniconda安装包，然后按照安装向导安装即可。

## Conda

### Conda管理

获取版本号

```bash
conda --version
```

conda升级

```bash
conda update conda
```

### Conda环境管理

创建环境

```bash
conda create -n <env-name> [list of package]
```

创建特定python版本的环境

```bash
conda create -n <env-name> python==<version>
```

{% note warning %}
如果没有指定python的版本，conda会选择base环境的python版本。
{% endnote %}

激活环境

```bash
conda activate <env-name>
```

退出当前环境

```bash
conda deactivate
```

复制环境

```bash
conda create -n <new-env-name> --clone <old-env-name>
```

列出所有环境

```bash
conda env list
```

删除环境

```bash
conda env remove -n <env-name>
```

### Conda包管理

Conda包管理是在当前环境下进行的，对当前环境的操作并不会影响其他环境。

安装包

```bash
conda install <package-name>
```

安装特定版本的包

```bash
conda install <package-name>=<version>
```

查看已安装包

```bash
conda list
```

卸载包

```bash
conda remove <package-name>
```

更新包

```bash
conda update <package-name>
```

更新所有包

```bash
conda update --all
```

搜索包（可以模糊搜索）

```bash
conda search <search-term>
```
