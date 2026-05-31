---
title: C
date: 2020-11-28 19:41:29
categories:
    - 语言
tags:
    - C
---

C语言是计算机的入门语言，下面是我的C语言学习心得。

<!--more-->

## 函数

### 创建并使用函数

一个函数的例子

```c
#include<stdio.h>
#define NAME "GIGATHINK, INC."
#define ADDRESS "101 Megabuck Plaza"
#define PLACE "Megapolis, CA 94904"
#define WIDTH 40

void starbar(void);//声明函数
                    //这个函数的作用是打印（*）这个符号
int main(void)
{
    starbar();//调用函数
    printf("%s\n",NAME);
    printf("%s\n",ADDRESS);
    printf("%s\n",PLACE);
    starbar();//调用函数
    
    return 0;
}

void starbar(void)
{
    int count;
    
    for(count=1;count<=WIDTH;count++)
        putchar('*');
        putchar('\n');
}
```

运行结果

![1](1.png)

### 函数的结构

实际参数  函数名（形式参数）

void starbar(void)

int main(void)也是一个函数，他是主函数。

C语言程序先读取主函数，其他函数在主函数中被调用。

#### 实际参数（实参）

实参代表的是函数的返回值类型。

对于主函数main来说，通常返回值为int类型。

```c
#include<stdio.h>
int main(void)
{
    ...
    
    return 0;
}
```

也就是最后的`return 0;`0为int类型。

对于上文的starbar函数来说，返回值是void类型，也就是没有返回值。

```c
void starbar(void)
{
    ...
}
```

当然你可以返回double类型，char类型，指针类型等。

使用返回值

```c
#include<stdio.h>
int fanhui(void);
int main(void)
{
    ...
    n=fanhui();//返回的a的值给了n
    return 0;
}
int fanhui(void)
{
    ...
    return a;//这里的a必须是int类型
}
```

#### 形式参数（形参）

形参的作用是传递数据到函数中。

对于主函数来说，形参是void（当然main的形参可以不是void，他有自己的形参，具体我也不清楚，所以在此不做讨论）。

对于上文的starbar函数来说，形参是void，所以他不从主函数中传递参数。

使用形参

```c
#include<stdio.h>
int xingcan(int m,double n,char b...int*d);//可以有一个，也可以传递多个
int main(void)
{
    int i;
    double j;
    char c;
    ...
    int*a；
    
    ...
    n=int xingcan(i,j,c...a);//括号里的变量的类型要与形参定义的类型一一对应。
    return 0;
}
int xingcan(int m,double n,char b...int*d)
{
//在这个函数中m的值与原函数的i相等，n的值与原函数的j相等，以此类推。
//以后学了C语言的存储类别，存储管理就会知道
//在这个函数中对m，n，b...的操作不会影响主函数中i，j，b...的值。
//但指针例外，因为指针传递的是一个地址，在函数中操作地址所指向的值（即*d）
//就会改变主函数中传送的*a的值，因为*a和*d指向同一个地址。
    ...
    return a;//这里的a必须是int类型
}
```

### 字符串和字符串函数

字符串与字符串函数都必须在<string.h>头文件下使用。

#### 字符串输入

gets( )函数：

他读取整行输入，直至遇到换行符，然后丢弃换行符，储存其余字符，并在这些字符的末尾添加一个空字符使其成为一个C字符串。

gets( )函数易产生漏洞，不建议使用

fgets( )函数：

+ fgets函数的第二个参数指明了读入字符的最大数量。如果该参数的值是n，那么fgets( )将读入n-1个字符，或者读到遇到的第一个换行符为止。
+ 如果fgets( )读到一个换行符，会把它储存在字符串中。
+ fgets( )函数的第三个参数指明要读入从键盘输入的数据，则以stdin（标准输入）作为参数，该标识符定义在<stdio.h>中。
+ 由于fgets( )储存换行符，所以fgets( )必须和fputs( )配套使用。

gets_s( )函数：

