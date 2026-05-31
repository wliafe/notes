---
title: Assembly
date: 2020-12-10 20:09:31
categories:
    - 语言
tags:
    - Assembly
---

汇编语言（Assembly Language）是一种低级程序设计语言，它使用助记符来代替机器语言的二进制代码，是机器语言与高级语言之间的桥梁。

<!--more-->

## 基础知识

### 汇编语言的组成

汇编语言有3类指令组成。

+ 汇编指令：机器码的助记符，有对应的机器码。
+ 伪指令：没有对应的机器码，由编译器执行，计算机并不执行。
+ 其他符号：如+、-、*、/等，由编译器识别，没有对应的机器码。

### CPU对存储器的读写

cpu需对外部器件进行下面3类信息交互。

+ 存储单元的地址（地址信息）
+ 器件的选择，读或写的命令（控制信息）
+ 读或写的数据（数据信息）

### 各类存储器芯片

随机存储器（RAM）：可读可写，必须带点存储，断电内容丢失。

只读存储器（ROM）：只读不写。

![1](1.png)

### 内存地址空间

这里以8086PC机内存地址空间分配为例

![2](2.png)

这幅图意思是从地址0 9FFFF的内存单元中读取数据，实际上是读取主随机存储器中的数据；向地址A0000 BFFFF的内存单元中写数据，就是向显存中写数据，这些数据会被显卡输出到显示器上；我们向地址C0000 BFFFF的内存单元中写数据的操作是无效的，因为这等于改写只读存储器中的内容。

### 8086CPU物理地址

物理地址=段地址*16+偏移地址

基础地址=段地址*16

物理地址=基础地址+偏移地址

8086CPU读取信息位置=CS*16+IP

### 栈

关于栈的特性没有比这个更形象了。

![3](3.png)

![4](4.png)

栈是人为定义的，不是CPU自然存在的内存，我们可以通过定义SS、SP的值来定义栈的范围。

#### CPU关于栈的机制

入栈命令：push ax（将ax表示的数据送入栈中）

出栈命令：pop ax（将栈顶的数据送入ax中）

CPU中SS、SP提供栈的机制:

+ SS:SS是段寄存器，他提供栈的段地址。
+ SP:SP是寄存器，提供栈的偏移地址。
+ SS:SP始终指向栈顶元素。

#### 栈顶超界

![5](5.png)

![6](6.png)

![7](7.png)

栈顶超界是很危险的，他会毁坏其他数据，因此在编程是要小心，不要超出栈的范围。

### 寻址方式

+ [data]
+ [bx]
+ [bx+data] 类似一维数组
+ [bx+si]
+ [bx+si+data] 类似二维数组

### 数据长度

在有寄存器名字时，看寄存器名字。

在没有寄存起名字时 用word ptr表示字(16位)单元，用byte ptr表示字节(8位)单元。

push pop只进行字操作。

## 寄存器

### 各个寄存器

**cs:ip**:决定cpu读取命令物理地址。

**ss:sp**:始终指向栈顶，决定栈的机制。

**ds**：决定cpu读取数据的基础地址。

**loop cx**：loop命令循环次数取决于cx。

**dx**：可作为累加寄存器。

**es**：附加寄存器。

### 通用寄存器

8086CPU寄存器是16位的，可以存放两个字节。

+ 通用寄存器（存放一般数据）：AX、BX、CX、DX。
  + AX分为AH和AL（AH和AL都是八位,AH为高位字节，AL为低位字节）其余通用寄存器以此类推。
+ 段寄存器（提供段地址）：CS、DS、SS、ES
+ 寄存器（提供偏移地址）：IP、SP、BP
+ 与bx作用类似：SI、DI
+ 标志寄存器：PSW

#### bx si di bp

他们可以通过[ ]表示数据。

他们可以单独出现或以 bx si，bx di，bp si，bp di这四种组合出现。

bx默认的段地址是ds。

bp默认的段地址是ss。

### DS和[address]

用mov将内存单元中的内容送入寄存器中。

格式：mov 寄存器名，内存单元地址。例：mov ax,[0]

[0]表示的是偏移地址，而段地址是DS的值。

同理可以将寄存器中的值送到内存单元中

#### 补充：改变DS值的方法

