#import something
import datetime
import requests
# import schedule
import random
import time
import json
import os
import sys



# 自定义输出
def myPrint(*myPrintStr):
    temp = ''
    for i in myPrintStr:
        temp += str(i)
    print('时间：{}，{}'.format(datetime.datetime.now(), temp))
    logFile = open('test.log','a',encoding='utf-8')
    # 输出信息到文件，不需要则注释这个输出
    print('时间：{}，{}'.format(datetime.datetime.now(), temp), file = logFile)

# 创建配置文件
def create_json_file():
    file = open('test.json', 'w', encoding='utf-8-sig')
    CZ_Data = {
        'usernum': '',#学号
        'password': '',#密码
        'partnerFlag': 'false',  # 需要加入小伙伴则置为true,不用则为false。如果加入小伙伴则与小伙伴相关的内容都需要填写，并且正确！
        'partnerNum': '',#小伙伴学号
        'partnerName': '',#小伙伴的姓名,一定要和学号匹配！否则程序无法正常运行
        'wanna_room': '1',  # 1二楼南，2南楼北，3三楼北，4三楼南
        'wanna_seat': '99',  # 自己想要的位置
        'startTime': '9',  #想要开始的时间
        'partnerWannaSeat': '88',  # 小伙伴想要的位置
        'wanna_duration': '13',  # 想要在自习室待多久
        # 以上内容需要自己填写
        'name': 'john',
        'cookie': '',
        'year': '9012',
        'month': '9',   
        'day': '9',
        # 'bookUserNum': '1',
        'id': '0',
        'partnerID': '-1',
    }
    # myPrint('create_json_file: {}'.format(CZ_Data))
    json.dump(CZ_Data, file, ensure_ascii=False)
    file.close()
    file = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    myPrint('create_json_file: {}'.format(s))
    file.close()

# 获取Cookies
def Get_cookie():
    file = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    if(s['cookie'] != '-1'):
        if(judge_Apply_New_Cookie() == False):
            cookie_json = Read_File_json()
            cookie = cookie_json['cookie']
            return cookie
    cookie = save_cookie_to_file()
    return cookie

# 获取现在的日期，返回的形式是YEAR、MONTH、DAY
def get_now_datetime():
    d = datetime.datetime.now()
    year = int(str(d)[:4])
    month = int(str(d)[5:7])
    day = int(str(d)[8:10])
    return year, month, day

# 获取现在的日期，返回的形式是HOUR、MINIUTE、SECONDS
def GetNowHourMinSec():
    d = datetime.datetime.now()
    hour = int(str(d)[11:13])
    miniute = int(str(d)[14:16])
    seconds = int(str(d)[17:19])
    return hour, miniute,seconds

# 从配置文件获取修改的时间
def get_ApplyTime_from_File():
    file = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    year = s['year']
    month = s['month']
    day = s['day']
    file.close()
    return int(year), int(month), int(day)

# 将修改时间储存至文件内
def save_Apply_Time_to_File():
    year, month, day = get_now_datetime()
    file = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    file.close()
    file = open('test.json', 'w', encoding='utf-8-sig')
    s['year'] = year
    s['month'] = month
    s['day'] = day
    json.dump(s, file, ensure_ascii=False)
    file.close()

# 将cookies储存到文件中
def save_cookie_to_file(Login_requests='-1'):
    if(Login_requests == '-1'):
        Login_requests = get_user_Info()
    Login_requests.json()
    file = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    file.close()
    file = open('test.json', 'w', encoding='utf-8-sig')
    cookies = Login_requests.cookies
    true_cookie = ''
    for cookie in cookies:
        temp_len = len(' for jxnu.huitu.zhishulib.com/>')
        true_cookie += str(cookie)[7:-temp_len] + ';'
    true_cookie = true_cookie[1:-1]
    s['cookie'] = true_cookie
    json.dump(s, file, ensure_ascii=False)
    file.close()
    save_Apply_Time_to_File()
    return true_cookie

