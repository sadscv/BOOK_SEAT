#import something
import datetime
import requests
import schedule
import random
import time
import json
import os

#本脚本由CZ制作，考研期间不喜欢抢位置，所以做了这个，考完之后加上了小伙伴的功能和四个自习室自由选择的功能，然后现在打算分享给大家，不要广为流传，自己默默用就好了=-=
#本脚本就是填好下面这些需要填的东西就好了，如果想要更改数据，就请停止这个脚本之后再删除同目录下的install.lock这个文件，之后再运行一遍这个脚本就好了，你还可以更改test.json这个文件，反正随便皮

def create_json_____():
    ____ = open('test.json', 'w', encoding='utf-8-sig')
    CZ_data = {
        'usernum': 'stuNum',#你的学号
        'password': 'ps',#你的密码
        'partnerFlag': 'true',  # 需要加入小伙伴则置为true，默认不需要小伙伴
        'partnerNum': 'partnerStuNum',#小伙伴的名字
        'partnerName': 'partnerName',#小伙伴的学号
        'wanna_room': '1',  # 1二楼南，2南楼北，3三楼北，4三楼南
        'wanna_seat': '66',  # 自己想要的位置
        'partnerWannaSeat': '88',  # 小伙伴想要的位置
        'wanna_duration': '13',  # 想要在自习室待多少小时。。。
        # 以上内容需要自己填写
        'name': 'john',
        'cookie': '',
        'year': '2018',
        'month': '8',
        'day': '26',
        # 'bookUserNum': '1',
        'id': '0',
        'partnerID': '-1',
    }
    print(CZ_data)
    json.dump(CZ_data, ____, ensure_ascii=False)
    ____.close()
    ____ = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(____)
    print(s)

def Get_cookie():
    ____ = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(____)
    if(s['cookie'] != '-1'):
        if(judge_Apply_New_Cookie() == False):
            cookie_json = Read______json()
            cookie = cookie_json['cookie']
            return cookie
    cookie = save_cookie_to_____()
    return cookie


def get_now_datetime():
    d = datetime.datetime.now()
    year = int(str(d)[:4])
    month = int(str(d)[5:7])
    day = int(str(d)[8:10])
    return year, month, day


def get_ApplyTime_from_____():
    ____ = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(____)
    year = s['year']
    month = s['month']
    day = s['day']
    ____.close()
    return int(year), int(month), int(day)


def save_Apply_Time_to_____():
    year, month, day = get_now_datetime()
    ____ = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(____)
    ____.close()
    ____ = open('test.json', 'w', encoding='utf-8-sig')
    s['year'] = year
    s['month'] = month
    s['day'] = day
    json.dump(s, ____, ensure_ascii=False)
    ____.close()


def save_cookie_to_____(Login_requests='-1'):
    if(Login_requests == '-1'):
        Login_requests = get_user_Info()
    Login_requests.json()
    ____ = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(____)
    ____.close()
    ____ = open('test.json', 'w', encoding='utf-8-sig')
    cookies = Login_requests.cookies
    true_cookie = ''
    for cookie in cookies:
        temp_len = len(' for jxnu.huitu.zhishulib.com/>')
        true_cookie += str(cookie)[7:-temp_len] + ';'
    true_cookie = true_cookie[1:-1]
    s['cookie'] = true_cookie
    json.dump(s, ____, ensure_ascii=False)
    ____.close()
    save_Apply_Time_to_____()
    return true_cookie


def judge_Apply_New_Cookie():
    year, month, day = get_ApplyTime_from_____()
    applied_datetime = datetime.datetime(year, month, day)
    now_datetime = datetime.datetime.now()
    Interval_time = int((now_datetime - applied_datetime).total_seconds())
    if Interval_time < 29*3600*24:
        return False
    return True


def Read______json():
    ____ = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(____)
    ____.close()
    return s


def get_user_Info():
    headers = {
        
        #自己探索

    }
    saved_json = Read______json()
    user_num = saved_json['usernum']
    user_password = saved_json['password']
    Login_Signature_requests = requests.get(
        'login?forwardAPI')
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
        'loginAPI', headers=headers, data=json.dumps(payload))
    return Login_requests

def get_partnerID(name,stu_num):
    print("get partnerID")
    search_user_id_content = {'name': name, 'student_number': stu_num}
    search_user_id_request = requests.post(
        'judgeNameStudentNumberAPI', data=search_user_id_content, headers=get_headers())
    search_user_id_json = search_user_id_request.json()
    print("\n partnerID",search_user_id_json['DATA']['user_id'])
    return search_user_id_json['DATA']['user_id']

