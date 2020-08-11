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

