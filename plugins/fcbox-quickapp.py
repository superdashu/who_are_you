from .plugin import Plugin
import requests

# 插件名称
name = '丰巢快递柜'

# 描述信息
description = """
丰巢快递柜(快应用) 验证码登录接口

源代码: http://t2.market.mi-img.com/download/Mina/06c7640b836ff5f447267efad145e38460941bd24
更新时间: 2020-08-14
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class FcboxQuickApp(Plugin):

    def run(self, options):

        formData = {
            'phone': options.telephone
        }

        resp = requests.post('https://common.fcbox.com/common/quickApp/sendLoginMsg', data=formData, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.fcbox.express/1.1.0 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['code'] == '130100000':
            return True

        raise Exception(body['msg'] if body['msg'] else resp.text)

def instance():
    return FcboxQuickApp(name, description, author, enable)

