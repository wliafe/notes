---
title: Redis
aliases: []
type: note
created: 2022-09-14
area: Developer Tools
status: active
review: pending
tags: []
---
> [!info] 导航
> [[40-Knowledge/Developer Tools/Developer Tools|返回工具索引]]

Redis是一个开源的内存数据库，它是一个键值对数据库。



## 安装Redis

```bash
apt install redis-server
```

## 配置Redis

修改配置文件`/etc/redis/redis.conf`

设置Redis端口，Redis默认端口为6379，可根据需要修改

![[99-Assets/Legacy/工具/Redis/1.png]]

设置Redis密码，在配置文件中添加 requirepass Redis.123

![[99-Assets/Legacy/工具/Redis/2.png]]

设置Redis远程连接，注释掉 # bind 127.0.0.1

![[99-Assets/Legacy/工具/Redis/3.png]]

最后要重启Redis才能生效

## Docker创建Redis容器

```bash
docker run --name <Redis容器名称> -d -p 6379:6379 redis --requirepass <Redis密码>
```
