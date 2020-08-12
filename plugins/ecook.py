from .plugin import Plugin
import requests
import json
import hashlib
import random

# 插件名称
name = '网上厨房'
# 描述信息
description = """
网上厨房(快应用) 验证码登录接口

源代码: http://t3.market.xiaomi.com/download/Mina/0cb6eb546d5574ad42e4958060f3c87029fb71ede
更新时间: 2020-08-12
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class ECook(Plugin):

    def run(self, options):

        # 伪造随机设备ID
        deviceId = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM01234567890', 40))

        formData = {
            'machine': hashlib.md5(deviceId.encode(encoding='utf-8')).hexdigest(),
            'appid': 'cn.ecook.qecook',
            'mobile': options.telephone,
            'terminal': '4',
            'version': '2.0.2',
            'device': 'Quick-AppXiaomi'
        }

        resp = requests.post('https://api.ecook.cn/public/sendMobileRegisterCode.shtml', data=formData, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 cn.ecook.qecook/2.0.2 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if int(body['state']) == 1:
            return True

        raise Exception(body['message'] if body['message'] else resp.text)


def instance():
    return ECook(name, description, author, enable)