# 判断是否需要更新Cookies
def judge_Apply_New_Cookie():
    year, month, day = get_ApplyTime_from_File()
    applied_datetime = datetime.datetime(year, month, day)
    now_datetime = datetime.datetime.now()
    Interval_time = int((now_datetime - applied_datetime).total_seconds())
    if Interval_time < 29*3600*24:  # 当这个cookie的使用时间高于一个月则更新cookie
        return False
    myPrint('judge_Apply_New_Cookie: 需要更新cookie了！')
    return True

# 读取配置文件
def Read_File_json():
    file = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    file.close()
    return s

# 获取用户信息，用户姓名、ID等
def get_user_Info():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '299',
        'content-type': 'application/json',
        'Cookie': 'web_language=zh-CN',
        'Host': 'jxnu.huitu.zhishulib.com',
        'Origin': 'https://jxnu.huitu.zhishulib.com',
        'Referer': 'https://jxnu.huitu.zhishulib.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'
    }
    saved_json = Read_File_json()
    user_num = saved_json['usernum']
    user_password = saved_json['password']
    Login_Signature_requests = requests.get(
        'https://jxnu.huitu.zhishulib.com/User/Index/login?forward=/Seat/Index/searchSeats?space_category%5Bcategory_id%5D=591&space_category%5Bcontent_id%5D=36&LAB_JSON=1')
    Login_Signature_Json = Login_Signature_requests.json()
    Login_Signature_Json
    Login_code = Login_Signature_Json['content']['data']['code']
    Login_str = Login_Signature_Json['content']['data']['str']
    payload = {
        "login_name": user_num,
        "password": user_password,
        "code": Login_code,
        "str": Login_str
    }
    Login_requests = requests.post(
        'https://jxnu.huitu.zhishulib.com/api/1/login', headers=headers, data=json.dumps(payload))
    return Login_requests

# 获取同伴的ID
def get_partnerID(name,stu_num):
    myPrint("get_partnerID: ")
    search_user_id_content = {'name': name, 'student_number': stu_num}
    search_user_id_request = requests.post(
        'https://jxnu.huitu.zhishulib.com/User/Index/judgeNameStudentNumber?LAB_JSON=1', data=search_user_id_content, headers=get_headers())
    search_user_id_json = search_user_id_request.json()
    myPrint("\nget_partnerID:  partnerID{}".format(search_user_id_json['DATA']['user_id']))
    return search_user_id_json['DATA']['user_id']

# 更新配置文件
def renew_file_json():
    user_Info_request = get_user_Info()
    user_Info_json = user_Info_request.json()
    save_cookie_to_file(user_Info_request)  # 先将cookie保存至cookie，这样才能获取小伙伴的id，否则会报未登录的错误
    file = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    file.close()
    file = open('test.json', 'w', encoding='utf-8-sig')
    s['name'] = user_Info_json['name']
    s['id'] = user_Info_json['id']
    json.dump(s, file, ensure_ascii=False)
    file.close()
    if s['partnerFlag'] == 'true':
        s['partnerID'] = get_partnerID(s['partnerName'], s['partnerNum'])
    file = open('test.json', 'w', encoding='utf-8-sig')
    json.dump(s, file, ensure_ascii=False)
    file.close()
    save_Apply_Time_to_File()

# 初始化系统
def init_book():
    if(os.path.exists('install.lock') != True):
        create_json_file()
        renew_file_json()
        open('install.lock', 'w')
    headers = get_headers()
    return headers

# 获取真正的自习室ID
def get_true_start_seat_num(room):
    return {
        1: 36,
        2: 35,
        3: 31,
        4: 37,
    }[room]

# 计算开始时间
def cal_begin_time(flag=0, time=9): #这个flag用于标志是预约今天的位置还是明天的。0：今天；其他：明天。
    must_seconds = 3600
    d1 = datetime.datetime(1970, 1, 1)
    # if(d2 == 0):
    d2 = datetime.datetime.now()
    date = d2-d1
    date = int(date.days)
    date = date*3600*24 + must_seconds*(time - 8)
    if flag == 0:
        date += must_seconds*24
    return date

# 获取响应头
def get_headers():
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Cookie': Get_cookie()
               }
    return headers

