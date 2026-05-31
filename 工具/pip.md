---
title: pip
date: 2025-08-01 09:00:33
categories:
    - 工具
tags:
    - Python
---

pip是Python官方的包管理工具，它可以用来安装、升级、卸载Python包。

有关pip的文档和包源，我们可以参考[pip官方文档](https://pypi.org/)，基本使用参考[pip安装包](https://packaging.python.org/en/latest/tutorials/installing-packages/)

<!-- more -->

## pip常用命令

安装包

```bash
pip3 install <package-name>
```

安装特定版本的包

```bash
pip3 install <package-name>==<version>
```

查看所有已安装包

```bash
pip3 list
```

卸载包

```bash
pip3 uninstall <package-name>
```

更新包

```bash
pip3 install --upgrade <package-name>
```

搜索包

```bash
pip3 search <search-term>
```

## pip换清华源加快速度

临时使用

```bash
pip3 install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package
```

设为默认

```bash
pip3 config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

恢复官方源

```bash
pip3 config unset global.index-url
```

## 创建一个库并发布到PyPI

这里我使用{% post_link uv %}来管理项目。

### 创建项目

按照{% post_link GitHub %}中的仓库管理体系创建仓库，并将项目clone到本地。

### 初始化项目

由于我要创建一个库，所以初始化时要加入`--lib`参数。

```bash
uv init --lib
```

### 安装依赖

```bash
uv add <package-name>
```

### 编写代码

在项目中编写代码，确保代码符合Python的规范。

### 编写`pyproject.toml`文件

参考[pip官方文档打包一个项目](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

修改项目根目录下的`pyproject.toml`文件，用于描述项目的元数据和依赖信息。

其中，project-name为项目名称要与包名相同，project-description为项目描述。

```toml pyproject.toml
[project]
name = "<project-name>"
version = "1.0.0"
description = "<project-description>"
readme = "README.md"
authors = [
    { name = "<username>", email = "<email>" }
]
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = []

[project.urls]
Homepage = "https://github.com/<username>/<repository-name>"
Issues = "https://github.com/<username>/<repository-name>/issues"

[build-system]
requires = ["uv_build>=0.8.4,<0.9.0"]
build-backend = "uv_build"
```

使用`module-name`参数可以实现项目名和包名不同的效果，具体参考[uv官方文档build-backend部分](https://docs.astral.sh/uv/concepts/build-backend/#modules)。

```toml
[tool.uv.build-backend]
module-name = "<package-name>"
```

### 创建workflow

参考[uv官方文档GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/)

创建workflow文件的目的是实现自动发布功能，为以后包的更新提供方便。

在`.github/workflows`目录下添加文件`publish-to-pypi.yml`文件，用于描述发布项目的工作流程。

文件内容如下：

```yml publish-to-pypi.yml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v6

      - name: Install dependencies
        run: uv sync

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.PYPI_API_TOKEN }}
```

每当创建一个tag时，workflow就会触发，自动发布项目到PyPI。

### 添加Trusted Publisher Management

注册一个PyPI账号，选择Publishing，添加Trusted Publisher。

![Trusted Publisher Management](1.png)

添加GitHub Trusted Publisher。

![Trusted Publisher表单](2.png)

这里最常见的问题就是撞名，没办法，一个一个试吧。

{% note danger %}
PyPI的包名是不可重复的，而且已创建项目的名称即使删除，上传的项目版本依然存在，如果想要重建，只能使用更高的版本号，所以在创建项目名称和发布版本号时要慎之又慎！！！关于PyPI的包名已存在问题，参考[Filename or contents already exists](https://pypi.org/help/#file-name-reuse)
{% endnote %}

### 生成PyPI Token

在Account settings中生成token。

![PyPI账号设置](3.png)

找到API tokens

![PyPI token生成](4.png)

按要求填写表单，生成token。

![PyPI token](5.png)

### 将Token添加到GitHub Actions

在GitHub仓库中，选择Settings，选择Secrets and variables，选择Actions，点击New repository secret。

![Secrets](6.png)

填写从PyPI账号获取的token。

![添加Secrets](7.png)

### 发布项目

在Gitee中创建一个tag，GitHub Actions就会自动执行workflow，发布项目到PyPI。

## 给PyPI项目添加文档

我使用的文档工具是[Sphinx](https://sphinx-doc.cn/en/master/index.html)，我使用的文档主题是[sphinx_rtd_theme](https://rtd.sphinx-doc.cn/en/stable/index.html)，我的文档发布平台是[Read the Docs](https://app.readthedocs.org/dashboard/)。

### Sphinx

#### 安装

```bash
uv add sphinx
```

#### 初始化

```bash
sphinx-quickstart docs
```

#### 配置

配置项目信息，其中，通过代码获取版本号填入`release`变量。

```python conf.py
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # 项目根目录

