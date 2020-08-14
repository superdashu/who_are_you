from .plugin import Plugin
import requests

# 插件名称
name = '及刻'

# 描述信息
description = """
及刻(快应用) 验证码登录接口

源代码: http://t5.market.xiaomi.com/download/Mina/0533b442aef87d6903ea6dc4c5a180f5f7041b181
更新时间: 2020-08-14
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class IGeekeeQuickApp(Plugin):

    def run(self, options):

        formData = {
            'areaCode': '+86',
            'phone': options.telephone,
        }

        resp = requests.post('https://poi.igeekee.cn/v2/user/send_msg', data=formData, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.sharedream.jike.quickapp.55/4.0.0.0 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['code'] == 200:
            return True

        raise Exception(body['msg'] if body['msg'] else resp.text)

def instance():
    return IGeekeeQuickApp(name, description, author, enable)

