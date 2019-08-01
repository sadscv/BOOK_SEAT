import logging
from datetime import datetime, timedelta
import json
import time
from typing import Dict

import pytz
import requests
import schedule
from requests import Response


class SeatBooker(object):
    MAX_TIMES = 10

    def __init__(self, path, tz):
        self.logger = logging.getLogger(__name__)
        self.tz = tz
        self.settings = self.load_config(path)
        self.renew_settings()

    def get_cookie(self):
        self.logger.debug('calling function')
        if 'cookies' not in self.settings:
            return self.refresh_cookie()
        if self.settings['cookies'] and self.need_refresh_cookie():
            return self.refresh_cookie()
        return self.settings['cookies']

    def refresh_cookie(self, login_response: Response = None):
        """
        fetch cookie and save it into self.settings['cookie']
        """
        self.logger.debug('calling function')
        if not login_response:
            login_response = self.send_login_request()
        cookies = login_response.cookies
        true_cookie = ''
        for cookie in cookies:
            # e.g. <Cookie org_id=101 for jxnu.huitu.zhishulib.com/>
            temp_len = len(' for jxnu.huitu.zhishulib.com/>')
            true_cookie += str(cookie)[8:-temp_len] + ';'
        self.update_settings('cookies', true_cookie)
        self.update_settings(
            'last_update', datetime.now().strftime('%Y%m%d'))
        return true_cookie

    # 获取Cookies
    def need_refresh_cookie(self) -> bool:
        """
        """
        self.logger.debug('calling function')
        if self.last_update:
            last_update = datetime.strptime(self.last_update, '%Y%m%d')
            update_interval = (datetime.now() - last_update).days
            if update_interval >= 29:
                self.logger.info('需要更新cookie了！')
                return True
            else:
                return False
        if not self.last_update:
            self.logger.info('missing `last_update` in settings,need refresh '
                             'cookie')
            return True

    @property
    def last_update(self):
        if 'last_update' not in self.settings:
            return False
        return self.settings['last_update']

    @last_update.setter
    def last_update(self, dt: datetime):
        self.update_settings('last_update', dt.strftime('%Y%m%d'))

    def send_login_request(self) -> Response:
        """
        get the required `code` and `str` from login page,
        then POST request with our composed payload.
        """
        self.logger.debug('calling function')
        login_name = self.settings['usernum']
        password = self.settings['password']

        login_signature_response = requests.get(
            'https://jxnu.huitu.zhishulib.com/User/Index/login?forward=/Seat'
            '/Index/searchSeats?space_category%5Bcategory_id%5D=591'
            '&space_category%5Bcontent_id%5D=36&LAB_JSON=1')
        data = login_signature_response.json()['content']['data']
        payload = {
            "login_name": login_name,
            "password": password,
            "code": data['code'],
            "str": data['str']
        }
        login_response = requests.post(
            'https://jxnu.huitu.zhishulib.com/api/1/login',
            headers=self.get_headers(),
            data=json.dumps(payload)
        )
        return login_response

    # 获取响应头
    def renew_settings(self) -> bool:
        """
        fetch some user's info and save them into `self.settings`
        """
        self.logger.debug('calling function')
        login_response = self.send_login_request()
        data = login_response.json()
        # 先将cookie保存至cookie，这样才能获取小伙伴的id，否则会报未登录的错误
        self.refresh_cookie(login_response)
        self.update_settings('name', data['name'])
        self.update_settings('id', data['id'])

        # if book seat with partner together, we should also fetch partner_id
        if self.settings['partnerFlag']:
            partner_id = self.get_user_id(
                self.settings['partnerName'],
                self.settings['partnerNum'])
            self.update_settings('partnerID', partner_id)
        return True

    def get_user_id(self, name: str, stu_num: str) -> str:
        """
        get user_id(in the system) by given student's name and number.
        """
        user_id_request = requests.post(
            'https://jxnu.huitu.zhishulib.com/User/Index/judgeNameStudentNumber'
            '?LAB_JSON=1',
            data={'name': name, 'student_number': stu_num},
            headers=self.get_headers(with_cookie=True)
        )
        user_id = user_id_request.json()['DATA']['user_id']
        return user_id

    def get_headers(self, with_cookie=None) -> Dict:
        self.logger.debug('calling function')
        headers = {
            # 'accept': 'application/json, text/plain, */*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'Connection': 'keep-alive',
            # 'Content-Length': '299',
            # 'content-type': 'application/json',
            'Cookie': self.get_cookie() if with_cookie else None,
            # 'Host': 'jxnu.huitu.zhishulib.com',
            # 'Origin': 'https://jxnu.huitu.zhishulib.com',
            # 'Referer': 'https://jxnu.huitu.zhishulib.com/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 '
                          'Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/68.0.3440.75 Mobile '
                          'Safari/537.36 '
        }
        return headers

    def get_available_seat(self, begin_time: int, room_id: int, duration: int,
                           target_seat: int = None) -> int:
        """
        fetch the available seat number through API by given conditions.
        """
        self.logger.debug('calling function')
        headers = self.get_headers(with_cookie=True)
        search_seat_content = {
            'beginTime': begin_time,
            'duration': duration,
            'seat[0]': target_seat,
            'space_category[content_id]': room_id
        }
        search_seats_request = requests.post(
            'https://jxnu.huitu.zhishulib.com/Seat/Index/searchSeats?LAB_JSON=1',
            data=search_seat_content, headers=headers)
        response = search_seats_request.json()
        print(response)
        if 'data' not in response:
            self.logger.info('没有符合条件的座位预约')
            return False
        available_seats = response['data']['bestPairSeats']['seats']
        if available_seats:
            if target_seat:
                for seat in available_seats:
                    if str(target_seat) == seat['title']:
                        return int(seat['id'])
            self.logger.info('target_seat had been booked during given period')
            return int(available_seats[0]['id'])
        return False

    @staticmethod
    def start_timestamp(hour: int) -> int:
        """
        Return the timestamp of given hour at today,if begin_time is earlier
        than now. we should return tomorrow's timestamp.
        """
        now = datetime.now()
        begin_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if now > begin_time:
            begin_time = begin_time + timedelta(days=1)
        return int(begin_time.timestamp())

    @staticmethod
    def get_room_id(room: int) -> int:
        return {
            1: 36,
            2: 35,
            3: 31,
            4: 37,
        }[room]

    def work(self):
        self.logger.info("I'm working...")
        start_time = self.start_timestamp(int(self.settings['startTime']))
        print('begin_time:', start_time, self.settings['startTime'])
        duration = 3600 * int(self.settings['duration'])
        if self.settings['wanna_seat']:
            target_seat = int(self.settings['wanna_seat'])
        else:
            target_seat = None
        seat_id = self.get_available_seat(
            begin_time=start_time,
            target_seat=target_seat,
            duration=duration,
            room_id=self.get_room_id(int(self.settings['wanna_room'])))

        print(seat_id)
        if not seat_id:
            self.logger.warning('no available seat in given period')
            return False

        partner_flag = self.settings['partnerFlag']
        if not partner_flag:
            book_result = self.book_seat(
                start_time, seat_id, self.settings['id'], duration)
        else:
            self.logger.info('book seat with partner')
            partner_id = self.settings['partnerID']
            partner_seat_id = self.get_available_seat(
                begin_time=start_time,
                target_seat=int(self.settings['partnerWannaSeat']),
                duration=duration,
                room_id=self.get_room_id(int(self.settings['wanna_room'])))
            kwargs = {
                'seatBookers[1]': partner_id,
                'seats[1]': partner_seat_id
            }
            book_result = self.book_seat(
                start_time, seat_id, self.settings['id'], duration,
                kwargs=kwargs)
        if book_result:
            self.logger.warning('seat booked, result:' + str(book_result))
            self.send_msg(book_result)

    # 抢位置
    def book_seat(self, begin_time, seat, seat_booker, duration, **kwargs):
        # 等待60.3秒，这个时间看电脑时间是否准确，我的服务器时间快了点，所以要多等一会。测试好这个时间可以提高成功率。
        # time.sleep(60.3)
        content = {
            'beginTime': begin_time,
            'duration': duration,
            'seats[0]': seat,
            'seatBookers[0]': seat_booker,
        }
        self.logger.info('booking seat with content:{}'.format(content))
        if kwargs:  # if **kwargs, we should append partner's info into `content`
            content = {**content, **kwargs}
        return self._book_seat(content)

    def _book_seat(self, content: dict):
        attempts = 0
        while attempts < self.MAX_TIMES:
            attempts += 1
            self.logger.debug('{}次尝试 '.format(attempts))
            try:
                print(content)
                response = self.book_seat_request(content)
            except requests.exceptions.ReadTimeout as e:
                self.logger.warning('book seat timeout', e)
                continue
            data = response.json()['DATA']
            if response.status_code != 200:
                continue
            # current seat had been used, try a smaller seat_id.
            if 'result' not in data:
                self.logger.warning('result not in book_seat_response data')
                break
            elif data['result'] == 'fail':
                # Todo: logic of following codes should be rewrite again,
                #  when `result` is `fail`, figure out which seat is
                #  unavailable, my seat or partner's seat.
                # @sadscv  19-7-27 下午9:02
                self.logger.info('{},现在开始尝试备用位置', data['msg'])
                content['seats[0]'] -= 1
                # if book seat with partner
                if 'seats[1]' in content:
                    content['seats[1]'] -= 1
                seat = self._book_seat(content)
                return seat
            elif data['result'] != 'fail':
                return content['seats[0]']
        return False

    def book_seat_request(self, book_seat_content: dict) -> Response:
        self.logger.info('calling function')
        headers = self.get_headers(with_cookie=True)
        book_seat_request = requests.post(
            'https://jxnu.huitu.zhishulib.com/Seat/Index/bookSeats?LAB_JSON=1',
            data=book_seat_content, headers=headers, timeout=2)
        return book_seat_request

    def send_msg(self, state):
        pass

    def current_seat(self):
        headers = self.get_headers(with_cookie=True)
        response = requests.get(
            'https://jxnu.huitu.zhishulib.com/Seat/Index/myBookingList'
            '?LAB_JSON=1', headers=headers, timeout=3)
        response_data = response.json()['content']['defaultItems'][0]
        seat_num = str(response_data['seatNum'])  # 位置
        room_name = str(response_data['roomName'])  # 自习室名
        start_time = datetime.fromtimestamp(int(response_data['time']))
        duration = timedelta(seconds=int(response_data['duration']))
        end_time = start_time + duration
        html_content = '''
        <p>您预约的位置信息如下：</p>
        <p>自习室名称：{}</p>
        <p>座号：{}</p>
        <p>开始时间：{}</p>
        <p>结束时间：{}</p>
        <p>记得定好闹钟哦！</p>
        '''.format(room_name, seat_num, start_time, end_time)
        return html_content

    @staticmethod
    def load_config(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 更新配置文件
    def update_settings(self, item, value):
        if item in self.settings:
            self.settings[item] = value
        else:
            self.logger.warning('{} not in config.json'.format(item))
            self.settings[item] = value
        return True


class CONFIG:
    def __init__(self):
        self.config = {
            "usernum": "",
            "password": "",
            "wanna_room": "",
            "wanna_seat": "",
            "startTime": "",
            "wanna_duration": "",

            "partnerFlag": "",
            "partnerID": "-1",
            "partnerName": "",
            "partnerNum": "",
            "partnerWannaSeat": ""
        }


if __name__ == "__main__":
    config_path = 'config.json'
    timezone = pytz.timezone('Asia/Shanghai')
    log_path = 'log/log.txt'
    logging.basicConfig(
        filename=log_path, filemode='w', level=logging.DEBUG,
        format='[%(asctime)s - %(levelname)-6s - %(name)+.8s - %(funcName)s]'
               ' : %(message)s')
    sb = SeatBooker(config_path, timezone)

    sb.work()
    # schedule.every().day.at("22:00").do(sb.work)
    print('滴滴滴，开始给你盯着位置啦！', datetime.now())
    while True:
        schedule.run_pending()
        time.sleep(1)
