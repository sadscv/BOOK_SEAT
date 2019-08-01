#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2019/07/07 18:26
@file: test_seatBooker.py

@desc: 
"""
from typing import Dict
from unittest import TestCase
from datetime import datetime

import pytz

from book_seat import SeatBooker


class TestSeatBooker(TestCase):
    def setUp(self):
        self.config = 'config.json'
        timezone = pytz.timezone('Asia/Shanghai')
        self.sb = SeatBooker(self.config, timezone)

    def test_init(self):
        self.sb.load_config('config.json')

    def test_renewal_date(self):
        self.sb.last_update = datetime.utcnow()
        renewal_date = datetime.strptime(self.sb.settings['last_update'],
                                         '%Y%m%d')
        self.assertEqual(renewal_date.date(), datetime.now().date())

    def test_load_config(self):
        config = self.sb.load_config(self.config)
        self.assertIsInstance(config, Dict)

    def test_update_config(self):
        item = 'month'
        value = -1
        self.sb.update_settings(item, value)
        self.assertEqual(self.sb.settings[item], -1)

    def test_need_update_cookie(self):
        # set `last_update` to enough long time ago.
        self.sb.last_update = datetime(1970, 1, 1)
        self.assertTrue(self.sb.need_refresh_cookie())

        # set `last_update` to current.
        self.sb.last_update = datetime.now()
        print(self.sb.last_update)
        self.assertFalse(self.sb.need_refresh_cookie())

    def test_refresh_cookie(self):
        self.assertIsNotNone(self.sb.refresh_cookie())

    def test_renew_settings(self):
        self.sb.renew_settings()
        import json
        with open('tmp.json', 'w+') as f:
            js = json.dumps(self.sb.settings, indent=4)
            f.write(js)

    def test_get_login_request(self):
        request = self.sb.send_login_request()
        self.assertEqual(request.status_code, 200)

    def test_get_user_id(self):
        # if u wanna pass this unittest,u should filling a real name and
        # student_id into following variable `name` and `s_id`
        pass
        name = self.sb.settings['name']
        s_id = self.sb.settings['usernum']
        self.assertIsInstance(self.sb.get_user_id(name, s_id), str)

    def test_start_time(self):
        self.sb.start_timestamp(hour=8)

    def test_search_seats(self):
        start_time = self.sb.start_timestamp(17)
        target_seat = None
        if self.sb.settings['wanna_seat']:
            target_seat = int(self.sb.settings['wanna_seat'])
        duration = 3600 * 1
        content_id = 35
        seat = self.sb.get_available_seat(
            begin_time=start_time,
            target_seat=target_seat,
            duration=duration,
            room_id=content_id
        )
        self.assertIsInstance(seat, int)

    def test_work(self):
        self.sb.work()

    def test_book_seat(self):
        begin_time = self.sb.start_timestamp(int(self.sb.settings['startTime']))
        duration = int(self.sb.settings['duration']) * 3600
        seat_id = 26786
        seatBookers_id = 85003
        content = {
            'beginTime': begin_time,
            'duration': duration,
            'seats[0]': seat_id,
            'seatBookers[0]': seatBookers_id
        }
        response = self.sb.book_seat_request(content)
        self.assertEqual(response.status_code, 200)

    def test_current_seat(self):
        seat = self.sb.current_seat()
        self.assertIsInstance(seat, str)
        # start = seat.startswith('<P>')
        # self.assertTrue(start)

