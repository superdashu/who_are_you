
# 插件基类
class Plugin(object):
    
    # 构造函数
    def __init__(self, name, description, author, enable):
        self._name = name
        self._description = description.strip()
        self._author = author
        self._enable = enable

    # 获取版本信息
    @property
    def version(self):
        return {
            'name': self._name,
            'description': self._description,
            'author': self._author
        }

    # 执行
    def execute(self, options):
        try:
            self.run(options)
        except Exception as e:
            return False, e
        else:
            return True, None