# 查找位置ID
def search_seats(beginTime, wanna_seat=0, duration=9, content_id=36, num=1, category_id=591):
    paired_seat = 0
    # seat_state = 0
    headers = get_headers()
    search_seat_content = {'beginTime': beginTime, 'duration': duration, 'num': num,
                           'space_category[category_id]': category_id, 'space_category[content_id]': content_id}
    search_seats_request = requests.post(
        'https://jxnu.huitu.zhishulib.com/Seat/Index/searchSeats?LAB_JSON=1', data=search_seat_content, headers=headers)
    search_seats_json = search_seats_request.json()
    if(wanna_seat == 0):
        paired_seat = search_seats_json['data']['bestPairSeats']['seats'][0]['id']
        # seat_state = search_seats_json['data']['bestPairSeats']['seats'][0]['title']
    else:
        paired_seat = search_seats_json['data']['POIs'][-wanna_seat]['id']
        # seat_state = search_seats_json['data']['POIs'][-wanna_seat]['state']
    return int(paired_seat)

# 查找用户ID
def search_user_id(name, stu_num):
    headers = get_headers()
    search_user_id_content = {'name': name, 'student_number': stu_num}
    search_user_id_request = requests.post(
        'https://jxnu.huitu.zhishulib.com/User/Index/judgeNameStudentNumber?LAB_JSON=1', data=search_user_id_content, headers=headers)
    search_user_id_json = search_user_id_request.json()
    return search_user_id_json['DATA']['user_id']

# 发送位置预约的请求
def send_book_seat_requests(book_seat_content, headers):
    try:
        myPrint('send_book_seat_requests: sending request ')
        reqS = requests.Session()
        book_seat_request = reqS.post('https://jxnu.huitu.zhishulib.com/Seat/Index/bookSeats?LAB_JSON=1', data=book_seat_content, headers=headers, timeout=3.2)
        return True, book_seat_request
    except:
        myPrint('send_book_seat_requests: timeout ')
        return False, None

# 预约位置，根据状态不同进行相应的操作
def book_seat(beginTime, seat_id=26267, seatBookers_id=60000, duration=3600*3): 
    headers = get_headers()
    flag = 0 # 已有预约的标记
    times = 0 # 请求发送次数的计数器
    book_seat_state = 'fail'
    book_seat_msg = '搞事情'
    Hour,Mins,Secs = GetNowHourMinSec()
    while Hour != 21 or Mins != 59 or Secs != 59: # 只要还没有到21：59：59那就一直休息
        Hour,Mins,Secs = GetNowHourMinSec()
        time.sleep(0.5)
    book_seat_content = {'beginTime': beginTime, 'duration': duration, 'seats[0]': seat_id, 'seatBookers[0]': seatBookers_id} # 拼装数据字典
    request_state, book_seat_request = send_book_seat_requests(book_seat_content, headers) # 发送请求
    looptimes = 0 # 用于记录位置尝试的次数
    while(book_seat_state == 'fail' and looptimes <= 12): # 如果没有预约成功b并且尝试次数小于13次则继续尝试
        times = 0 # 用于记录发送请求的次数，因为经常会timeout，所以需要记录这个的次数。
        book_seat_content = {'beginTime': beginTime, 'duration': duration, 'seats[0]': seat_id, 'seatBookers[0]': seatBookers_id}
        request_state, book_seat_request = send_book_seat_requests(book_seat_content, headers)
        while request_state == False or book_seat_request.status_code != 200: # 如果请求没有发送成功或者对方服务器崩溃就一直请求
            times = times + 1
            request_state, book_seat_request = send_book_seat_requests(book_seat_content, headers)
            if(times == 60):
                break
        try:
            book_seat_request_json = book_seat_request.json()
            book_seat_state = book_seat_request_json['DATA']['result']
            book_seat_msg = book_seat_request_json['DATA']['msg']
            looptimes += 1
            if('已有的预约' in book_seat_msg): # 已有预约表明已经有了位置，则强制中断。
                flag = 1
                book_seat_msg, book_seat_state = '安排上了', "true"
                myPrint('book_seat: 为{} 尝试了{}次'.format(seatBookers_id, looptimes))
                break
            if('已被加入黑名单' in book_seat_request_json['DATA']['msg']): # 忘记签到被拉黑了直接结束本次任务！
                book_seat_msg, book_seat_state = book_seat_request_json['DATA']['msg'], 'fail'
                break
            if('选择的位置无法预约' in book_seat_msg): # 位置被占了就尝试下一个位置
                book_seat_state = 'fail'
                seat_id -= 1
        except:
            book_seat_state = 'fail'
            pass
        myPrint('book_seat: 为{} 尝试了{}次'.format(seatBookers_id, looptimes))
        myPrint('book_seat: 反馈信息如下：{} 现在开始尝试这个位置：{}'.format(book_seat_request_json['DATA']['msg'], seat_id))
    if(book_seat_state == 'fail' and flag != 1): # 尝试了60次，依旧没能成功预约上
        book_seat_state = 'fail'
        try:
            book_seat_msg = book_seat_request_json['DATA']['msg'] + ', 都尝试过了'
        except:
            book_seat_msg = '很抱歉的通知你，我真的努力了，奈何大家的学习热情真的太高了，我。。。没能帮你抢到位置，所以自己再去捡漏吧。'
    myPrint('book_seat :为{} 尝试了{}个位置'.format(seatBookers_id, looptimes))
    return book_seat_msg, book_seat_state

