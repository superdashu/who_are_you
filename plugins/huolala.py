from .plugin import Plugin
import requests
import execjs
import json
import hashlib

# 插件名称
name = '货拉拉'
# 描述信息
description = """
货拉拉(快应用) 验证码登录接口

源代码: http://t2.market.mi-img.com/download/Mina/0533b442a7f87e6909ea68c4c2a182f5f5041b181
更新时间: 2020-08-12
"""

# 作者
author = 'kksanyu'

# 是否启用该插件
enable = False

jsCode = '''
function timeStampFormat(e, t) {
    10 === parseInt(e).toString().length && (e *= 1e3);
    var n = new Date(e),
        r = {
            "M+": n.getMonth() + 1,
            "d+": n.getDate(),
            "h+": n.getHours(),
            "m+": n.getMinutes(),
            "s+": n.getSeconds(),
            "q+": Math.floor((n.getMonth() + 3) / 3),
            S: (n.getMilliseconds() + "").padStart(3, "0")
        };
    for (var o in /(y+)/.test(t) && (t = t.replace(RegExp.$1, (n.getFullYear() + "").substr(4 - RegExp.$1.length))), r) new RegExp("(" + o + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? r[o] : ("00" + r[o]).substr(("" + r[o]).length)));
    return t
}

function m() {
    for (var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : 10, t = [], n = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], r = 0; r < e; r++) {
        var o = Math.floor(10 * Math.random());
        t[r] = n[o]
    }
    return t.join("")
}

function v() {
    var e = timeStampFormat(Date.now(), "yyMMddhhmmssS");
    return "".concat(e, "1000000").concat(m())
}
'''

class Huolala(Plugin):

    def run(self, options):

        vm = execjs.compile(jsCode)

        params = {
            'token': '',
            '_ref': '',
            'revision': '2700',
            '_su': vm.call('v'),
            'user_md5': hashlib.md5(''.encode(encoding='utf-8')).hexdigest(),
            'appversion': '2.4.30',
            'sub_revision': '1002',
        }

        params['_m'] = 'send_sms_code'
        params['phone_no'] = options.telephone
        params['img_code'] = ''

        # 计算签名
        signStr = ''
        for key, value in sorted(params.items(), key=lambda x: x[0]):
            signStr += key + value

        signStr += 'quickapp.huolala.cn'
        params['_sign'] = hashlib.md5(signStr.encode(encoding='utf-8')).hexdigest()


        resp = requests.get('https://quickapp.huolala.cn/index.php', params=params, headers={
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; MI 9 Transparent Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 hap/1.7/xiaomi com.miui.hybrid/1.7.3.2 com.huolala.client_quickapp/2.4.30 ({"packageName":"com.miui.quickappCenter","type":"url","extra":{"scene":"allquickapp"}})'
        })

        body = resp.json()
        if body['ret'] == 0:
            return True
        
        raise Exception(body['msg'] if body['msg'] else resp.text)


def instance():
    return Huolala(name, description, author, enable)

