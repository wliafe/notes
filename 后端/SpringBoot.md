---
title: SpringBoot
date: 2022-09-19 18:03:16
categories:
    - 后端
tags:
    - Java
---

SpringBoot是Spring的一个子项目，是为了简化Spring的配置而诞生的。

<!--more-->

## 第一个项目

### 项目创建

![1](1.png)

![2](2.png)

![3](3.png)

### 文件编写

```yml application.yml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.1.120:3306/Users
    username: root
    password: Mysql.123
```

```java User.java
public class User implements Serializable {
    private Integer id;
    private String name;
    private String password;

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", password='" + password + '\'' +
                '}';
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
```

```java UserMapper.java
@Mapper
public interface UserMapper {
    @Insert("insert into users(name,password) values(#{name},#{password})")
    void save(User user);

    @Delete("delete from users where id = #{id}")
    void delete(Integer id);

    @Update("update users set name= #{name},password= #{password} where id= #{id}")
    void update(User user);

    @Select("select * from users")
    List<User> findAll();

    @Select("select * from users where id = #{id}")
    User findById(Integer id);
}

```

```java UserService.java
public interface UserService {
    boolean save(User user);

    boolean update(User user);

    boolean delete(Integer id);

    User findById(Integer id);

    List<User> findAll();
}
```

```java UserServiceImpl.java
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserMapper userDao;

    public boolean save(User user) {
        userDao.save(user);
        return true;
    }

    public boolean update(User user) {
        userDao.update(user);
        return true;
    }

    public boolean delete(Integer id) {
        userDao.delete(id);
        return true;
    }

    public User findById(Integer id) {
        return userDao.findById(id);
    }

    public List<User> findAll() {
        return userDao.findAll();
    }
}
```

```java UserController.java
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    UserService userService;

    @PostMapping
    public boolean save(@RequestBody User user) {
        userService.save(user);
        return true;
    }

    @PutMapping
    public boolean update(@RequestBody User user) {
        userService.update(user);
        return true;
    }

    @DeleteMapping("/{id}")
    public boolean delete(@PathVariable Integer id) {
        userService.delete(id);
        return true;
    }

    @GetMapping("/{id}")
    public User findById(@PathVariable Integer id) {
        return userService.findById(id);
    }

    @GetMapping
    public List<User> findAll() {
        return userService.findAll();
    }
}
```

### 运行

![4](4.png)

![5](5.png)

## 多环境配置

开发SpringBoot应用的时候，通常程序需要在测试环境测试成功后才会上线到生产环境。而测试环境和生产环境的数据库地址、服务器端口等配置都不同。在为不同环境打jar包时，需要频繁的修改`application.yml`配置文件，十分麻烦。

可以采用创建多个配置文件的方法解决这一问题。

创建以下三个文件，配置不同环境的地址信息，存放在`application.yml`同一目录下：

+ application-dev.yml：本地开发环境
+ application-test.yml：测试环境
+ application-prod.yml：生产环境

![6](6.png)

其中`application.yml`存放公共配置，可通过修改active切换读取的配置文件，比如active: dev改成active: test就是将读取`application-dev.yml`改为`application-test.yml`，环境也从本地开发变成了测试环境。

```yml application-dev.yml
spring:
  profiles:
    active: dev
  application:
    name: data-transceivers #当前服务的名称
```

```yml application-test.yml
spring:
  kafka:
    bootstrap-servers: 10.10.5.70:6667,10.10.5.71:6667,10.10.5.72:6667 #测试环境地址
server:
  port: 8312
```

```yml application-prod.yml
spring:
  kafka:
    bootstrap-servers: 10.10.2.92:6667,10.10.2.93:6667,10.10.2.94:6667 #生产环境地址
server:
  port: 8312
```

## SpringBoot启动报错

### 报错内容

{% note danger %}

```text
java.lang.IllegalStateException: Failed to load property source from 'file:/D:/IDEA/spring-cloud/sp05-eureka/target/classes/application.yml' (classpath:/application.yml)

Caused by: org.yaml.snakeyaml.error.YAMLException: java.nio.charset.MalformedInputException: Input length = 1
```

{% endnote %}

### 错误原因

出现这个的原因，就是解析yml文件时，中文字符集不是utf-8的原因，

但是通过cmd命令，`mvn clean compile`后，项目又可以成功运行

找了很久问题，使用eclipse和IDEA同时测试，最终发现，是Maven在项目编译时，默认字符集编码是GBK

### 检查pom文件

我们首先需要在pom文件中设置，编译时编码utf-8即可，如果解决不了进行第二步

```xml pom.xml
<properties>
   <java.version>1.8</java.version>
    <spring-cloud.version>Hoxton.SR6</spring-cloud.version>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    <maven.compiler.encoding>UTF-8</maven.compiler.encoding>
</properties>
```

![7](7.png)

### 修改编码格式

![8](8.png)

![9](9.png)

然后重新启动项目！！！！

### 最不应该出现的错误

就是你的`application.yml`文件是通过把其他类型的文件后缀名直接改为yml生成的，这时就需要你把`application.yml`中的内容全部复制，然后删除，再新建一个`application.yml`文件，将复制的内容拷贝进去再运行项目就不会报错了。

### 总结

这个问题，在一般成熟的项目里面是不会出现的，他一般出现在新建的项目上面，因为一般新建的项目有些配置不够完善，这一块是需要注意的地方。
