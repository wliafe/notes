---
title: MySQL
date: 2022-04-03 10:32:18
categories:
    - 工具
tags:
---

MySQL是一个关系型数据库管理系统，是后端常用的数据库系统，MySQL是开源的，可以免费下载使用。

<!--more-->

## MySQL数据库安装

### MySQL安装、服务命令

安装MySQL服务器

```bash
apt install mysql-server
```

启动MySQL服务

```bash
systemctl start mysqld 
```

或

```bash
service mysql start
```

重启MySQL服务

```bash
service mysql restart
```

停止MySQL服务

```bash
service mysql stop
```

显示MySQL状态

```bash
service mysql status
```

设置MySQL服务开机自启动

```bash
service mysql enable
```

进入数据库

```bash
mysql [-h <主机ip>] -u root -p 
```

退出

```bash
exit
```

### 配置MySQL远程登录

修改`/etc/mysql/mysql.conf.d/mysqld.cnf`配置文件。

打开配置文件，找到`bind-address = 127.0.0.1`这一行，改为`bind-address = 0.0.0.0`即可或注释掉

修改完成保存后，需要重启MySQL服务才会生效

MySQL默认端口3306

### 配置MySQL

运行MySQL初始化安全脚本

```bash
mysql_secure_installation
```

#### 脚本报错

错误样例

{% note danger %}
... Failed! Error: SET PASSWORD has no significance for user 'root'@'localhost' as the authentication method used doesn't store authentication data in the MySQL server. Please consider using ALTER USER instead if you want to change authentication parameters.
{% endnote %}

更正方法

```sql
use mysql;
```

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'Mysql.123';
flush privileges;
```

## 常用SQL命令

展示所有数据库

```sql
show databases;
```

使用数据库

```sql
use <数据库名称>;
```

展示当前数据库所有表

```sql
shwo tables;
```

展示表结构

```sql
desc <表名称>;
```

## Docker创建MySQL容器

```bash
docker run --name <MySQL容器名称> -e MYSQL_ROOT_PASSWORD=<Mysql密码> -d -p 3306:3306 mysql
```

## MySQL数据库导入导出

### MySQL数据库导出数据和表结构

```bash
mysqldump -u <用户名> -p <密码> <数据库名> > <数据库名>.sql
```

### MySQL数据库导出表结构

```bash
mysqldump -u <用户名> -p <密码> -d <数据库名> > <数据库名>.sql
```

### MySQL数据库导入.sql文件

```bash
mysql -u <用户名> -p <密码> <数据库名> < <数据库名>.sql
```

数据库中命令方式导入

选择数据库

```sql
use <数据库名称>;
```

导入数据（注意sql文件的路径）

```sql
source <sql文件路径>;
```
