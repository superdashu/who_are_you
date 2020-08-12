from .plugin import Plugin
import requests
import hashlib
import time

# 插件名称
name = '房天下'
# 描述信息
description = """
房天下(微信小程序) 验证码登录接口

更新时间: 2020-08-12
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

class Fang(Plugin):

    def run(self, options):

        now = str(int(time.time() * 1000))

        params = {
            'appname': 'fangx',
            'v': '1.3.1',
            'miniplat': 'weixin',
            'mobilephone': options.telephone,
            'dataStr': now
        }

        signStr = 'dataStr={}&mobilephone={}'.format(now, options.telephone)
        params['sign'] = hashlib.md5(signStr.encode(encoding='utf-8')).hexdigest()

        resp = requests.get('https://miniapp.fang.com/weixin/appsendmobilecode', params=params, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2577 MMWEBSDK/200701 Mobile Safari/537.36 MMWEBID/1843 MicroMessenger/7.0.17.1720(0x27001137) Process/appbrand0 WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
            'referer': 'https://servicewechat.com/wxffbb41ec9b99a969/273/page-frame.html'
        })

        body = resp.json()
        body = body['common'][0]
        if body['return_result'] == '100':
            return True

        raise Exception(body['error_reason'] if body['error_reason'] else resp.text)


def instance():
    return Fang(name, description, author, enable)