```asm
mov bx,1000H
mov ds,bx
```

这两条指令运行后，ds的值就改为1000H了。

### [bx]

[bx]：表示的是ds:bx所表示位置的数据

### SI 和 DI

与bx作用类似。

### 标志寄存器

他就是flag，他储存的信息被称为程序状态字(PSW)。

![8](8.png)

#### 标志

ZF标志：零标志位，记录相关指令执行后结果是否为零，结果是零zf=1，不是零zf=0

PF标志：奇偶标志位，记录相关指令执行后结果中1的个数是否为偶数，1的个数为偶数pf=1，为奇数pf=0

SF标志：符号标志位，记录相关指令执行后结果是否为负，结果为负sf=1，非负sf=0

CF标志：进位标志位，（无符号数运算）记录运算结果的最高有效位向更高位的进位值，或借位值。

OF标志：溢出标志位，记录（有符号数）运算的结果是否发生溢出，如果发生溢出of=1，没有溢出of=0

DF标志：方向标志位，在串处理指令中，控制si，di增减。df=0 每次操作后si di递增，df=1 每次操作后si di递减

#### 标志存储器Debug中表示

![9](9.png)

## 指令

### mov指令

```asm
mov 寄存器，数据
mov 寄存器，寄存器
mov 寄存器，内存单元
mov 内存单元，寄存器
mov 段寄存器，寄存器
mov 寄存器，段寄存器
mov 内存单元，段寄存器
mov 段寄存器，内存单元
```

### add指令（加法）

```asm
add 寄存器，数据
add 寄存器，寄存器
add 寄存器，内存单元
add 内存单元，寄存器
```

### sub指令（减法）

```asm
sub 寄存器，数据
sub 寄存器，寄存器
sub 寄存器，内存单元
sub 内存单元，寄存器
```

### mul乘法指令

相乘的数为8位或16位

如果是8位，就放在 al 和 8位reg或内存字节单元中，结果放在ax中

如果是16位，就放在 ax 和 16位reg或内存字单元中，结果高位在dx中，低位在ax中。

格式：

```asm
mul reg/内存单元
```

### div除法指令

除数：8位或16位，放在reg或内存单元中。

被除数：除数8位则被除数16位，在ax中存放。除数16位则被除数32位，在ax和dx中存放，dx存放高16位，ax存放低16位。

结果：除数为8位，al存商，ah存余数。除数16位，ax存商，dx存余数。

格式：

```asm
div 除数
```

### and 指令

### or指令

### push指令

```asm
push 寄存器
push 段寄存器
push 内存单元
```

### pop指令

```asm
pop 寄存器
pop段寄存器
pop内存单元
```

### loop指令

loop：是循环的意思

loop的循环次数取决与cx的值，每循环一次cx的值减一，直到减到零为止。

在debug中用p命令可以快速完成循环

#### loop程序

```asm
assume cs:code
code segment
    mov cx,11

    mov ax,2
 s: add ax,ax
    loop s

    mov ax,4c00h
    int 21h
code ends
end
```

### jmp指令

mov ax,123可以改变ax的值，同理可以改变bx,cx,dx的值，但是mov不可以改变CS、IP的值，因此用jmp命令改变CS、IP的值。

```asm
jmp 段地址:偏移地址
```

例一：

```asm
jmp 2AE3:3  ;执行后：CS=2AE3H,IP=0003H
```

例二：

```asm
;指令执行前：ax=1000H，CS=2000H，IP=0003H
jmp ax
;指令执行后：ax=1000H，CS=2000H，IP=1000H
```

段内近转移：-32768~32767

```asm
jmp near ptr 标号
```

段间转移，远转移

```asm
jmp far ptr 标号
```

目的地址在寄存器中

```asm
jmp reg
```

目的地址在数据中

```asm
jmp word ptr    ;数据地址（只取一个字，改变ip）
jmp dword ptr   ;数据地址（取两个字，高地址是cs，低地址是ip）
```

### jcxz指令

有条件的转移指令，属于段内短转移

格式：

```asm
jcxz 标号
```

在cx是0的前提条件下才会执行这条指令

### call指令

#### 目的地址在指令中

段内近转移

格式：

```asm
call 标号
```

效果：

```asm
push ip
jmp near ptr 标号
```

