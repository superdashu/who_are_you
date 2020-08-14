from .plugin import Plugin
import requests
import execjs

# 插件名称
name = '蜂助手'
# 描述信息
description = """
蜂助手(快应用) 验证码登录接口

源代码: http://t2.market.mi-img.com/download/Mina/009ce34be8b5c431a36c20052f1a2c478e71559f3
更新时间: 2020-08-14
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

jsCode = '''
function getNowFormatDate() {
    var e = new Date,
        t = e.getMonth() + 1,
        n = e.getDate();
    return t >= 1 && t <= 9 && (t = "0" + t), n >= 0 && n <= 9 && (n = "0" + n), e.getFullYear() + t + n + e.getHours() + e.getMinutes() + e.getSeconds()
}
'''

class PhoneQuickApp(Plugin):

    def run(self, options):

        vm = execjs.compile(jsCode)

        params = {
            'phonenum': options.telephone,
            'validCode': '',
            'key': vm.call('getNowFormatDate'),
            'templateid': '42',
            'modelid': '16',
        }

        resp = requests.get('https://www.phone580.com/fzsuserapi/user/sendsmscode', params=params, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.phone580.FZSService/1.1.0 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})',
        })

        body = resp.json()
        if body['success'] == True:
            return True

        raise Exception(body['message'] if body['message'] else resp.text)

def instance():
    return PhoneQuickApp(name, description, author, enable)