# 和同伴一起抢位置
def book_seat_withPartner(beginTime, seat_id=26267, seatBookers_id=60000, duration=3600*3,partnerID=0,partnerWannaSeat=0): #小伙伴功能因为没有尝试的机会，所以结束条件什么的都可能会有问题，自己小心尝试吧。
    headers = get_headers()
    flag = 0 # 已有预约的标记
    times = 0 # 请求发送次数的计数器
    book_seat_state = 'fail'
    book_seat_msg = '搞事情'
    Hour,Mins,Secs = GetNowHourMinSec()
    while Hour != 21 or Mins != 59 or Secs != 59: # 只要还没有到21：59：59那就一直休息
        Hour,Mins,Secs = GetNowHourMinSec()
        time.sleep(0.5)
    book_seat_content = {'beginTime': beginTime, 'duration': duration, 'seats[0]': seat_id, 'seatBookers[0]': seatBookers_id,'seats[1]':partnerWannaSeat,'seatBookers[1]':partnerID}
    request_state, book_seat_request = send_book_seat_requests(book_seat_content, headers)
    looptimes = 0 # 用于记录位置尝试的次数
    while(book_seat_state == 'fail' and looptimes <= 12): # 如果没有预约成功b并且尝试次数小于13次则继续尝试
        times = 0 # 用于记录发送请求的次数，因为经常会timeout，所以需要记录这个的次数。
        request_state, book_seat_request = send_book_seat_requests(book_seat_content, headers)
        while request_state == False or book_seat_request.status_code != 200: # 如果请求没有发送成功或者对方服务器崩溃就一直请求
            times = times + 1
            request_state, book_seat_request = send_book_seat_requests(book_seat_content, headers)
            if(times == 60):
                break
        try:
            book_seat_request_json = book_seat_request.json()
            book_seat_state = book_seat_request_json['DATA']['result']
            book_seat_msg = book_seat_request_json['DATA']['msg']
            looptimes += 1
            if('已有的预约' in book_seat_msg): # 已有预约表明已经有了位置，则强制中断。
                flag = 1
                book_seat_msg, book_seat_state = '安排上了', "true"
                myPrint('book_seat: 为{} 尝试了{}次'.format(seatBookers_id, looptimes))
                break
            if('已被加入黑名单' in book_seat_request_json['DATA']['msg']): # 忘记签到被拉黑了直接结束本次任务！
                book_seat_msg, book_seat_state = book_seat_request_json['DATA']['msg'], 'fail'
                break
            if('选择的位置无法预约' in book_seat_msg): # 位置被占了就尝试下一个位置
                book_seat_state = 'fail'
                seat_id -= 1
        except:
            book_seat_state = 'fail'
            pass
        myPrint('book_seat: 为{} 尝试了{}次'.format(seatBookers_id, looptimes))
        myPrint('book_seat: 反馈信息如下：{} 现在开始尝试这个位置：{}'.format(book_seat_request_json['DATA']['msg'], seat_id))
    if(book_seat_state == 'fail' and flag != 1): # 尝试了60次，依旧没能成功预约上
        book_seat_state = 'fail'
        try:
            book_seat_msg = book_seat_request_json['DATA']['msg'] + ', 都尝试过了'
        except:
            book_seat_msg = '很抱歉的通知你，我真的努力了，奈何大家的学习热情真的太高了，我。。。没能帮你抢到位置，所以自己再去捡漏吧。'
    myPrint('book_seat: 为{} 尝试了{}个位置'.format(seatBookers_id, looptimes))
    return book_seat_msg, book_seat_state

