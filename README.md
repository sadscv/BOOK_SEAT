# 江西师范大学自习室位置帮抢脚本

## 为什么开发这个脚本？

本脚本由CZ制作，考研期间不喜欢抢位置，所以做了这个，考完之后加上了小伙伴的功能和四个自习室自由选择的功能，然后现在打算分享给大家，不要广为流传，自己默默用就好了=-=

## 怎么使用？

首先环境安装：使用PIP进行环境安装。

```
pip install requests
pip install schedule
```

接着填好脚本内注释了需要填的东西。

```python
​        'usernum': '',#学号

        'password': '',#密码

        'partnerFlag': 'true',  # 需要加入小伙伴则置为true,不用则为false。** 如果加入小伙伴则与小伙伴相关的内容都需要填写，并且正确！ **

        'partnerNum': '',#小伙伴学号

        'partnerName': '',#小伙伴的姓名,一定要和学号匹配！否则程序无法正常运行
        
        'wanna_room': '1',  # 1二楼南，2南楼北，3三楼北，4三楼南
        
        'wanna_seat': '99',  # 自己想要的位置
        
        'startTime': '9',  #想要开始的时间
        
        'partnerWannaSeat': '88',  # 小伙伴想要的位置
        
        'wanna_duration': '13',  # 想要在自习室待多久

```

通知问题：使用[server酱](http://sc.ftqq.com)进行通知，先前往server酱官网进行申请与绑定，得到一个server酱的Token，将此Token替换脚本内这个函数内的

```python
# 向Server酱发送消息以进行消息通知

def send_msg(msg='快来见抢座位程序最后一面啦~', state='false'):

​    r = requests.post('https://sc.ftqq.com/{}.send?text=位置预约系统的来信&desp={}'.format(Server酱的Token, msg))

​    r = r.json()

​    print(msg, r['errmsg'], state, datetime.datetime.now())
```

"**server酱的Token**"。  注意！！！这个token需要字符串形式，也就是两边要加上''或者""，否则将不会有消息通知的。



运行这个脚本则输入命令：

```
python3 自习室抢位置.py
```

## 运行的时候怎么调整数据？

如果想要初始化，就请停止这个脚本之后再删除同目录下的install.lock这个文件，之后再运行一遍这个脚本就好了。

想要调整位置信息可以直接更改test.json这个文件，不用停止脚本，反正随便皮。

## 想要立马测试程序怎么办？
如果想要测试这个程序，就把程序内的
```python
while True:
    schedule.run_pending()
    time.sleep(1)
# job()
```
注释了，然后job()取消注释，在 book_seat / book_seat_withPartner 这两个函数中的time.sleep(60.3)给相应的注释了。这样就可以立马测试程序。

## 想要一直防止服务器一直运行怎么办？
将
```python
while True:
    schedule.run_pending()
    time.sleep(1)
# job()
```
替换成
```python
while True:
    try:
        schedule.run_pending()
    except:
        print('预约失败！',datetime.datetime.now())
        pass
    time.sleep(1)
# job()
```
暴力解决。毕竟有太多的意外情况，总不能全都解决吧=-=

## PS

 **~~API啥的都隐去了，大家自己玩填空题嘛。~~**

我想了想还是把完整的代码放出来了。

 完全面向过程编程，面向对象是不存在的，怎么顺手怎么来！ 

## PPS

大佬愿意帮忙对象化的，可以联系我。就是提一个issue就可以了哦。不然pull request？

## PPPS

本人上线了本脚本的DEMO，感兴趣的可以试一试哦！

传送门——》[座位预约系统](http://bookseats.cunzao.xyz:8000/index/)



## 更新日志

2019年5月10日 16点55分

1.调整是否成功的判定条件

2.更新预约成功后位置信息获取的方式

3.更新内容通知的格式，使通知的信息更加完善

4.更新了README.MD，让脚本更易用


2019年6月22日 19点19分

1.加了能够修改开始时间的功能。没办法，这个脚本都是因为自己懒才写的，所以少功能啥的也正常哦！想要什么功能或者改进加个issue哦！

2.修改了小伙伴相关的bug，以前测试是在已经有json的情况下进行的，没有测试完全初始化的情况。

3.顺手增加了一点点注释，真的是一点点！


2019年7月2日 14点14分

1.将输出流重定向到文件了，默认打开，不需要则自己注释开头增加的那几段代码。

2.完善了使用说明，增加了测试相关的教程。

3.增加了预约今天位置的功能，一般用于测试，具体使用教程看 cal_begin_time 的代码注释。


2019年7月6日 16点21分

1.更新了位置预约的逻辑。

2.更新了程序定时功能的代码。

3.增加相应的try，防止程序意外退出。
