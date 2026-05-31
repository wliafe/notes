---
title: Qt for Python
date: 2025-05-27 17:25:19
categories:
    - 前端
tags:
    - Python
---

Qt框架是一个跨平台的C++应用程序开发框架，由Qt公司开发。Qt框架提供了一组丰富的GUI组件和工具，用于开发Windows、Linux、macOS等操作系统的应用程序。Qt for Python也叫Pyside，是一个基于Qt框架的Python绑定库，它可以让Python开发者使用C++编写的Qt应用程序。本文主要讲Qt for Python的安装和使用。

<!--more-->

## Qt for Python环境搭建

### 安装基础环境（Linux，Windows不用）

```bash
sudo apt update
```

```bash
sudo apt upgrade
```

```bash
sudo apt-get install libxcb-*
```

```bash
sudo apt-get install libxkbcommon-x11-0
```

### 搭建Python环境

我的Python环境主要依赖于uv，有关uv的详细内容可以参考我的博客{% post_link uv %}

创建Qt环境

```bash
uv init
```

安装Qt for Python

```bash
uv add pyside6
```

### 安装VSCode Qt for Python插件

![VSCode Qt for Python插件](1.png)

### 解决输出界面所有中文乱码中部分的乱码问题(标题乱码未解决)（Linux）

```bash
sudo apt-get install fonts-noto-cjk
```

### 解决wayland错误（Linux）

{% note danger %}
Failed to create wl_display (No such file or directory)
qt.qpa.plugin: Could not load the Qt platform plugin "wayland" in "" even though it was found.
{% endnote %}

在代码中加入下面这一行

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'
```

## Qt打包

使用pyside6-deploy打包exe文件时，可以通过修改nuitka的一些参数来达到想要的效果

### pyside6-deploy打包exe不显示终端窗口

这里假设你的主文件是`main.py`文件。

生成打包配置文件`pysidedeploy.spec`

```bash
pyside6-deploy --init
```

在`pysidedeploy.spec`文件中[nuitka]的extra_args中添加下面的参数

```text pysidedeploy.spec
--windows-console-mode=disable
```

运行打包命令

```bash
pyside6-deploy
```

## Qt使用GUI实时显示logging信息

要实现Qt使用GUI实时显示logging信息这个功能，需要两个条件，一个是给logging添加QtHandler，另一个是使用QThread执行运算程序，主线程用来更新界面显示。

### QTextBrowserHandler

由于Qt显示logging的GUI工具是TextBrowser，所以我定义了一个QTextBrowserHandler类，用来将logging的信息输出到TextBrowser中。

```python
class QTextBrowserHandler(logging.Handler, QObject):
    '''自定义Qt日志处理器'''
    signal = Signal(str)

    def __init__(self):
        '''初始化'''
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, record):
        '''重写日志输出方法'''
        msg = self.format(record)
        self.signal.emit(msg)
```

### QThread

QThread是Qt中的线程类，用来执行耗时的操作。我定义了一个QWorkThread类，用来执行run函数。

```python
class QWorkThread(QThread):
    '''自定义Qt线程'''

    def set_run(self, run):
        '''设置线程执行函数'''
        def run_func():
            try:
                run()
            except Exception as e:
                logger = logging.getLogger('qt')
                logger.error(f"run函数执行时发生异常: {e}")
        self.run = run_func
```

### 简单样例

新建`example.ui`文件，使用VSCode插件编辑界面，这个编辑后保存的文件

```xml example.ui
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>样例</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QPushButton" name="pushButton">
     <property name="text">
      <string>hello world</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QTextBrowser" name="textBrowser"/>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
```

这个文件是插件自动根据`.ui`文件生成的。

```python example_ui.py
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'example.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u6837\u4f8b", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"hello world", None))
    # retranslateUi
```

这个是执行文件，里面有之前的两个工具，还有一个打印hello world的run函数。

```python example.py
import sys
import logging
from PySide6.QtCore import Signal, QObject, QThread
from PySide6.QtWidgets import QApplication, QWidget
from example_ui import Ui_Form


class QTextBrowserHandler(logging.Handler, QObject):
    '''自定义Qt日志处理器'''
    signal = Signal(str)

    def __init__(self):
        '''初始化'''
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, record):
        '''重写日志输出方法'''
        msg = self.format(record)
        self.signal.emit(msg)


class QWorkThread(QThread):
    '''自定义Qt线程'''

    def set_run(self, run):
        '''设置线程执行函数'''
        def run_func():
            try:
                run()
            except Exception as e:
                logger = logging.getLogger('qt')
                logger.error(f"run函数执行时发生异常: {e}")
        self.run = run_func


class Run:
    def __init__(self, logger=None):
        """
        初始化 Run 类的实例。

        Args:
            logger (logging.Logger, optional): 可选的日志记录器对象。如果提供，则使用该日志记录器；否则创建一个新的日志记录器。默认值为 None。
        """
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")  # 设置日志格式
        if logger:
            self.logger = logger
        else:
            # 设置日志
            self.logger = logging.getLogger('run')  # 创建日志
            self.logger.setLevel(logging.DEBUG)  # 设置日志等级
            # 添加控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def print_hello_world(self):
        self.logger.info('hello world')


class Example(QWidget):
    '''自定义Qt主窗口'''

    def __init__(self):
        '''初始化'''
        QWidget.__init__(self)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")  # 设置日志格式
        # 设置日志
        self.logger = logging.getLogger('qt')  # 创建日志
        self.logger.setLevel(logging.DEBUG)  # 设置日志等级
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        # 添加qt处理器
        qt_handler = QTextBrowserHandler()
        qt_handler.setLevel(logging.INFO)
        qt_handler.setFormatter(formatter)
        self.logger.addHandler(qt_handler)
        # 定义执行函数
        self.run = Run(self.logger)
        # 初始化界面
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 定义执行线程
        self.thread = QWorkThread(self)
        # 事件绑定
        qt_handler.signal.connect(self.ui.textBrowser.append)
        self.ui.pushButton.clicked.connect(self.start_run)

    def start_run(self):
        '''开始执行run函数'''
        self.thread.set_run(self.run.print_hello_world)
        self.thread.start()  # 线程启动，执行run函数


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Example()
    window.show()

    sys.exit(app.exec())
```

这是这个程序的显示结果

![程序执行结果](2.png)
