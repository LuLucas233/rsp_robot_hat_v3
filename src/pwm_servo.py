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
# title           :pwm_servo.py
# author          :Hiwonder
# date            :20210205
# notes           : request pigpio library
# ==============================================================================

import threading
import pigpio


class PwmServo:
    def __init__(self, pi, pin, min_width=50, max_width=2500, deviation=0):
        self.pi = pi
        self.pin = pin

        self.min_width = min_width
        self.max_width = max_width
        self.deviation = deviation
        self.inc_times = 0
        self.pos_cur = 1500
        self.pos_set = self.pos_cur
        self.pos_inc = 0
        self.lock = threading.Lock()
        self.update_timer = threading.Timer(0.02, self.update_pos_task)
        self.update_timer.start()

    def get_position(self):
        """
        :return:
        """
        return self.pos_cur

    def set_position(self, new_pos, duration=0):
        """
        :param new_pos:
        :param duration:
        :return:
        """
        if not self.min_width <= new_pos <= self.max_width:
            raise ValueError("new position out of pulse width range")
        new_pos = int(new_pos)
        if duration < 0:
            raise ValueError("duration must be not less than 0")
        elif duration == 0:
            with self.lock:
                self.pos_set = new_pos
                self.pos_cur = new_pos
                self.pi.set_servo_pulsewidth(self.pin, self.pos_cur + self.deviation)
        else:
            duration = 20 if duration < 20 else duration
            duration = 30000 if duration > 30000 else duration
            inc_times = int(duration / 20 + 0.5)
            with self.lock:
                self.inc_times = inc_times
                self.pos_set = new_pos
                self.pos_inc = (self.pos_cur - new_pos) / inc_times

    def update_pos_task(self):
        """
        :return:
        """
        self.update_timer = threading.Timer(0.02, self.update_pos_task)
        self.update_timer.start()
        with self.lock:
            self.inc_times -= 1
            if self.inc_times > 0:
                pos_cur = self.pos_set + int(self.pos_inc * self.inc_times)
                self.pi.set_servo_pulsewidth(self.pin, pos_cur + self.deviation)
                self.pos_cur = pos_cur
            elif self.inc_times == 0:
                self.pi.set_servo_pulsewidth(self.pin, self.pos_set + self.deviation)
                self.pos_cur = self.pos_set
            else:
                self.inc_times = -1

    def set_deviation(self, new_deviation=0):
        """
        :param new_deviation:
        :return:
        """
        if not -300 < new_deviation < 300:
            raise ValueError("new deviation out range. it must be betweent -300~300")
        else:
            self.deviation = int(new_deviation)

    def get_deviation(self):
        """
        :return:
        """
        return self.deviation


_pi = pigpio.pi()
servo1 = PwmServo(_pi, 12)
servo2 = PwmServo(_pi, 13)
