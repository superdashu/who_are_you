from .plugin import Plugin
import requests
import execjs
import hashlib
import time
import base64

# 插件名称
name = '奔腾'

# 描述信息
description = """
奔腾(快应用) 验证码登录接口

源代码: http://t5.market.xiaomi.com/download/Mina/01ef9b462d86b4b141da59a0c219a59f3a96437d1

更新时间: 2020-08-14
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

jsCode = '''
function randomString(t) {
    t = t || 32;
    for (var e = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678", r = e.length, n = "", i = 0; i < t; i++) n += e.charAt(Math.floor(Math.random() * r));
    return n
}

function getDeviceId() {
    return '' + Math.ceil(100000 * Math.random());
}
'''

class PhoneQuickApp(Plugin):

    def run(self, options):

        vm = execjs.compile(jsCode)

        # 获取token
        appId = '27527019'
        appSecret = 'WtegFvnxIrAqkKINXYUpnIScqFJijpFm'
        randStr = vm.call('randomString')
        deviceId = hashlib.md5(vm.call('getDeviceId').encode('utf-8')).hexdigest()
        timestamp = str(int(time.time()))

        signature = hashlib.md5('app_id={}&app_secret={}&device_id={}&rand_str={}&timestamp={}'.format(appId, appSecret, deviceId, randStr, timestamp).encode('utf-8')).hexdigest()

        resp = requests.post('https://benteng.ad.xiaomi.com/api/5a60c77b79875', data={
            'rand_str': randStr,
            'device_id': deviceId,
            'signature': signature,
            'app_id': appId,
            'timestamp': timestamp
        }, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.duoguanhudong.fawpentium/1.9.13 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
            'client': 'XCX',
            'version': 'v1.0.0'
        })

        body = resp.json()
        if body['code'] != 1:
            raise Exception(body['msg'] if body['msg'] else resp.text)


        accessToken = body['data']['access_token']

        resp = requests.get('https://benteng.ad.xiaomi.com/api/5acd9f48bb275', params={
            'access_token': accessToken,
            'mobile': str(base64.b64encode(options.telephone.encode('utf-8')), 'utf-8'),
            'user_token': '',
            'type': '0',
            'versionwith': 'v1.0.0'
        }, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.duoguanhudong.fawpentium/1.9.13 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
            'client': 'XCX',
            'access-token': accessToken,
            'user-token': '',
            'version': 'v1.0.0'
        })

        body = resp.json()
        if body['code'] == 1:
            return True

        raise Exception(body['msg'] if body['msg'] else resp.text)

def instance():
    return PhoneQuickApp(name, description, author, enable)

