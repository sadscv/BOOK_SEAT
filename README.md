**# 江西师范大学自习室位置帮抢脚本**

**## 为什么开发这个脚本？**

本脚本由CZ制作，考研期间不喜欢抢位置，所以做了这个，考完之后加上了小伙伴的功能和四个自习室自由选择的功能，然后现在打算分享给大家，不要广为流传，自己默默用就好了=-=

**## 怎么使用？**

首先环境安装：使用PIP进行环境安装。

```
pip install requests
pip install schedule
```

接着填好脚本内注释了需要填的东西。

```python
		 'usernum': '',#学号

​        'password': '',#密码

​        'partnerFlag': 'true',  # 需要加入小伙伴则置为true，默认不需要小伙伴

​        'partnerNum': '',#小伙伴学号,需要加入小伙伴则填写

​        'partnerName': '',#小伙伴的姓名，需要加入小伙伴则写

​        'wanna_room': '1',  # 1二楼南，2南楼北，3三楼北，4三楼南

​        'wanna_seat': '99',  # 自己想要的位置

​        'partnerWannaSeat': '88',  # 小伙伴想要的位置，需要加入小伙伴则写

​        'wanna_duration': '13',  # 想要在自习室待多久
```

通知问题：使用[server酱](http://sc.ftqq.com)进行通知，先前往server酱官网进行申请与绑定，得到一个server酱的Token，将此Token替换脚本内这个函数内的

```python
# 向Server酱发送消息以进行消息通知

def send_msg(msg='快来见抢座位程序最后一面啦~', state='false'):

​    r = requests.post(

​        'https://sc.ftqq.com/'+ Server酱的Token +'.send?text=位置预约系统的来信&desp={}'.format(msg))

​    r = r.json()

​    print(msg, r['errmsg'], state, datetime.datetime.now())
```

"**server酱的Token**"。  



最后运行这个脚本，输入命令：

```
python3 自习室抢位置.py
```

**## 运行的时候怎么调整数据？**

如果想要初始化，就请停止这个脚本之后再删除同目录下的install.lock这个文件，之后再运行一遍这个脚本就好了。

想要调整位置信息可以更改test.json这个文件，反正随便皮。

**## PS**

 **~~API啥的都隐去了，大家自己玩填空题嘛。~~**

我想了想还是把完整的代码放出来了。

 完全面向过程编程，面向对象是不存在的，怎么顺手怎么来！ 

**## PPS**

大佬愿意帮忙对象化的，可以联系我。

**## PPPS**

本人上线了本脚本的DEMO，感兴趣的可以试一试哦！

传送门——》[座位预约系统](http://bookseats.cunzao.xyz:8000/index/)