from datetime import date, datetime, timedelta
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
import os
from util import get_accmulation_str, get_countdown_str, get_random_color, get_my_word, get_weather_str, get_week_day

#
# 变量
nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d") #今天的日期

#
# 系统变量
app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')
user_ids = os.getenv('USER_ID', '').split("\n")
template_id = os.getenv('TEMPLATE_ID')

citys = os.getenv('CITY', '').split("\n")
print("CITY: ", citys)
accumulation = os.getenv('SUMCNT', '').split("\n")
print("SUMCNT: ", accumulation)
countdown = os.getenv('COUNTDOWN', '').split("\n")
print("COUNTDOWN: ", countdown)

# check env vars
if app_id is None or app_secret is None:
  print('请设置 APP_ID 和 APP_SECRET')
  exit(422)
if not user_ids:
  print('请设置 USER_ID，若存在多个 ID 用回车分开')
  exit(422)
if template_id is None:
  print('请设置 TEMPLATE_ID')
  exit(422)

#
# text data
#

data = {
  "date": {
    "value": today.strftime('%Y年%m月%d日'),
    "color": get_random_color()
  },
  "week_day": {
    "value": get_week_day(today),
    "color": get_random_color()
  },

  "combine_weather": {
    "value": get_weather_str(citys),
    "color": get_random_color()
  },
  "combine_accumulation_count": {
    "value": get_accmulation_str(accumulation, today),
    "color": get_random_color()
  },
  "combine_countdown": {
    "value": get_countdown_str(countdown, today, nowtime),
    "color": get_random_color()
  },

  "words": {
    "value": get_my_word(),
    "color": get_random_color()
  },
}

#
# main
#

if __name__ == '__main__':
  try:
    client = WeChatClient(app_id, app_secret)
  except WeChatClientException as e:
    print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
    exit(502)

  wm = WeChatMessage(client)
  count = 0
  try:
    for user_id in user_ids:
      print('正在发送给 %s, 数据如下：%s' % (user_id, data))
      res = wm.send_template(user_id, template_id, data)
      count+=1
  except WeChatClientException as e:
    print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
    exit(502)

  print("发送了" + str(count) + "条消息")
