#!/usr/bin/env python3
#
# This file is part of rsp_robot_hat_v3.
# Copyright (C) 2021 Hiwonder Ltd. <support@hiwonder.com>
#
# rsp_robot_hat_v3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rsp_robot_hat_v3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# title           :__main__.py
# author          :Hiwonder, LuYongping(Lucas)
# date            :20210205
# notes           :
# ==============================================================================


import sys
import time
from . import buzzer
from . import pwm_servo
from . import serial_servo


def set_buzzer(args):
    buzzer.set_state(int(args[1]))


def test_buzzer(args):
    while True:
        try:
            buzzer.set_state(1)
            time.sleep(0.5)
            buzzer.set_state(0)
            time.sleep(0.5)
        except KeyboardInterrupt:
            buzzer.set_state(0)
            break


def test_pwm_servo(args):
    while True:
        try:
            pwm_servo.servo1.set_position(1000, 1000)
            pwm_servo.servo2.set_position(2000, 1000)
            time.sleep(1.5)
            pwm_servo.servo1.set_position(2000, 1000)
            pwm_servo.servo2.set_position(1000, 1000)
            time.sleep(1.5)
        except KeyboardInterrupt:
            break


def set_pwm_servo(args):
    id_, pos, dur = list(map(int, args[1:]))
    servo = [pwm_servo.servo1, pwm_servo.servo2][id_ - 1]
    servo.set_position(pos, dur)
    time.sleep(dur / 1000 + 0.1)


def test_serial_servo(args):
    while True:
        try:
            serial_servo.set_position(1, 250, 1000)
            serial_servo.set_position(2, 750, 1000)
            time.sleep(1.5)
            serial_servo.set_position(1, 750, 1000)
            serial_servo.set_position(2, 250, 1000)
            time.sleep(1.5)
        except KeyboardInterrupt:
            break


test_list = dict(set_buzzer=set_buzzer,
                 test_buzzer=test_buzzer,
                 set_pwm_servo=set_pwm_servo,
                 test_pwm_servo=test_pwm_servo,
                 test_serial_servo=test_serial_servo)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] in test_list:
        test_list[sys.argv[1]](sys.argv[1:])