+ gets_s( )只从标准输入中读取数据，所以不需要第三个参数。
+ 如果gets_s( )读到换行符，会丢弃它而不是储存它。
+ 如果gets_s( )读到最大字符数都没读到换行符。会将所读到的字符全部舍弃。

s_gets( )函数：

他是fgets( )完善。他将fgets( )最后保存的换行符改为C语言字符串末尾的"\0"

s_gets( )函数的用法

```c
char * s_gets(char*st,int n)
{
    char * ret_val;
    int i = 0;

    ret_val=fgets(st,n,stdin);
    if(ret_val);
    {
        while (st[i]!='\n'&&st[i]!='\0')
            i++;
        if (st[i]=='\n')
            st[i]='\0';
        else
            while (getchar()!='\n')
                continue;
    }
    return ret_val;
}
```

最常见的scanf函数就不再介绍了。

#### 字符串函数

strlen( )函数：用于统计字符串的长度。

```c
void fit(char *string,unsigned int size)
{
    if(strlen(string)>size)
        string[size]='\0';
}
```

strcat( )函数：用于拼接字符串。

```c
#include<stdio.h>
#include<string.h>
int main(void)
{
    char flower[30] = "wonderflower";
    char addon[] = "s smell like old shoes";
    puts("What is your favorite flower?");
    strcat(flower, addon);
    puts(flower);
    puts(addon);
    return 0;
}
```

strncat( )函数：可以指定添加字符串个数的strcat( )函数。

```c
strncat(flower,addon,23);
```

strcmp( )函数：将所给字符串与已储存的字符串作比较。

```c
#include<stdio.h>
#include<string.h>
#define ANSWER "Great"
int main(void)
{
    char try[40]="";//改为输入可以与ANSWER比较 
    puts("Who is burnied in Grant's tomb?");
    if(strcmp(try,ANSWER)!=0)
    ......
}
```

strncmp( )函数：可以指定比较字符串个数的strcmp( )函数。

```c
strcmp(try,ANSWER，5);
```

strcpy( )函数：将一个字符串数组复制到另一个字符串数组的函数。

```c
#include<stdio.h>
#include<string.h>
int main(void)
{
    char flower[25];
    char addon[] = "s smell like old shoes";
    strcpy(flower, addon);
    puts(flower);
    puts(addon);
    return 0; 
}
```

运行结果

```text
s smell like old shoes
s smell like old shoes
```

strncpy( )函数：可以指定复制字符串个数的strcpy( )函数。

```c
strcpy(flower,addon,23);
```

### 文件输入输出函数

+ getc( ):从文件中获取一个字符。
+ putc( ):向文件中输入一个字符。

```c
ch=getc(fp)
putc(ch,fp)
```

+ fopen( ):打开一个文件。
+ fclose( ):关闭一个文件。

```c
fp=fopen("wordy","a+")
fclose(fp)
```

+ fscanf( ):输入内容到变量中。
+ fprintf( ):输出内容到文件或显示器。

```c
char input[40];
fscanf(fp,"%s",input);
fprintf(fp,"%s",input);
```

+ fgets( ):从文件中获取（）个字符
+ fputs( ):将字符串保存到文件中（他在字符串末尾不会打印换行符）。

```c
#define STLEN 40
FILE *fp;
char buf[40];
fgets(buf,STLEN,fp);
fputs(buf,fp);
```

+ fseek( ):将指针指向文件某一位置。
  + SEEK_SET 文件开始处
  + SEEK_CUR 当前位置
  + SEEK_END 文件末尾
  + 0L 0字节  1L 1字节 以此类推
  + 正常 返回值为0 错误 返回值为-1（例如试图超出文件范围）
+ ftell( ):判断文件指针的当前位置。
  + 只适用于以二进制（rb）打开的文件

```c
fseek(fp,0l,SEEK_END);
ftell(fp);
```

## 结构体

### 示例

