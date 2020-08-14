from .plugin import Plugin
import requests

# 插件名称
name = '瓜子二手车'
# 描述信息
description = """
瓜子二手车(快应用) 验证码登录接口

源代码: http://t4.market.mi-img.com/download/Mina/0ce4f488bbd7ad09980fb9af47fce22847f417578
更新时间: 2020-08-14
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class GuaziQuickApp(Plugin):

    def run(self, options):

        formData = {
            'phone': options.telephone,
            'source': '12'
        }

        resp = requests.post('https://mapi.guazi.com/user/account/sendLoginCode', data=formData, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.application.gz.quick/4.6.5 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['code'] == 0:
            return True

        raise Exception(body['msg'] if body['msg'] else resp.text)

def instance():
    return GuaziQuickApp(name, description, author, enable)

