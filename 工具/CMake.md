---
title: CMake
date: 2022-03-16 07:56:42
categories:
    - 工具
tags:
    - Cpp
---

CMake是一个跨平台的C++构建工具，它可以根据平台不同生成不同的构建脚本。

<!--more-->

## CMake的简单使用

CMake的最简单粗暴的使用方法，仅限于Windows。

下载CMake软件后，创建文件夹作为一个项目。

在文件夹中新建`CMakeLists.txt`文件。

```text CMakeLists.txt
cmake_minimum_required(VERSION 3.5)#最低CMake版本

project (projectname)# 工程名

#添加源文件
aux_source_directory(${CMAKE_SOURCE_DIR} MAIN_FUNC_SRCS)#源文件目录(相对路径)


#添加.h文件
include_directories(${CMAKE_SOURCE_DIR})#.h文件目录(相对路径)


#指定生成目标
add_executable(${PROJECT_NAME} ${MAIN_FUNC_SRCS})
            生成的可执行文件名      所有的源文件
```

CMake命令

```bash
mkdir build
```

```bash
cd build
```

```bash
cmake ..
```

```bash
make
```

## 文件目录理想结构

```text
└── ttms
     ├── config
     │     └── config
     ├── src
     │    ├── include
     │    └── main.cpp
     └── CMakeLists.txt
```

## CMake较理想结构

```text CMakeLists.txt
cmake_minimum_required(VERSION 3.20.2)
project(SunProject)

set(CMAKE_CXX_STANDARD 14)

add_library(${PROJECT_NAME}-lib
        
        )

add_definitions(
       
)

target_include_directories(${PROJECT_NAME}-lib PUBLIC src)

add_executable(${PROJECT_NAME}-exe src/main.cpp)

target_link_libraries(${PROJECT_NAME}-exe PRIVATE ${PROJECT_NAME}-lib)
```

## add_definitions( )

变量名需要以D开头，变量在代码中作为宏定义出现

CMake文件：

```text CMakeLists.txt
add_definitions(
        -DCONFIG_FILE="${CMAKE_CURRENT_SOURCE_DIR}/config"
)
```

cpp文件：

```cpp
std::ifstream conf(CONFIG_FILE"/config");
```

## CMake说明网站

[CMake菜谱](https://www.bookstack.cn/read/CMake-Cookbook/content-preface-preface-chinese.md)

[GitBook](https://sfumecjf.github.io/cmake-examples-Chinese/)

[CMake 3.21 (中文)](https://runebook.dev/zh-CN/docs/cmake/-index-)
