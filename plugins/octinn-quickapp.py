from .plugin import Plugin
import requests

# 插件名称
name = '订蛋糕'
# 描述信息
description = """
订蛋糕(快应用) 验证码登录接口

源代码: http://t5.market.xiaomi.com/download/Mina/0e9584b8c7a402421c82b27925f18cc422d41e3e6
更新时间: 2020-08-14
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class OctinnQuickApp(Plugin):

    def run(self, options):

        requestData = {
            'phone': options.telephone,
            'type': 5
        }

        resp = requests.post('https://api.octinn.com/account/send_verify_code', json=requestData, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.octinn.cake/1.2.1 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
            'oi-udid': '',
            'oi-type': 'USER',
            'oi-appkey': '1b999165537c1929dcbfb7dafdc72247',
            'oi-auth': '',
            'oi-apiver': '27',
            'oi-chn': '0'
        })

        body = resp.json()
        if 'ticket' in body:
            return True

        raise Exception(body['msg'] if body['msg'] else resp.text)

def instance():
    return OctinnQuickApp(name, description, author, enable)