段间转移

格式：

```asm
call far ptr 标号
```

效果：

```asm
push cs
push ip
jmp far ptr 标号
```

#### 目的地址在寄存器中

格式：

```asm
call 16位reg
```

效果：

```asm
push ip
jmp 16位reg
```

#### 目的地址在内存中

格式：

```asm
call word ptr 内存单元地址
```

效果：

```asm
push ip
jmp word ptr 内存单元地址
```

格式：

```asm
call dword ptr 内存单元地址
```

效果：

```asm
push cs
push ip
```

格式：

```asm
jmp dword ptr 内存单元地址
```

### ret指令

作用：修改ip的内容，实现近转移

格式：

```asm
ret
```

效果：

```asm
pop ip
```

### retf指令

作用：修改cs 和 ip 的内容，实现段转移

格式：

```asm
retf
```

效果：

```asm
pop ip
pop cs
```

### adc指令

带进位加法指令，利用cf位。

格式：

```asm
adc 操作对象1，操作对象2
```

功能：操作对象1=操作对象1+操作对象2+cf

### sbb指令

带借位减法指令，利用cf位

格式：

```asm
sbb 操作对象1，操作对象2
```

功能：操作对象1=操作对象1-操作对象2-cf

### cmp指令

比较指令

格式：

```asm
cmp 操作对象1，操作对象2
```

功能：计算操作对象1-操作对象2 不保存结果

通过标志来判断比较结果

![10](10.png)

### 条件转移指令

格式：指令 标号

|指令|条件|
|:--|:--|
|je|zf=1|
|jne|zf=0|
|jb|cf=1|
|jnb|cf=0|
|ja|cf=0 且 zf=0|
|jna|cf=1 或 zf=1|

### 串传送指令

#### movsb

传送字节

格式：

```asm
movsb
```

功能：将ds：si指向的内存单元的字节送入es：di中，然后根据df的值，将si di递增或递减。

#### movsw

传送字

格式：

```asm
movsw
```

功能：将ds：si指向的内存单元的字节送入es：di中，然后根据df的值，将si di递增2或递减2。

### rep指令

循环指令

格式：

```asm
rep ...
```

功能：循环执行后面的指令，循环次数取决于cx

### cld指令

使df=0

格式：

```asm
cld
```

### std指令

使df=1

格式：

```asm
std
```

### pushf指令

将标志存储器数据压栈。

格式：

```asm
pushf
```

### popf指令

将栈中数据存入标志存储器。

格式：

```asm
popf
```

### 端口读写指令

#### in指令

从端口读入数据

格式：

```asm
in al,60h   ;从60h端口读入一个字节。
```

#### out指令

向端口写入数据

格式：

```asm
out al,60h  ;向60h端口写入一个字节。
```

在in和out指令中只能用ax和al从端口读入或向端口写入数据。

对0~255以内的端口读写时，直接写端口

对256~65535的端口进行读写时，端口放在dx中

CMOS RAM：自带电源，记录时间。

### shl指令

shl 是逻辑左移指令

将寄存器或内存单元中的数据向左移位

将最后移出的一位写入CF中

最低位用0补充

左移位数大于1则将移动位数存在cl中

### shr指令

shr 是逻辑右移指令，他和shl作用相反

## 汇编程序

### dosbox汇编命令

+ R：查看、改变CPU寄存器的内容。
+ D：查看内存中的内容。
+ E：改写内存中的内容。
+ U：将内存中的机器指令翻译成汇编指令。
+ T：执行一条机器指令。
+ A：以汇编指令的格式在内存中写入一条机器指令。

D命令

```asm
d 段地址(ds):偏移地址
```

### 汇编程序基本结构

例：

```asm
assume cs:codesg
codesg segment
    mov ax,0123h
    mov bx,0456h
    add ax,bx
    add ax,ax

    mov ax,4c00h
    int 21h
codesg ends
end
```

### 伪指令

例中有三种伪指令。

1. 他表示一个段开始，和段结束。
2. end：他是汇编程序结束的标记。
3. assume：这句含义是“假设”。用assume将有特定用途的段和相关的的段寄存器关联起来。
4. 程序返回：int 21h是程序返回。将程序返回到主程序。

