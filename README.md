who_are_you
=====
[![License](https://img.shields.io/github/license/kksanyu/who_are_you)](https://github.com/kksanyu/who_are_you)

### 概述

一种礼貌回应陌生人的方式

### 开发

克隆项目

```shell
$ git clone https://github.com/kksanyu/who_are_you.git
$ cd who_are_you
```

安装依赖

```shell
$ pip install requests
$ pip install js2py
$ pip install pyexecjs
```

### 使用

```shell
# 帮助
$ python run.py -h

# 指定插件测试
$ python run.py -f 插件名称 -t 手机号

# 运行所有插件
$ python run.py -t 手机号
```

#### 添加一个自定义插件

在 `plugins` 目录下, 添加一个 `demo.py`, 实例代码如下

```shell
from .plugin import Plugin
import js2py

# 插件名称
name = '测试插件'
# 描述信息
description = """
仅供测试
""" 
# 作者
author = 'kksanyu'
# 是否启用该插件
enable = True

# 演示js代码
jsAddFunc = """
function add(a, b) {
    return a + b;
}
"""

class Demo(Plugin):

    def run(self, options):
        print('运行Demo::run', options.telephone)
        # raise RuntimeError('测试异常')

        add = js2py.eval_js(jsAddFunc)
        
        a = 1
        b = 2
        c = add(a, b)
        print('计算结果', c)


def instance():
    return Demo(name, description, author, enable)
```

测试

```shell
$ python run.py -f demo -t 手机号
```


### 相关查阅文档

- [requests文档](https://requests.readthedocs.io/)

### 已知问题

- js2py在复杂的混淆算法下, 可能会运行缓慢或者执行js报错，这种情况下可以考虑使用其他库、重写js方法为python函数、通过调用nodejs来曲线救国。

### License

The MIT License(http://opensource.org/licenses/MIT)

请自由地享受和参与开源

