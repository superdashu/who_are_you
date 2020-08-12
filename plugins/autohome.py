from .plugin import Plugin
import requests
import hashlib
import base64
import time

# 插件名称
name = '汽车之家极速版'
# 描述信息
description = """
汽车之家极速版(快应用) 验证码登录接口

源代码: http://t4.market.xiaomi.com/download/Mina/0b30a5ae89ca689a7c56aaa6a634762362c4170db
更新时间: 2020-08-12
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class AutoHome(Plugin):

    def run(self, options):

        params = {
            'validType': '13',
            'sourceFromType': 'quickapp',
            'mobile': base64.b64encode(options.telephone.encode(encoding="utf-8")).decode(),
            '_appid': 'wxapp.fastapp',
            '_timestamp': str(int(time.time())),
            'quickappversion': '5.32.1',
        }

        appkey = '$auto@Fast|App123'

        # 计算签名
        signStr = ''
        for key, value in sorted(params.items(), key=lambda x: x[0]):
            signStr += key + value

        signStr = appkey + signStr + appkey
        params['_sign'] = hashlib.md5(signStr.encode(encoding='utf-8')).hexdigest()

        resp = requests.get('https://wxcar.api.autohome.com.cn/api/user/CreateValidCode', params=params, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.autohome.quickapp/5.32.1 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})'
        })

        body = resp.json()
        if body['returncode'] == 0:
            return True
        
        raise Exception(body['message'] if body['message'] else resp.text)


def instance():
    return AutoHome(name, description, author, enable)

