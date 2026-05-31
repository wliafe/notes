---
title: GitHub
date: 2025-07-31 21:20:19
categories:
    - 工具
tags:
---

GitHub是一个基于Git的版本控制平台，用于托管和协作开发项目。

<!--more-->

## 我的仓库管理体系

先简单介绍一下我的仓库管理办法，由于墙的缘故，GitHub时不时无法访问，而我并不希望我的代码管理依赖于代理软件是否好用，因此有了现在的仓库管理体系，简单的说就是利用Gitee的仓库镜像管理功能，将国内的Gitee仓库作为GitHub的加速器，让本地项目直接上传到Gitee，让Gitee帮忙上传到GitHub，这样除了在配置仓库时需要代理软件访问GitHub，在项目开发中就不需要了。

### Gitee仓库创建

当创建一个新项目时，我会在国内的Gitee仓库建立项目，这并不需要代理软件。

![Gitee仓库创建](1.png)

填写仓库信息，根据情况选择开源或私有（对Gitee来说无所谓，反正没人看，但选择私有可能会少些麻烦），我一般也会选择初始化仓库，添加`.gitignore`文件，添加开源协议（开源协议可以根据自己的喜好选），README文件我也会加上，项目写到后期总要介绍的，哪怕只是给未来的自己看。

![Gitee新建仓库信息填写](2.png)

填写完成后，点击创建即可，创建好的仓库是这样的。

![Gitee仓库截图](3.png)

之后就是像前文提到的获取仓库http地址，将仓库地址克隆到本地了。

到这一步，全程没有使用代理软件，我的项目开发也可以步入正轨了，但当我想将项目放到GitHub上时，就需要进行下面的操作，运气好的话可能也不需要代理软件。

### Gitee联动GitHub

打开新建好的仓库，点击管理，选择仓库镜像管理，点击添加镜像。

![Gitee镜像仓库管理](4.png)

#### GitHub导入Gitee仓库

保持页面打开，然后打开GitHub，选择导入仓库。

![GitHub导入仓库](5.png)

填写Gitee仓库信息，最后点击导入。

![GitHub导入仓库填写信息](6.png)

#### 获取GitHub私人令牌

打开GitHub个人设置。

![打开GitHub个人设置](7.png)

选择开发者设置。

![GitHub私人令牌](8.png)

点击创建新令牌。

![创建新令牌](9.png)

填写令牌名（我的习惯是Gitee<仓库名>Mirror），过期时间选择无期限，勾选`repo`，然后点击生成令牌。

![填写令牌信息](10.png)

#### Gitee添加镜像

将生成的令牌复制下来，粘贴到Gitee添加镜像页面私人令牌中，然后在镜像仓库列表里选择我们在GitHub新导入的Gitee仓库，最后点击添加。

![Gitee添加镜像](11.png)

每当Gitee代码仓库更新时，他就会自动同步到GitHub仓库，当然，你也可以通过下图界面手动同步。

![Gitee仓库代码同步](12.png)

## GitHub Actions

GitHub Actions是一个持续集成和持续交付（CI/CD）平台，用于自动化构建、测试和部署软件项目。学会使用GitHub Actions可以帮助你更高效地管理项目，提高项目的质量。对我来说，使用GitHub Actions可以帮我自动发布博客，还可以帮我自动发布pip库。

### 创建Actions

在GitHub项目中添加文件`.github/workflows`，在该目录下添加文件`<main>.yml`文件，然后上传到GitHub就可以了。

## Webhooks

`Github项目->Settings->Webhooks`中包含项目更新时需要同步发送的信息选项，Gitee的仓库同步，Read the Docs的文档更新都通过Webhooks进行。

![Webhooks](13.png)

点击`Edit`可以编辑Webhooks的触发条件，可以修改Gitee的同步触发方式，或者降低Read the Docs文档的更新频率。

## Github徽标

使用[Shield.io](https://shields.io/)可以轻松创建GitHub徽标，徽标可以显示项目的状态，比如是否通过了测试，是否发布了新的版本，是否有新的问题等。
