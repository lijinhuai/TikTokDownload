#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:__init__.py
@Date       :2022/07/29 23:20:56
@Author     :JohnserfSeed
@version    :1.3.0.54
@License    :(C)Copyright 2019-2022, Liugroup-NLPR-CASIA
@Github     :https://github.com/johnserf-seed
@Mail       :johnserfseed@gmail.com
-------------------------------------------------
Change Log  :
2022/07/29 23:20:56 : Init
2022/08/16 18:34:27 : Add moudle Log
-------------------------------------------------
'''

import re
import os
import json
import time
import random
import asyncio
import logging
import requests
import platform
import argparse
import configparser

from lxml import etree
from TikTokUpdata import Updata

from .XB import XBogus
from .Log import Log
from .Urls import Urls
from .Lives import Lives
from .Check import CheckInfo
from .Config import Config
from .Command import Command
from .Profile import Profile
from .Download import Download
from .Images import Images

# 日志记录
log = Log()


def generate_random_str(randomlength=16):
    """
    根据传入长度产生随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
    length = len(base_str) - 1
    for _ in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def generate_ttwid() -> str:
    """生成请求必带的ttwid
    param :None
    return:ttwid
    """
    url = 'https://ttwid.bytedance.com/ttwid/union/register/'
    data = '{"region":"cn","aid":1768,"needFid":false,"service":"www.ixigua.com","migrate_info":{"ticket":"","source":"node"},"cbUrlProtocol":"https","union":true}'
    response = requests.request("POST", url, data=data)
    # j = ttwid  k = 1%7CfPx9ZM.....
    for j, k in response.cookies.items():
        return k

odin_tt = 'a09d8eb0d95b7b9adb4b6fc6591918bfb996096967a7aa4305bd81b5150a8199d2e29ed21883cdd7709c5beaa2be3baa'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'referer':'https://www.douyin.com/',
    # 获取用户数据失败就自行替换ttwid
    'Cookie': f'msToken={generate_random_str(107)};ttwid={generate_ttwid()};odin_tt={odin_tt}'
}


def replaceT(obj):
    """替换文案非法字符

    Args:
        obj (_type_): 传入对象

    Returns:
        new: 处理后的内容
    """
    if len(obj) > 80:
        obj = obj[:80]
    # '/ \ : * ? " < > |'
    reSub = r"[^\u4e00-\u9fa5^a-z^A-Z^0-9^#]"  # '/ \ : * ? " < > |'
    new = []
    if type(obj) == list:
        for i in obj:
            # 替换为下划线
            retest = re.sub(reSub, "_", i)
            new.append(retest)
    elif type(obj) == str:
        # new = eval(repr(obj).replace('\\', '_').replace('/','_').replace(':','_').replace('*','_').replace('?','_').replace('<','_').replace('>','_').replace('|','_').replace('"','_'))
        # 替换为下划线
        new = re.sub(reSub, "_", obj, 0, re.MULTILINE)
    return new


def Status_Code(code: int):
    if code == 200:
        return
    else:
        log.info('[  提示  ]:该视频%i，暂时无法解析！' % code)
        print('[  提示  ]:该视频%i，暂时无法解析！' % code)
        return


def reFind(strurl):
    """匹配分享的url地址

    Args:
        strurl (string): 带文案的分享链接

    Returns:
        result: url短链
    """
    # 空数据判断
    if strurl == '':
        return strurl
    result = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', strurl)
    return result


print('''
  ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗
  ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗
     ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║
     ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║
     ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝
     ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝
     ''')

print("#" * 120)
print(
    """
                                                TikTokTool V1.3.0.54
        使用说明：
                1、本程序目前支持命令行调用和配置文件操作，GUI预览版本已经发布
                2、命令行操作方法：1）将本程序路径添加到环境变量
                                2）控制台输入 TikTokTool -u https://v.douyin.com/jqwLHjF/

                3、配置文件操作方法：1）运行软件前先打开目录下 conf.ini 文件配置用户主页和音乐下载模式
                                2）按照控制台输出信息操作

                4、如有您有任何bug或者意见反馈请在 https://github.com/Johnserf-Seed/TikTokDownload/issues 发起
                5、GUI预览版本现已发布，操作更简单 https://github.com/Johnserf-Seed/TikTokDownload/tags 下载
                6、TikTokLive 输入抖音直播间web端链接，例如 https://live.douyin.com/176819813905
                7、新版工具fastdl正在开发中 ----> https://github.com/Johnserf-Seed/fastdl

        注意：  目前已经支持app内分享短链和web端长链识别。
        """
)
print("#" * 120)
print('\r')

if (platform.system() == 'Windows'):
    sprit = '\\'
    # 💻
    print('[   💻   ]:Windows平台')
elif (platform.system() == 'Linux'):
    sprit = '/'
    # 🐧
    print('[   🐧   ]:Linux平台')
else:
    sprit = '/'
    # 🍎
    print('[   🍎   ]:MacOS平台')

# 检查版本
Updata().get_Updata()
