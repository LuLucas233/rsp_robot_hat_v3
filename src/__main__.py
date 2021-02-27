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
# author          :Hiwonder
# date            :20210205
# notes           :
# ==============================================================================


import sys
import time
from rsp_robot_hat_v3 import buzzer


def test_buzzer():
    while True:
        try:
            buzzer.set_state(1)
            time.sleep(0.5)
            buzzer.set_state(0)
            time.sleep(0.5)
        except KeyboardInterrupt:
            buzzer.set_state(0)
            break


test_list = dict(test_buzzer=test_buzzer)

if __name__ == "__main__":
    print("test", sys.argv)
    if len(sys.argv) == 2 and sys.argv[1] in test_list:
        test_list[sys.argv[1]]()
