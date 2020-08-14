from .plugin import Plugin
import requests

# 插件名称
name = '车轮查违章'

# 描述信息
description = """
车轮查违章(快应用) 验证码登录接口

源代码: http://t4.market.xiaomi.com/download/Mina/0f89141832d19a58c701fe46326d3d9489342cd4c
更新时间: 2020-08-14
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class ChelunQuickApp(Plugin):

    def run(self, options):

        formData = {
            'phone': options.telephone,
        }

        resp = requests.post('https://passport.chelun.com/api_v2/get_sms_captcha?os=h5', data=formData, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.eclicks.wzsearch/1.0.3 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['code'] == 1:
            return True

        raise Exception(body['msg'] if body['msg'] else resp.text)

def instance():
    return ChelunQuickApp(name, description, author, enable)

