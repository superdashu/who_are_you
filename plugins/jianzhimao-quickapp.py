from .plugin import Plugin
import requests

# 插件名称
name = '兼职猫'
# 描述信息
description = """
兼职猫(快应用) 验证码登录接口

源代码: http://t1.market.xiaomi.com/download/Mina/0b16d85057e984bfc26495b2d981b874e426e317d
更新时间: 2020-08-13
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class JianzhimaoQuickApp(Plugin):

    def run(self, options):

        params = {
            'business': '1',
            'phone': options.telephone,
            'type': '1'
        }

        resp = requests.get('https://fast.jianzhimao.com/api/sms', params=params, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.joiway.jianzhi/1.4.5 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['code'] == 200:
            return True

        raise Exception(body['message'] if body['message'] else resp.text)

def instance():
    return JianzhimaoQuickApp(name, description, author, enable)

