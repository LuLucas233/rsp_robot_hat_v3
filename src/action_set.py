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
# title           :actionset.py
# author          :Hiwonder, LuYongping(Lucas)
# date            :20210303
# notes           :
# ==============================================================================

import os
import asyncio
import threading
import sqlite3 as sql
from .misc import empty_func
from .serial_servo import set_position


async def _run_action_set(act_path, repeat=1, lock_servos=None):
    """
    :param act_path: The path of the action set you want to run
    :param repeat: The number of times this action is repeated
    :param lock_servos:
    :return:
    """

    if not os.path.exists(act_path):
        raise FileNotFoundError(act_path)

    # 从动作组文件中取出动作数据
    ag = sql.connect(act_path)
    cu = ag.cursor()
    cu.execute("select * from ActionGroup")
    action_set = cu.fetchall()
    if not action_set:
        return

    # 对动作数据做些处理
    # 将所有动作里面被lock的舵机的角度设为指定lock的角度
    lock_servos = lock_servos if lock_servos else dict()
    for id_, lock_pos in lock_servos.items():
        for act in action_set:
            act[1 + id_] = lock_pos

    # 运行动作
    for i in range(repeat):
        for action in action_set:
            duration = action[1]
            pos_set = action[2:]
            for id_, pos in enumerate(pos_set, 1):
                set_position(id_, pos, duration)
            await asyncio.sleep(duration / 1000.0)


def run_action_set(act_path, repeat=1, block=True, lock_servos=None, done_callback=empty_func):
    """
    run an action set

    :param act_path: The path of the action set you want to run
    :param repeat: The number of times this action is repeated
    :param block:
    :param lock_servos:
    :param done_callback:
    :return:
    """
    if block:
        asyncio.run(_run_action_set(act_path, repeat, lock_servos))
    else:
        future = asyncio.run_coroutine_threadsafe(_run_action_set(act_path, repeat, lock_servos), _loop)
        future.add_done_callback(done_callback)
        return future


def _start_loop(loop_):
    asyncio.set_event_loop(loop_)
    loop_.run_forever()


_loop = asyncio.get_event_loop()
threading.Thread(target=_start_loop, args=(_loop,), daemon=True).start()

