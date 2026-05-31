---
title: Docker
date: 2022-05-16 21:08:55
categories:
    - 工具
tags:
---

Docker是一个开源的应用容器引擎，它可以让开发者打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的Linux机器上，也可以实现虚拟化。有关Docker的使用可以参考[Docker官方文档](https://docs.docker.com/)。在[Docker Hub](https://hub.docker.com/)上有很多Docker镜像，其中有官方镜像也有用户上传的镜像，用户可以根据需要下载使用。

本文介绍了我常用几个Docker容器，Docker Desktop for Windows软件，以及其它一些Docker用法。

<!--more-->

## Docker容器创建

Nginx容器创建

```bash
docker run --name <Nginx容器名称> -d -p 8080:80 nginx:stable-perl
```

{% note info %}
如果想让Docker容器随Docker启动而启动，就要在创建容器（docker run）时指定`--restart=always`参数。

```text
--restart=always
```

{% endnote %}

## Docker Desktop for Windows

Docker Desktop for Windows是微软推出的一个软件，它允许用户在Windows上运行Docker容器，而不需要安装虚拟机。Docker Desktop for Windows的docker引擎是跑在Linux环境中的，而Linux环境是WSL提供的，因此使用Docker Desktop for Windows时需要安装{% post_link "Windows Subsystem for Linux (WSL)" WSL %}。

这是[Docker Desktop for Windows的下载地址](https://www.docker.com/products/docker-desktop/)

## Docker本地和容器之间的文件传输

获取容器id全称

```bash
docker inspect -f '{{.id}}' <容器名称>
```

本地文件传输到容器

```bash
docker cp <本地文件路径> <ID全称>:<容器路径>
```

容器文件传输到本地

```bash
docker cp <ID全称>:<容器路径> <本地文件路径>
```

## Docker国内镜像

`/etc/docker/daemon.json`文件中添加以下内容：

```json daemon.json
{
    "registry-mirrors": [
        "https://docker.1ms.run",
        "https://docker.mybacc.com",
        "https://dytt.online",
        "https://lispy.org",
        "https://docker.xiaogenban1993.com",
        "https://docker.yomansunter.com",
        "https://aicarbon.xyz",
        "https://666860.xyz",
        "https://docker.zhai.cm",
        "https://a.ussh.net",
        "https://hub.littlediary.cn",
        "https://hub.rat.dev",
        "https://docker.m.daocloud.io"
    ]
}
```