def renew______json():
    user_Info_request = get_user_Info()
    user_Info_json = user_Info_request.json()
    ____ = open('test.json', 'r', encoding='utf-8-sig')
    s = json.load(____)
    ____.close()
    ____ = open('test.json', 'w', encoding='utf-8-sig')
    s['name'] = user_Info_json['name']
    s['id'] = user_Info_json['id']
    json.dump(s, ____, ensure_ascii=False)
    ____.close()
    if s['partnerFlag'] == 'true':
        s['partnerID'] = get_partnerID(s['partnerName'], s['partnerNum'])
    ____ = open('test.json', 'w', encoding='utf-8-sig')  # 不要更改这段否则你会后悔的
    json.dump(s, ____, ensure_ascii=False)
    ____.close()
    save_cookie_to_____(user_Info_request)
    save_Apply_Time_to_____()


def init_book():
    if(os.path.exists('install.lock') != True):
        create_json_____()
        renew______json()
        open('install.lock', 'w')
    headers = get_headers()
    return headers


def get_true_start_seat_num(room):
    return {
        1: 36,
        2: 35,
        3: 31,
        4: 37,
    }[room]


def cal_begin_time(d2=0, time=9):
    must_seconds = 3600
    d1 = datetime.datetime(1970, 1, 1)
    if(d2 == 0):
        d2 = datetime.datetime.now()
    date = d2-d1
    date = int(date.days)
    date = date*3600*24 + must_seconds*(time - 8) + must_seconds*24
    return date


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


def search_seats(beginTime, wanna_seat=0, duration=9, content_id=36, num=1, category_id=591):
    paired_seat = 0
    # seat_state = 0
    headers = get_headers()
    search_seat_content = {'beginTime': beginTime, 'duration': duration, 'num': num,
                           'space_category[category_id]': category_id, 'space_category[content_id]': content_id}
    search_seats_request = requests.post(
        'searchSeatsAPI', data=search_seat_content, headers=headers)
    search_seats_json = search_seats_request.json()
    if(wanna_seat == 0):
        paired_seat = search_seats_json['data']['bestPairSeats']['seats'][0]['id']
        # seat_state = search_seats_json['data']['bestPairSeats']['seats'][0]['title']
    else:
        paired_seat = search_seats_json['data']['POIs'][-wanna_seat]['id']
        # seat_state = search_seats_json['data']['POIs'][-wanna_seat]['state']
    return int(paired_seat)


def search_user_id(name, stu_num):
    headers = get_headers()
    search_user_id_content = {'name': name, 'student_number': stu_num}
    search_user_id_request = requests.post(
        'judgeNameStudentNumberAPI', data=search_user_id_content, headers=headers)
    search_user_id_json = search_user_id_request.json()
    return search_user_id_json['DATA']['user_id']


def send_book_seat_requests(book_seat_content, headers):
    try:
        print('sending request ', datetime.datetime.now())
        book_seat_request = requests.post(
            'bookSeatAPI', data=book_seat_content, headers=headers, timeout=2)
        return True, book_seat_request
    except:
        print('timeout ', datetime.datetime.now())
        return False, None


def book_seat(beginTime, seat_id=0, seatBookers_id=0, duration=3600*3):
    headers = get_headers()
    flag = 0
    times = 0
    book_seat_state = 'f'
    book_seat_msg = '搞事情'
    time.sleep(60.3)
    book_seat_content = {'beginTime': beginTime, 'duration': duration,
                         'seats[0]': seat_id, 'seatBookers[0]': seatBookers_id}
    request_state, book_seat_request = send_book_seat_requests(
        book_seat_content, headers)
    while request_state == False or book_seat_request.status_code != 200:
        times = times + 1
        time.sleep(1)
        request_state, book_seat_request = send_book_seat_requests(
            book_seat_content, headers)
        print(times, '次尝试 ', datetime.datetime.now())
        if(times == 20):
            break
    book_seat_request_json = book_seat_request.json()
    looptimes = 1
    while(book_seat_request_json['DATA']['result'] == 'fail' and looptimes <= 10):
        print(book_seat_request_json['DATA']['msg'],
              '\n现在开始尝试备用位置', datetime.datetime.now())
        times = 0
        seat_id -= 0 if looptimes % 3 != 0 else 1
        book_seat_content = {'beginTime': beginTime, 'duration': duration,
                             'seats[0]': seat_id, 'seatBookers[0]': seatBookers_id}
        request_state, book_seat_request = send_book_seat_requests(
            book_seat_content, headers)
        while request_state == False or book_seat_request.status_code != 200:
            times = times + 1
            time.sleep(1)
            request_state, book_seat_request = send_book_seat_requests(
                book_seat_content, headers)
            print(times, '次尝试 ', datetime.datetime.now())
            if(times == 20):
                break
        book_seat_request_json = book_seat_request.json()
        book_seat_state = book_seat_request_json['DATA']['result']
        time.sleep(0.3)
        looptimes += 1
        try:
            if('已有的预约' in book_seat_request_json['DATA']['msg']):
                flag = 1
                break
        except:
            continue
        if(book_seat_state == 'fail' and flag != 1):
            book_seat_msg = book_seat_request_json['DATA']['msg'] + \
                ','+'都尝试过了，还是被占了'
    if(book_seat_request_json['DATA']['result'] != 'false' or flag == 1):
        book_seat_msg, book_seat_state = '安排上了', "true"
    return book_seat_msg, book_seat_state

