# -*- coding:utf-8 -*-
from urllib import request
import datetime
import requests
import random
from dateutil import rrule

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

# get_interval_count 有几个起点
def get_interval_count(freq, st, until):
    points = rrule.rrule(freq, dtstart=st, until=until)
    # for point in list(points):
    #     print(point) # 打印间隔的每个月
    cnt = points.count()
    print(cnt)
    return cnt

# get_interval_count(rrule.DAILY,datetime.date(2022,8,6),datetime.date(2022,8,9))
# get_interval_count(rrule.WEEKLY,datetime.date(2022,8,6),datetime.date(2022,8,13))
# get_interval_count(rrule.MONTHLY,datetime.date(2022,8,6),datetime.date(2022,8,7))
