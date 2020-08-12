#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import plugins

def usePlugin(name, args):
    plugin = __import__('plugins.' + name, fromlist=[name])

    if not plugin.enable:
        return plugin.name, False, '插件未启用'
    
    isSuccess, e = plugin.instance().execute(args)
    return plugin.name, isSuccess, e

def main():

    parser = argparse.ArgumentParser(description='一种礼貌回应陌生人的方式')
    parser.add_argument('-f', '--file', metavar='指定插件', required=False, help='一般在测试的时候使用')
    parser.add_argument('-t', '--telephone', metavar='手机号码', required=True)
    args = parser.parse_args()
    
    allPlugin = plugins.__all__

    print('插件数量', len(allPlugin), '个')

    # 单插件测试需要校验是否存在
    if args.file != None:
        try:
            allPlugin.index(args.file)
        except Exception as e:
            print('指定插件', args.file, '不存在')
            return
        
        pluginName, isSuccess, e = usePlugin(args.file, args)
        print(pluginName, '执行成功' if isSuccess else '执行失败', e)
        return


    # 遍历所有插件
    for name in allPlugin:
        pluginName, isSuccess, e = usePlugin(name, args)
        print(pluginName, '执行成功' if isSuccess else '执行失败', e)


if __name__ == '__main__':
    main()

