from .plugin import Plugin
import requests

# 插件名称
name = '饿了么'
# 描述信息
description = """
饿了么(快应用) 验证码登录接口

更新时间: 2020-08-12
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class ElemeQuickApp(Plugin):

    def run(self, options):

        requestData = {
            'mobile': options.telephone,
            'captcha_hash': '',
            'captcha_value': ''
        }

        resp = requests.post('https://mainsite-restapi.ele.me/eus/login/mobile_send_code', json=requestData, headers={
            'x-quickapp': 'versionName=1.24.13;versionCode=258;packageName=me.ele.xyy;runtimePkg=com.miui.quickappCenter',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 me.ele.xyy/1.24.13 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if 'validate_token' in body and body['validate_token'] != None and body['validate_token'] != '':
            return True

        raise Exception(body['message'] if body['message'] else resp.text)


def instance():
    return ElemeQuickApp(name, description, author, enable)