# 向Server酱发送消息以进行消息通知
def send_msg(msg='快来见抢座位程序最后一面啦~', state='false'):
    r = requests.post('https://sc.ftqq.com/{}.send?text=位置预约系统的来信&desp={}'.format(Server酱的Token, msg))
    r = r.json()
    myPrint('send_msg: {}{}{}'.format(msg, r['errmsg'], state))
    return

#获取预约的位置具体信息
def get_booked_seat_info():
    try:
        headers = get_headers()
        temp = requests.get('https://jxnu.huitu.zhishulib.com/Seat/Index/myBookingList?LAB_JSON=1',headers = headers, timeout=3)
        a = temp.json()
    except:
        return 'TimeOut'
    seatNum = a['content']['defaultItems'][0]['seatNum']#位置
    roomName = a['content']['defaultItems'][0]['roomName']#自习室名
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(a['content']['defaultItems'][0]['time'])))#开始时间
    endTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(a['content']['defaultItems'][0]['time'])+int(a['content']['defaultItems'][0]['duration'])))#结束时间
    html_content = '''
    <p>您预约的位置信息如下：</p>
    <p>自习室名称：{}</p>
    <p>座号：{}</p>
    <p>开始时间：{}</p>
    <p>结束时间：{}</p>
    <p>记得定好闹钟哦！</p>
    '''.format(str(roomName), str(seatNum), str(startTime),str(endTime))
    return html_content

# 抢位置的前序管理
def job():
    myPrint("job: I'm working...")
    file_json_info = Read_File_json()
    BeginTime = cal_begin_time(0,int(file_json_info['startTime']))
    # BeginTime = cal_begin_time(1,int(file_json_info['startTime'])) #如果需要预约今天的位置就注释上一行，用这一行
    # myPrint(BeginTime, file_json_info['startTime'])
    wanna_duration = 3600*int(file_json_info['wanna_duration'])
    seat_id = int(search_seats(BeginTime, int(file_json_info['wanna_seat']),wanna_duration,get_true_start_seat_num(int(file_json_info['wanna_room']))))
    partnerFlag = file_json_info['partnerFlag']
    if partnerFlag == 'true':
        myPrint("job: with_partner\n")
        partnerID = file_json_info['partnerID']
        partnerWannaSeat = search_seats(BeginTime, int(file_json_info['partnerWannaSeat']), wanna_duration, get_true_start_seat_num(int(file_json_info['wanna_room'])))
        # myPrint(partnerWannaSeat, '有小伙伴')
        book_seat_msg, book_seat_state = book_seat_withPartner(BeginTime, seat_id, file_json_info['id'], wanna_duration,partnerID,partnerWannaSeat)
    else:
        # myPrint('没小伙伴')
        book_seat_msg, book_seat_state = book_seat(BeginTime, seat_id, file_json_info['id'], wanna_duration)
    send_msg(book_seat_msg, book_seat_state)

# schedule函数，用于定时启动
# schedule.every().day.at("21:59").do(job)

# 主函数
if __name__ == "__main__":
    init_book()
    myPrint('__main__: 滴滴滴，开始给你盯着位置啦！')
    while True:
        # schedule.run_pending()
        # time.sleep(1)
        Hour,Mins,Secs = GetNowHourMinSec()
        if Hour == 21 and Mins == 59:
            myPrint('__main__: 开始预约')
            try: # 增加try可以防止出现意外而导致程序意外退出。
                job()
            except:
                myPrint('__main__: 预约失败')
                pass
        time.sleep(5)
    # job()
    #如果想要测试这个程序，就把上面这个while循环注释了，然后job()取消注释，在bookseat/bookseatwithpartner这两个函数中的time.sleep(60.3)给相应的注释了。
    #这样就可以立马测试程序而不需要等待到晚上。