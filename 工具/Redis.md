---
title: Redis
date: 2022-09-14 20:30:07
categories:
    - 工具
tags:
---

Redis是一个开源的内存数据库，它是一个键值对数据库。

<!--more-->

## 安装Redis

```bash
apt install redis-server
```

## 配置Redis

修改配置文件`/etc/redis/redis.conf`

设置Redis端口，Redis默认端口为6379，可根据需要修改

![Redis端口](1.png)

设置Redis密码，在配置文件中添加 requirepass Redis.123

![Redis密码](2.png)

设置Redis远程连接，注释掉 # bind 127.0.0.1

![Redis远程连接](3.png)

最后要重启Redis才能生效

## Docker创建Redis容器

```bash
docker run --name <Redis容器名称> -d -p 6379:6379 redis --requirepass <Redis密码>
```
