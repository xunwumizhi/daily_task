# 测试公众号推送

## 使用说明

代码里面要求的配置：

APP_ID: 公众平台 appID

APP_SECRET: 公众平台 appSecret

TEMPLATE_ID: 模板 ID

USER_ID: 接收人的 OpenID 多个用换行分隔

BIRTHDAY: 倒数日（原生日），换行分隔，见更新说明。格式如 05-20，1999-11-04 这种

START_DATE: 正数日期，格式：2008-08-08

CITY: 城市，不要加市，准确到地级市。比如：北京、天津、广州、承德。

最终推送模板见：[here](./template.md)

ps. 有一些注意事项在此补充

1. 第一次登录微信公众平台测试号给的 app secret 是错误的，刷新一下页面即可
2. 生日的日期格式是：`05-20`，纪念日的格式是 `2022-08-09`，请注意区分。城市请写到地级市，比如：`北京`，`广州`，`承德`
3. 变量中粘贴的各种英文字符串不要有空格，不要有换行，除了模板之外都没有换行
4. Github Actions 的定时任务，在 workflow 的定义是 `0 0 * * *`，是 UTC 时间的零点，北京时间的八点。但是由于 Github 同一时间任务太多，因此会有延迟

## 代码 DIY
如果你有一个自己的服务器，或是不会关机的电脑，可以通过如下方式使用代码。本项目使用Python3。

1. 首先clone本仓库：

```bash
git clone https://github.com/rxrw/daily_morning.git
```

2. 安装依赖：

```bash
cd daily_morning

pip3 install -r requirements.txt
```

3. 根据示例完成配置文件`config.yaml`

4. 运行代码`timer.py`，即可实现每日定时发送：

```bash
python3 timer.py
```

附：当然，如果你有多个女朋友，你可以在微信公众平台上为她们设置不同的模板，并且为每个人分别建立一个配置文件，例如：`xiaomei.yaml` 和`xiaohong.yaml`（注意在配置时千万不要写错了`user_ids`）。然后同时运行两个服务：
```bash
python3 timer.py --cfg xiaomei.yaml &

python3 timer.py --cfg xiaohong.yaml &
```