def book_seat_withPartner(beginTime, seat_id=0, seatBookers_id=0, duration=3600*3,partnerID=0,partnerWannaSeat=0):
    #为了效率考虑才复制了上面那个函数，所以不要自作聪明
    headers = get_headers()
    flag = 0
    times = 0
    book_seat_state = 'f'
    book_seat_msg = '搞事情'
    time.sleep(60.3)
    #这个sleep时间自己调到最合适的
    book_seat_content = {'beginTime': beginTime, 'duration': duration,
                        'seats[0]': seat_id, 'seatBookers[0]': seatBookers_id,'seats[1]':partnerWannaSeat,'seatBookers[1]':partnerID}
    request_state, book_seat_request = send_book_seat_requests(
        book_seat_content, headers)
    while request_state == False or book_seat_request.status_code != 200:
        times = times + 1
        time.sleep(1)
        request_state, book_seat_request = send_book_seat_requests(
            book_seat_content, headers)
        print(times, '次尝试 ', datetime.datetime.now())
        if(times == 20):
            break
    book_seat_request_json = book_seat_request.json()
    looptimes = 1
    while(book_seat_request_json['DATA']['result'] == 'fail' and looptimes <= 10):
        print(book_seat_request_json['DATA']['msg'],
              '\n现在开始尝试备用位置', datetime.datetime.now())
        times = 0
        seat_id -= 0 if looptimes % 3 != 0 else 1
        partnerWannaSeat -= 0 if looptimes % 3 != 0 else 1
        book_seat_content = {'beginTime': beginTime, 'duration': duration,
                           'seats[0]': seat_id, 'seatBookers[0]': seatBookers_id}
        request_state, book_seat_request = send_book_seat_requests(
            book_seat_content, headers)
        while request_state == False or book_seat_request.status_code != 200:
            times = times + 1
            time.sleep(1)
            request_state, book_seat_request = send_book_seat_requests(
                book_seat_content, headers)
            print(times, '次尝试 ', datetime.datetime.now())
            if(times == 20):
                break
        book_seat_request_json = book_seat_request.json()
        book_seat_state = book_seat_request_json['DATA']['result']
        time.sleep(0.3)
        looptimes += 1
        try:
            if('已有的预约' in book_seat_request_json['DATA']['msg']):
                flag = 1
                break
        except:
            continue
        if(book_seat_state == 'fail' and flag != 1):
            book_seat_msg = book_seat_request_json['DATA']['msg'] + \
                ','+'都尝试过了，还是被占了'
    if(book_seat_request_json['DATA']['result'] != 'false' or flag == 1):
        book_seat_msg, book_seat_state = '安排上了', "true"
    return book_seat_msg, book_seat_state


def send_msg(msg='快来见抢座位程序最后一面啦~', state='false'):
    r = requests.post(
        'https://sc.ftqq.com/token.send?text='+msg)#此次加入通知，可以去了解一下这个微信推送的方式！直接替换token就行了
    r = r.json()
    print(msg, r['errmsg'], state, datetime.datetime.now())


def job():
    print("I'm working...", datetime.datetime.now())
    _____json_info = Read______json()
    BeginTime = cal_begin_time()
    wanna_duration = 3600*int(_____json_info['wanna_duration'])
    seat_id = search_seats(BeginTime, int(_____json_info['wanna_seat']),wanna_duration,get_true_start_seat_num(int(_____json_info['wanna_room'])))
    print(seat_id)
    seat_id = int(seat_id)
    partnerFlag = _____json_info['partnerFlag']
    if partnerFlag == 'true':
        partnerID = _____json_info['partnerID']
        partnerWannaSeat = search_seats(BeginTime, int(
            _____json_info['partnerWannaSeat']), wanna_duration, get_true_start_seat_num(int(_____json_info['wanna_room'])))
        book_seat_msg, book_seat_state = book_seat_withPartner(
            BeginTime, seat_id, _____json_info['id'], wanna_duration,partnerID,partnerWannaSeat)
    else:
        book_seat_msg, book_seat_state = book_seat_withPartner(
            BeginTime, seat_id, _____json_info['id'], wanna_duration)
    send_msg(book_seat_msg, book_seat_state)


schedule.every().day.at("21:59").do(job)

if __name__ == "__main__":
    init_book()
    print('滴滴滴，开始给你盯着位置啦！', datetime.datetime.now())
    while True:
        schedule.run_pending()
        time.sleep(1)
    # job()