```asm
XXX segment

...

XXX ends
```

### 运行一个程序

用edit命令打开文本编辑，编辑程序。

![11](11.png)

编辑程序并保存为asm文件，取名为t1。

![12](12.png)

用masm t1；命令编译为obj文件。

![13](13.png)

用link t1；命令编译为exe文件。

![14](14.png)

用debug t1.exe；命令来运行程序。

![15](15.png)

![16](16.png)

最后int 要用p命令来运行。

![17](17.png)

### dw伪指令

```asm
dw 0123h, 0456h,0789h,0abch,0defh,0fedh,0cbah,0987h
```

例一：从cs:0开始存储后面的数据

```asm
assume cs:code
code segment

    dw 0123h,0456h,0789h,0abch,0defh,θfedh,0cbah,0987h

start:  mou bx,0
        mou ax,0

        mou cx,8
    s:  add ax,cs:[bx]
        add bx,2
        loop s
    
        mov ax,4c00h
        int 21h
code ends
end start
```

start和end start 共同决定程序的开始位置，跳过dw命令。

例二：将数据逆序存放在段代码中使用栈

```asm
assume cs:codesg
codesg segment

    dw 0123h,0456h,0789h,0abch,0defh,θfedh,0cbah,0987h
    dw 0,0,0,0,0,0,0,0

start:  mov ax,cs
        mov ss,ax
        mov sp,30h

        mov bx,0
        mov cx,8
    s:  push cs:[bx]
        add bx,2
        loop s

        mov bx,0
        mov cx,8
   s0:  pop cs:[bx]
        add bx,2
        loop s0
        
        mov ax,4c00h
        int 21h
codesg ends
end start
```

### 多段程序

可以通过多段程序将数据段地址（ds），栈的段地址（ss）确定下来，方便调用。

```asm
assume cs:code,ds:data,ss:stack

data segment
    dw 0123h,0456h,0789h,0abch,0defh,θfedh,0cbah,0987h
data ends

stack segment
    dw 0,0,0,0,0,0,0,0
stack ends

code segment
start:  mov ax,stack
        mov ss,ax
        mov sp,16

        mov ax,data
        mov ds,ax

        push ds:[0]
        push ds:[2]
        pop ds:[2]
        pop ds:[0]

        mov ax,4c00h
        int 21h
code ends
end start
```

### db伪指令

将abcd转化为ascii码，从cs:0开始写入。

```asm
db 'abcd'
```

例：将一段字符转化为小写，另一段字符转化为大写

```asm
assume cs:codesg,ds:datasg

datasg segment
    db'BaSiC'
    db'iNfOrMaTiOn'
datasg ends

codesg segment
start:  mov ax,datasg
        mov ds,ax
        mov bx,0
        mov cx,5

    s:  mou al,[bx]
        and al,11011111B
        mov [bx],al
        inc bx
        loop s

        mov bx,5
        mov cx,11

   s0:  mov al,[bx]
        or al,00100000B
        mov [bx],al
        inc bx
        loop s0

        mou ax,4c00h
        int 21h
codesg ends
end start
```

### 用内存保存段地址

```asm
assume cs:codesg,ds:datasg
datasg segment
    db 'ibm            '
    db 'dec            '
    db 'dos            '
    db 'uax            '
    dw 0
datasg ends

codesg segment
start:  mov ax,datasg
        mov ds,ax
        mov bx,0
        
        mov cx,4
   s0:  mov ds:[40h],cx
        mov si,θ
        mov cx,3

    s:  mov al,[bx+si]
        and al,11011111b
        mov [bx+si],al
        inc si
        loop s

        add bx,16
        mov cx,ds:[40h]
        loop s0
        
        mov ax,4c00h
        int 21h
codesg ends
end start
```

{% note info %}
还可用栈来保存段地址
{% endnote %}

### dd伪指令

dd命令：定义双字节数据。

```asm
dd 1
```

### dup操作符

```asm
db/dw/dd 重复次数 dup (重复的数据)
```

### offset操作符

获取编译器处理符号的偏移地址。

```asm
assume cs:codesg
codesg segment
start:  mov ax, offset start    ;相当于mov ax,0
    s:  mov ax,offset s         ;相当于mov ax,3
codesg ends
end start
```
