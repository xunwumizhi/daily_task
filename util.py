# -*- coding:utf-8 -*-
from urllib import request
from datetime import date, datetime, timedelta
import requests
import random

url = "https://raw.githubusercontent.com/xunwumizhi/written-expression/main/writing-notes.md"
spacer = "\r\n\r\n"
jumpStr = ("#", "```")

# 获取当前日期为星期几
def get_my_word():
    # content = request.urlopen(url).read().decode('utf-8')
    rsp = requests.get(url)
    content = rsp.content.decode('utf-8')
    cs = content.split(spacer)
    print("my word list len: ", len(cs))
    word = randomStr(cs)
    return word

def randomStr(cs):
    num_items = len(cs)
    random_index = random.randrange(num_items)
    word = cs[random_index]
    if word.startswith(jumpStr):
        return randomStr(cs)
    return word

# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']

# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

testCs = ['# 段落摘抄', '## 默念的时时刻刻', '```', "去哪里呀", "做核酸呀"]
# print(randomStr(testCs))
