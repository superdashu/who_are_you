from .plugin import Plugin
import requests
import execjs
import json
import hashlib
import time
import random

# 插件名称
name = '菜谱大全'
# 描述信息
description = """
菜谱大全(快应用) 验证码登录接口

源代码: http://t2.market.xiaomi.com/download/Mina/06c7650b866ffbf4492679fade45e9846c941bd24
更新时间: 2020-08-13
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

jsCode = '''
function _(t) {
    var e = [];
    for (var n in t) e.push(n);
    e.sort();
    var r = "";
    for (var o in e) null != t[e[o]] && (r += e[o] + "=" + t[e[o]] + "&");
    return r.substr(0, r.length - 1)
}
'''

class XianghaQuickApp(Plugin):

    def run(self, options):

        vm = execjs.compile(jsCode)

        # 获取token
        resp = requests.post('https://apielf.xiangha.com/common/public/auth/getToken', json={}, headers={
            'xh-client-data': json.dumps({
                "appId": 3
            }),
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.xhquickapp/2.3.0 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['code'] != 10000:
            raise Exception(body['msg'] if body['msg'] else resp.text)

        token = body['data']['token']

        # 发起请求
        requestData = {
            'tel': options.telephone,
        }
        
        timestamp = int(time.time())
        noncestr = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM01234567890', 32))

        d = {
            'accesstoken': token,
            'noncestr': noncestr,
            'timestamp': timestamp,
            'tel': options.telephone
        }
        sign = hashlib.md5((vm.call('_', d) + '19CBB4C0045DAA37').encode(encoding='utf-8')).hexdigest()

        resp = requests.post('https://apielf.xiangha.com/QuickApp/V1/index/sendVerifyCode', json=requestData, headers={
            'xh-client-data': json.dumps({
                'appId': 3,
                'accesstoken': token,
                'sign': sign,
                'noncestr': noncestr,
                'timestamp': timestamp
            }),
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.xhquickapp/2.3.0 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['code'] == 10000:
            return True

        raise Exception(body['msg'] if body['msg'] else resp.text)

def instance():
    return XianghaQuickApp(name, description, author, enable)

