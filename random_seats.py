import random
import json
import time
import schedule
import datetime

# 本脚本用于你坐某个位置腻了之后随机选择位置，本脚本会排除边上的位置以及靠近门口的位置，不过只适合二楼南，其他自习室自己修改。

def random_seats():
    line = random.randint(1,2)
    table = 1
    seats1=seats2=0
    if(line == 1):
        table = random.randint(1,34)
        seats = random.sample([3,4,5,6],2)
        seats1 = table*8+seats[0]
        # seats2 = table*8+seats[1]
    if(line == 2):
        table = random.randint(0,17)
        seats = random.sample([3,4,5,6,7,8,9,10],2)
        seats1 = table*12+272+seats[0]
        # seats2 = table*12+272+seats[1]
    # print('明日份惊喜：',seats1,seats2,datetime.datetime.now())
    print('明日份惊喜：',seats1,datetime.datetime.now())
    # return seats1,seats2
    return seats1

def renew_file_json_wanna_seat(wanna_seat,file_path):
    file = open(file_path,'r',encoding='utf-8-sig')
    s = json.load(file)
    file.close()
    file = open(file_path,'w',encoding='utf-8-sig')
    s['wanna_seat'] = wanna_seat
    json.dump(s,file,ensure_ascii=False)
    file.close()

def modify_wanna_seats():
    wanna_seats1 = 0
    banList = {0,8,18,239,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,129,130,131,132,133,134,135,136,265,266,267,268,269,270,271,272,415,416,405,406,407,408,409,410,411,412,413,414}
    while(wanna_seats1 in banList):
        wanna_seats1,wanna_seats2 = random_seats()
    path1 = 'test.json'
    renew_file_json_wanna_seat(wanna_seats1,path1)

schedule.every().day.at("21:50").do(modify_wanna_seats)

if __name__ == "__main__":
    print('骚起来',datetime.datetime.now())
    while True:
        schedule.run_pending()
        time.sleep(1)
    # modify_wanna_seats()