```c
#include<stdio.h>
#include<string.h>
char* s_gets(char* st, int n);
#define MAXTITL 41
#define MAXAUTL 31

struct book {
    char title[MAXTITL];
    char author[MAXAUTL];
    float value;
};

int main(void)
{
    struct book library;

    printf("Please enter the book title.\n");
    s_gets(library.title, MAXAUTL);
    printf("Now enter the author.\n");
    s_gets(library.author, MAXAUTL);
    printf("Now enter the value.\n");
    scanf("%f", &library.value);
    printf("%s by %s:$%.2f\n", library.author, library.title, library.value);
    printf("Done.\n");

    return 0;
}

char* s_gets(char* st, int n)
{
    char* ret_val;
    char* find;

    ret_val = fgets(st, n, stdin);
    if (ret_val)
    {
        find = strchr(st, '\n');
        if (find)
            *find = '\0';
        else
            while (getchar() != '\n')
                continue;
    }
    return ret_val;
}
```

### 声明

使用结构体标记声明：适用于需多次使用结构体的情况。

```c
struct book {
    char title[MAXTITL];
    char author[MAXAUTL];
    float value;
};
```

不使用结构体标记，直接声明并定义结构体变量：适用于只使用一次的结构体。

```c
struct {
    char title[MAXTITL];
    char author[MAXAUTL];
    float value;
}library;
```

### 初始化

分别初始化结构体成员

```c
library.title="Chicken of the Andes";
library.author="Disma Lapoult";
library.value=29.99;
```

集中初始化结构体成员

```c
struct book library={
    "Chicken of the Andes",
    "Disma Lapoult",
    29.99
};
```

## Linux I/O

### IO简介

本章所关注的是磁盘文件的I/O操作。然而，鉴于可以采用相同的系统调用对诸如管道、终端等所有类型的文件施以输入/输出操作，故而本章的大部分内容会与后续章节有关。

### 文件描述符

所有IO操作的系统调用都以文件描述符（一个非负整数）指代打开的文件。

|文件描述符|用途|
|:-----:|:----:|
|0|标准输入|
|1|标准输出|
|2|标准错误|

在程序中，可以用0、1、2来表示，或者采用<unistd.h>中定义的POSIX标准名称。

IO操作的4个系统调用：

+ `fd = open(pathname, flags, mode)` 函数打开pathname所标识的文件，并返回文件描述符，用以在后续函数调用中指代打开的文件。如果文件不存在，open()函数可以创建之，这取决于对位掩码参数flags的设置。flags参数还可指定文件的打开方式：只读、只写亦或是读写方式。mode参数则指定了由open()调用创建文件的访问权限，如果open()函数并未创建文件，那么可以忽略或省略mode参数。
+ `numread = read(fd, buffer, count)` 调用从fd所指代的打开文件中读取至多count字节的数据，并存储到buffer中。read()调用的返回值为实际读取到的字节数。如果再无字节可读（例如：读到文件结尾符 EOF 时），则返回值为 0。
+ `numwritten = write(fd, buffer, count)` 调用从buffer中读取多达count字节的数据写入由fd所指代的已打开文件中。write()调用的返回值为实际写入文件中的字节数，且有可能小于count。
+ `status = close(fd)` 在所有输入/输出操作完成后，调用close()，释放文件描述符fd以及与之相关的内核资源。

Linux通用IO

open()、read()、write()、close()

### 打开一个文件：open()

```cpp
#include<fcntl.h>
int open(const char *pathname,int flags, mode_t mode);
```

读取成功返回文件描述符。

文件读取失败，返回-1

参数表：

![open函数参数表1](2.png)

![open函数参数表2](3.png)

在open函数含有O_CREAT时，即需要创建文件时，就要添加mode参数注明文件的读取权限。

### 读取一个文件：read()

```cpp
#include<united.h>
ssize_t read(int fd,void *buffer, size_t count);
//成功返回实际读取字节个数
//失败返回0
```

### 数据写入文件：write()

```cpp
#include<unistd.h>
ssize_t write(int fd, void *buffer,size_t count);
//成功返回实际写入文件的字节数>=0
//如果返回0，若errno被设定，则出错，否则写入0
//返回-1，调用失败查看errno判断错误
```

### 关闭文件：close()

```cpp
#include<unistd.h>
int close(int fd);
```

### 改变文件偏移量：lseek()