sys.path.insert(0, str(ROOT / "src"))

if sys.version_info >= (3, 11):
    # Python 3.11 或更高
    import tomllib as tomli
else:
    # Python 3.8 ~ 3.10
    import tomli

with open(ROOT / "pyproject.toml", "rb") as f:
    config = tomli.load(f)

project = "wliafe-mltools"
copyright = "2025, wliafe"
author = "wliafe"
release = config["project"]["version"]
```

添加Sphinx插件。

```python conf.py
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "zh_CN"
```

设置html主题。

```python conf.py
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
```

#### 编写index.rst文件

在`.. toctree`下面列出自己编写的文档。

```rst index.rst
.. wliafe-mltools documentation master file, created by
   sphinx-quickstart on Fri Aug 22 14:27:37 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

欢迎查看 wliafe-mltools 文档
==========================================

.. toctree::
   :maxdepth: 1

   入门
   api
   历史版本

索引和表格
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

#### 自动生成API文档

使用`sphinx.ext.autodoc`和`sphinx.ext.napoleon`插件根据代码中的注释自动生成API文档。

在`conf.py`文件中添加插件。

编写`api.rst`文件，列出需要生成文档的模块。

```rst api.rst
API 文档
========

.. automodule:: mltools
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: mltools.learn.Epoch
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: mltools.utils.Timer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: mltools.utils.Recorder
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: mltools.draw.Animator
   :members:
   :undoc-members:
   :show-inheritance:
```

将`api.rst`添加到`index.rst`中。

#### 使用Markdown编写文档

使用Markdown编写文档，需要安装`myst_parser`插件。

```bash
uv add myst_parser
```

在`conf.py`文件中添加插件。

编写Markdown文件，将Markdown文件名添加到`index.rst`。

#### 本地构建项目

在项目根目录下执行以下命令，构建项目。

```bash
sphinx-build -M html docs/source docs/build
```

### sphinx_rtd_theme主题

#### 安装

```bash
uv add sphinx_rtd_theme
```

#### 配置

将主题作为插件添加到`conf.py`文件中。

将`conf.py`文件中的`html_theme`变量设置为`sphinx_rtd_theme`。

我使用的是主题的默认配置，如果想配置主题，参考[sphinx_rtd_theme](https://rtd.sphinx-doc.cn/en/stable/index.html)。

### Read the Docs

使用Github注册Read the Docs账号。

点击`Add project`，填写信息。

![Read the Docs控制面板](8.png)

在项目中添加`.readthedocs.yaml`文件用于Read the Docs构建项目。

```yaml .readthedocs.yaml
version: 2
build:
  os: ubuntu-24.04
  tools:
    python: '3.8'
sphinx:
  configuration: docs/source/conf.py
python:
  install:
  - requirements: docs/requirements.txt
  - requirements: requirements.txt
```

{% note info %}
`.readthedocs.yaml`配置文件的requirements选项只支持`requirements.txt`文件。
{% endnote %}
