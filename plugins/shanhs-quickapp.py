from .plugin import Plugin
import requests

# 插件名称
name = '闪鱼回收'
# 描述信息
description = """
闪鱼回收(快应用) 验证码登录接口

源代码: http://t4.market.mi-img.com/download/Mina/0be4f848bfdda409710fb2af45ace72848797f87c
更新时间: 2020-08-13
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class ShanhsQuickApp(Plugin):

    def run(self, options):

        requestData = {
            'phoneNo': options.telephone,
        }

        resp = requests.post('https://m.shanhs.com/sapi/user/getPhoneCode', json=requestData, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.shanhs.shanyuhuishou/1.0.5 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['status'] == '200':
            return True

        raise Exception(resp.text)

def instance():
    return ShanhsQuickApp(name, description, author, enable)