```cpp
#include<unistd.h>
off_t lseek(int fd,off_t offset, int whence);
//返回文件的偏移量
```

### 通用IO模型以外的操作：ioctl()

```cpp
#include<sys/ioctl.h>
int ioctl(int fd,int request, ...)
```

### 原子操作和竞争条件

原子操作是指，某些系统调用中的所有步骤会作为独立操作而一次行加以执行，其间不会为其他进程或线程所中断。

在open函数中使用O_EXCL标志可以使打开文件成为原子操作。

### 文件控制操作：fcntl()

```cpp
#include<fcntl.h>
int fcntl(int fd, int cmd, ...);
//函数调用成功返回cmd的对应值。
//函数调用失败返回-1。
```

### 打开文件状态标志

```cpp
int flags,accessMode;
flags = fcntl(fd,F_GETFL);
if(flags == -1)
    errExit("fcntl");
```

### 文件描述符和打开文件之间的关系

多个文件描述符可以指向同一打开的文件。

内核维护的三个数据结构：

+ 进程级的文件描述符表
+ 系统级的打开文件表
+ 文件系统的i-node表

文件描述符表：

+ 控制文件描述符操作的一组标志。
+ 对打开文件句柄的引用

打开文件表：

+ 当前文件的偏移量
+ 打开文件时所使用的状态标志
+ 文件访问模式
+ 与信号驱动I/O相关的设置
+ 对该文件i-node对象的引用

i-node表：

+ 文件类型
+ 一个指针，指向该文件所持有的锁的列表
+ 文件的各种属性，包括文件的大小以及与不同类型操作相关的时间戳。

### 复制文件描述符

复制文件描述符：dup()

```cpp
#include<unistd.h>
int dup(int oldfd);
//调用成功,返回新的文件描述符标志
//调用失败,返回-1
```

复制文件描述符：dup2()

```cpp
#include<unistd.h>
int dup2(int oldfd, int newfd);
//调用成功，返回新的文件描述符，与newfd相同
//调用失败，返回-1
```

若调用dup2()时，oldfd已经打开，需要调用close()将其关闭

复制文件描述符：dup3()

```cpp
#define _GNU_SOURCE
#include<unistd.h>
int dup3(int oldfd, int newfd, int flags);
//调用成功，返回文件描述符
//调用失败，返回-1
```

flags用于修改系统调用行为

### 在文件特定偏移量处的I/O：pread()和pwrite()

```cpp
#include<unistd.h>
ssize_t pread(int fd, void *buf, size_t count, off_t offset);
//文件描述符、变量、读取数、偏移量。
//调用成功返回读取的字节数
//调用失败返回-1
ssize_t pwrite(int fd, const void *buf, size_t count, off_t offset);
//调用成功返回写的字节数
//调用失败返回-1
```

### 分散输入和集中输出：readv()和writev()

```cpp
#include<sys/uio.h>
sturct iovec{
    void *iov_base;//起始地址
    size_t iov_len;//读取的字节数
}
ssize_t readv(int fd, const struct iovec *iov, int iovcnt);
//文件描述符、iov结构数组、iov个数
//调用成功返回读取的字节数
//调用失败返回-1
ssize_t writev(int fd, const struct iovec *iov, int iovcnt);
//调用成功返回实际写入数量
//调用失败返回-1
```

### 截断文件：truncate()和ftruncate()系统调用

作用：将文件大小设置为length参数指定的值

```cpp
#include<unistd.h>
int truncate(const char *pathname, off_t length);
int ftruncate(int fd, off_t length);
//调用成功返回0
//调用失败返回-1
```

### /dev/fd 目录

每个进程，内核都提供这个目录，这个文件目录里存储了该进程的文件描述符。

## Linux进程

### 进程号和父进程号

每个进程都有一个进程号(PID)，进程号是一个正数，标识进程。

返回该进程进程号：getpid()函数

```c
#include<unistd.h>
pid_t getpid(void);
//调用成功返回PID
```

返回该进程的父进程号：getppid()函数

```c
#include<unistd.h>
pid_t getppid(void);
//调用成功返回PID
```
