# -*- coding:utf-8 -*-
from urllib import request
import requests
import random
from dateutil import rrule
import re
from datetime import date, datetime, timedelta

def proc_wx_data(data):
    s = data["words"]["value"]
    n = 20  # 每个数组元素的长度
    result = []
    for i in range(0, len(s), n):
        result.append(s[i:i+n])
    print(result)

    for i in range(len(result)):
        data["line%d" % i] = {"value": result[i]}
    print("data %s" % data)

url = "https://raw.githubusercontent.com/xunwumizhi/written-expression/main/writing-notes.md"
spacer = "\r\n\r\n"
jumpStr = ("#", "```")
weather_format = "%s 天气 %s 空气质量 %s; 温度 %d ~ %d °C"
# 这是我们相识的第 %d 天|2022-08-06|day
# 距离妹妹的生日还有 %d 天|1997-02-03|30|今天是妹妹的生日，祝宝宝生日快乐！

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

# get_interval_count 是第几个起点
def get_interval_count(freq, st, until):
    points = rrule.rrule(freq, dtstart=st, until=until)
    # for point in list(points):
    #     print(point) # 打印间隔的每个月
    cnt = points.count()
    print("interval count: %d" % cnt)
    return cnt

# get_weather 直接返回对象，在使用的地方用字段进行调用。
def get_weather(city):
    if city == "":
        return None
    print(city)
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    print(res)
    if res is None:
        return None
    weather = res['data']['list'][0]
    return weather

# city = "101220101"         #城市天气查询的id ,根据自己城市上网查询即可,当前是合肥市
def get_weather_v1(cityCode):
    url = "http://t.weather.sojson.com/api/weather/city/" + cityCode
    res = requests.get(url).json()
    # weather = res['data']['list'][0]
    today = res['data']
    todayDetail = res['data']['forecast'][0]
    # return weather['quality'], math.floor(weather['wendu'])
    cityName = res['cityInfo']['city']
    weather = today['wendu']
    airQuality = today['quality']
    low = todayDetail['low']
    high = todayDetail['high']
    print(cityName,weather,airQuality,low,high)
    return 

# 获取当前日期为星期几
def get_week_day(today):
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    week_day = week_list[datetime.date(today).weekday()]
    return week_day

# get_sum_count 纪念数 freq: string, start_date: string, today: datetime
def get_sum_count(freq, start_date, today):
    if start_date == "":
        return None
    if freq == "year":
        love_freq = rrule.YEARLY
    elif freq == "month":
        love_freq = rrule.MONTHLY
    elif freq == "week":
        love_freq = rrule.WEEKLY
    else:
        love_freq = rrule.DAILY
    st = datetime.strptime(start_date, "%Y-%m-%d")
    cnt = get_interval_count(love_freq, st, today)
    # delta = today - st
    # cnt = delta.days
    return cnt

# get_counter_left 天数倒计时
def get_counter_left(aim_date, today, nowtime):
    if aim_date == "":
        return None
    # 为了经常填错日期的同学们
    if re.match(r'^\d{1,2}\-\d{1,2}$', aim_date):
        next = datetime.strptime(str(date.today().year) + "-" + aim_date, "%Y-%m-%d")
    elif re.match(r'^\d{2,4}\-\d{1,2}\-\d{1,2}$', aim_date):
        next = datetime.strptime(aim_date, "%Y-%m-%d")
        next = next.replace(nowtime.year)
    else:
        print('日期格式不符合要求')
        return 0
    if next < nowtime:
        next = next.replace(year=next.year + 1)
    days = (next - today).days
    # days = get_interval_count(rrule.DAILY, today, next)
    print(days)
    return days

# 
# string
#

def get_weather_str(citys):
    weatherStr = ""
    for city in citys:
        # st = get_weather(city)
        # cityName = city
        st = get_weather_v1(city)
        cityName = st['cityName']
        w = st['weather']
        aq = st['airQuality']
        lowest = st["low"]
        highest = st["high"]
        weatherStr += weather_format % (cityName, w, aq, lowest, highest)
        weatherStr += "\n"
    print(weatherStr)
    return weatherStr

# 这是我们相识的第 %d 天|2022-08-06|day
def get_accmulation_str(accumulation, today):
    aStr = ""
    for a in accumulation:
        arr = a.split("|")
        if len(arr) < 3:
            continue
        format = arr[0]
        start_date = arr[1]
        req = arr[2]
        love_cnt = get_sum_count(req, start_date, today)
        word = format % love_cnt
        aStr += word
        aStr += "\n"
    print(aStr)
    return aStr

# 距离妹妹的生日还有 %d 天|1997-02-03|30|今天是妹妹的生日，祝宝宝生日快乐！
def get_countdown_str(countdown, today, nowtime):
    cStr = ""
    for a in countdown:
        arr = a.split("|")
        if len(arr) < 4:
            continue
        format = arr[0]
        aim_date = arr[1]
        day_limit_str = arr[2]
        happy = arr[3]
        day_limit = int(day_limit_str)
        left = get_counter_left(aim_date, today, nowtime)
        if left == 365 or left == 366:
            word = happy
        elif left <= day_limit:
            word = format % left
        else:
            continue
        cStr += word
        cStr += "\n"
    print(cStr)
    return cStr



'''
testing case
'''

# get_interval_count(rrule.DAILY,datetime.date(2022,8,6),datetime.date(2022,8,9))
# get_interval_count(rrule.WEEKLY,datetime.date(2022,8,6),datetime.date(2022,8,13))
# get_interval_count(rrule.MONTHLY,datetime.date(2022,8,6),datetime.date(2022,8,7))

# nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间 2022-10-07 15:30:11.195544
# today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d") # 今日零点 2022-10-07 00:00:00

# print(get_weather("深圳"))
# print(get_week_day(today))
# get_sum_count("month", "2022-08-06", date(2022, 10, 7))
# print(get_counter_left("2022-10-09",datetime(2022,10,7),nowtime))

# s = "深圳\n西安"
# get_weather_str(s.split("\n"))
# s = "这是我们相识的第 %d 天|2022-08-06|day"
# get_accmulation_str(s.split("\n"), today)
# s = "距离妹妹的生日还有 %d 天|1997-10-08|300|今天生日！"
# get_countdown_str(s.split("\n"), today, nowtime)

## 天气测试
#
# get_weather_v1('101220101')