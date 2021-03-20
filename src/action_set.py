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
from .serial_servo import set_position
from .misc import empty_func as _empty_func


class ActionSet:
    def __init__(self, path, repeat=1, lock_servos=None):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.path = path
        self.repeat = repeat
        self.lock_servos = lock_servos if lock_servos else dict()
        self.action_data = []


async def _run_action_set(action_sets: tuple):
    """
    :param action_sets: The path of the action set you want to run
    :return:
    """
    for action_set in action_sets:
        # 从动作组文件中取出动作数据
        with sql.connect(action_set.path) as ag:
            action_data = ag.execute("select * from ActionGroup").fetchall()
        # 对动作数据做些处理
        # 将所有动作里面被lock的舵机的角度设为指定lock的角度
        for id_, lock_pos in action_set.lock_servos.items():
            for act in action_data:
                act[1 + id_] = lock_pos
        action_set.action_data = action_data

    for action_set in action_sets:
        for i in range(action_set.repeat):
            for action in action_set.action_data:
                duration = action[1]
                pos_set = action[2:]
                for id_, pos in enumerate(pos_set, 1):
                    set_position(id_, pos, duration)
                await asyncio.sleep(duration / 1000.0)


def run_action_set(action_set, block=True, done_callback=_empty_func):
    """
    run an action set

    :param action_set: The path of the action set you want to run
    :param block:
    :param done_callback:
    :return:
    """
    if block:
        asyncio.run(_run_action_set((action_set,)))
    else:
        f = asyncio.run_coroutine_threadsafe(_run_action_set((action_set,)), _loop)
        f.add_done_callback(done_callback)
        return f


def run_multi_action_sets(action_sets, block=True, done_callback=_empty_func):
    """
    运行多个动作组

    :param action_sets: 要允许的动作组及运行
    :param block:
    :param done_callback:
    :return:
    """
    if block:
        asyncio.run(_run_action_set(action_sets))
    else:
        f = asyncio.run_coroutine_threadsafe(_run_action_set(action_sets), _loop)
        f.add_done_callback(done_callback)
        return f


def _start_loop(loop_):
    asyncio.set_event_loop(loop_)
    loop_.run_forever()


_loop = asyncio.get_event_loop()
threading.Thread(target=_start_loop, args=(_loop,), daemon=True).start()
