---
title: Node.js
date: 2025-07-04 21:04:26
categories:
    - 工具
tags:
    - JavaScript
---

Node.js是一个基于Chrome V8引擎的JavaScript运行环境，前端项目（Vue，React项目）和博客项目（Hexo项目）都是用JavaScript开发的，而Node.js就是这些项目运行的核心，它可以让JavaScript运行在服务器端，而不是浏览器端。通俗的讲，Node.js就像Java中的JVM，Python中的解释器，它们都是执行代码的工具。

<!-- more -->

## 安装

Node.js的安装比较简单，从[Node.js官网](https://nodejs.org/zh-cn)下载安装包，我选择的是Windows安装程序，一路下一步安装即可。

![nodejs安装包下载](1.png)

其中，这一步的选项Automatically install the necessary tools（自动安装所需工具）决定了是否安装用于编译原生模块的依赖项。这包括Python和Visual Studio Build Tools等工具，这些工具是否安装取决于个人需要，我没有选择安装。

![nodejs安装](2.png)

判断是否安装成功的办法当然是版本查看，打开命令行，输入下面命令，如果显示出版本号，说明安装成功。

```bash
node -v
```

## npm Node.js的包管理器

npm是Node.js的包管理器，用于安装、发布、管理和开发Node.js应用程序的工具。npm是随同Node.js一起安装的，所以当你下载并安装Node.js时，npm也会被自动安装。这里只简单介绍我比较关注的功能，更详细的功能讲解请参考[npm官方文档](https://docs.npmjs.com/)，中文文档请参考[npm中文文档](https://npm.nodejs.cn/)，有关npm命令的内容在[这里](https://npm.nodejs.cn/cli/v11/commands)。

### 安装包

npm安装包分为全局安装和局部安装，全局安装表明安装的包可以在任何目录下使用，而局部安装表明安装的包只能在当前目录下使用。我个人其实更推荐局部安装，局部安装可以实现环境隔离，避免不同项目环境的冲突，就像conda在python中的作用一样。

全局安装

```bash
npm install -g <package>
```

局部安装

```bash
npm install <package>
```

package.json局部安装

局部安装包列表在项目的`package.json`文件中就可查看，同时`package.json`文件也是项目的配置文件，记录项目的依赖关系，当项目迁移到其他机器时，只需要一条npm命令就可安装`package.json`文件中所有依赖。

```bash
npm install
```

### 卸载包

全局卸载

```bash
npm uninstall -g <package>
```

局部卸载

```bash
npm uninstall <package>
```

## npx Node.js的包执行器

npx是Node.js的包执行器，npx的执行逻辑很有意思，下面是他的执行顺序：

1. 检查当前目录局部安装的包，如果没有，执行下一步
2. 检查全局安装的包，如果没有，执行下一步
3. 从npm源中下载包到局部环境，回到第一步

因此npx特别适合执行项目创建命令，由于我最近在弄博客，就以hexo项目为例。

安装好Node.js后，选用taobao镜像源（加快下载速度），在自己创建的空文件下执行下面一条命令，即可创建一个hexo项目。

```bash
npx hexo init
```

npx执行hexo要比正常执行hexo命令多一个npx前缀，但这对我来说算是微不足道的小问题。

npx创建hexo项目的速度要比正常hexo创建项目的速度要慢一点，但在选用国内镜像源后，这一点问题也已解决。

已经创建好的hexo项目由于项目内部已安装hexo依赖包，所以项目内使用npx执行hexo命令不再受npm源网速影响。

综上所述，用npx创建项目是一个不错的方法，我个人也在使用中。

## nrm Node.js的镜像源管理器

nrm是Node.js的镜像源管理器，用于管理Node.js的镜像源，nrm可以切换npm源，也可以添加自定义源，这里是 [nrm 官方文档](https://github.com/Pana/nrm)。

在给npm换源时发现了nrm这个工具，给了我意外的惊喜，在给其他工具换源时，我需要查询源的网址，换源命令，有时还要修改配置文件，非常麻烦不说，还要担心源不稳定时切换回官方源的问题，有了这个工具，我不再需要手动修改npm源配置文件了，非常方便，强烈建议pip、conda也推出类似的工具。

当然nrm也可用npx执行，只是不那么方便罢了。

### nrm安装

作为源管理工具，我推荐全局安装

```bash
npm install -g nrm
```

### nrm常用命令

查看当前可用的源

```bash
nrm ls
```

切换源（建议选taobao）

```bash
nrm use <registry>
```

```bash
nrm use taobao
```

切换为官方源

```bash
nrm use npm
```

## package.json Node.js项目包管理文件

前面提到过，`package.json`文件中记录了项目的依赖关系，不止如此，`package.json`的scripts字段记录的脚本命令也很好用，scripts字段将项目的构建、运行、部署等脚本命令集中到一起，由npm run命令统一执行，不必每次都输入完整的命令，为用户提供了极大方便，这里还是以hexo项目为例。

scripts字段为

```json package.json
"scripts": {
    "build": "hexo generate",
    "clean": "hexo clean",
    "deploy": "hexo deploy",
    "server": "hexo server"
  },
```

这时，我们就可以使用npm run命令来执行scripts字段中的脚本命令了，比如：

执行构建命令

```bash
npm run build
```

执行部署命令

```bash
npm run deploy
```

执行运行命令

```bash
npm run server
```

利用好scripts字段，我们可以大大简化我们的操作。
