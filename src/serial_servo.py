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
# title           :serial_servo.py
# author          :Hiwonder, LuYongping(Lucas)
# date            :20210205
# notes           :
# ==============================================================================

import time
from .misc import set_bounds
from . import _serial_servo_commands as _ssc

_ssc.port_init()


def set_id(new_id, old_id=0xFE):
    """
    设置舵机id
    :param new_id:
    :param old_id:
    :return:
    """
    _ssc.write_cmd(old_id, _ssc.ID_WRITE, new_id)


def get_id(id_=None, retry=50):
    """
    读取串口舵机id
    :param id_: 默认为空
    :param retry:
    :return: 返回舵机id
    """
    id_ = id_ if id_ else 0xFE
    return _ssc.read_msg(id_, _ssc.ID_READ, retry)


def set_position(id_, position, duration):
    """
    驱动串口舵机转到指定位置

    :param id_: 要驱动的舵机id
    :param position: 位置
    :param duration: 转动需要的时间
    """
    position = set_bounds(position, 0, 1000)
    duration = set_bounds(duration, 0, 30000)
    _ssc.write_cmd(id_, _ssc.MOVE_TIME_WRITE, [position, duration])


def stop(id_=None):
    """
    停止舵机运行
    :param id_:
    :return:
    """
    _ssc.write_cmd(id_, _ssc.MOVE_STOP)


def set_deviation(id_, d=0):
    """
    调整偏差
    :param id_: 舵机id
    :param d:  偏差
    """
    _ssc.write_cmd(id_, _ssc.ANGLE_OFFSET_ADJUST, d)


def save_deviation(id_):
    """
    配置偏差，掉电保护
    :param id_: 舵机id
    """
    _ssc.write_cmd(id_, _ssc.ANGLE_OFFSET_WRITE)


def get_deviation(id_, retry=50):
    """
    读取偏差值
    :param id_: 舵机号
    :param retry: 重试次数
    :return:
    """
    return _ssc.read_msg(id_, _ssc.ANGLE_OFFSET_READ)


def set_position_limit(id_, low, high):
    """
    设置舵机转动范围
    :param id_:
    :param low:
    :param high:
    :return:
    """
    _ssc.write_cmd(id_, _ssc.ANGLE_LIMIT_WRITE, [low, high])


def get_position_limit(id_, retry=50):
    """
    读取舵机转动范围
    :param id_:
    :param retry:
    :return: 返回元祖 0： 低位  1： 高位
    """
    return _ssc.read_msg(_ssc.ANGLE_LIMIT_READ, retry)


def set_vin_limit(id_, low, high):
    """
    设置舵机电压范围
    :param id_:
    :param low:
    :param high:
    :return:
    """
    _ssc.write_cmd(id_, _ssc.VIN_LIMIT_WRITE, [low, high])


def get_vin_limit(id_, retry=50):
    """
    读取舵机转动范围
    :param id_:
    :return: 返回元祖 0： 低位  1： 高位
    """
    return _ssc.read_msg(id_, _ssc.VIN_LIMIT_READ, retry)


def set_thermal_limit(id_, m_temp):
    """
    设置舵机最高温度报警
    :param id_:
    :param m_temp:
    :return:
    """
    _ssc.write_cmd(_ssc.TEMP_MAX_LIMIT_WRITE, m_temp)


def get_thermal_limit(id_, retry=50):
    """
    读取舵机温度报警范围
    :param id_:
    :param retry:
    :return:
    """
    return _ssc.read_msg(id_, _ssc.TEMP_MAX_LIMIT_READ, retry)


def get_position(id_, retry=50):
    """
    读取舵机当前位置
    :param id_:
    :param retry:
    :return:
    """
    return _ssc.read_msg(id_, _ssc.POS_READ, retry)


def get_temperature(id_, retry=50):
    """
    读取舵机温度
    :param id_:
    :param retry:
    :return:
    """
    return _ssc.read_msg(id_, _ssc.TEMP_READ, retry)


def get_vin(id_, retry=50):
    """
    读取舵机电压
    :param id_:
    :param retry:
    :return:
    """
    return _ssc.read_msg(id_, _ssc.VIN_READ, retry)


def reset_all(id_):
    """
    舵机清零偏差和P值中位（500）
    :param id_:
    :return:
    """
    set_deviation(id_, 0)  # 清零偏差
    time.sleep(0.1)
    _ssc.write_cmd(id_, _ssc.MOVE_TIME_WRITE, [500, 1000])  # 中位


def unload(id_):
    """
    舵机掉电
    :param id_:
    :return:
    """
    _ssc.write_cmd(id_, _ssc.LOAD_OR_UNLOAD_WRITE, 0)


def get_load_state(id_, retry=50):
    """
    获取舵机负载状态
    :param id_:
    :param retry:
    :return:
    """
    return _ssc.read_msg(id_, _ssc.LOAD_OR_UNLOAD_READ, retry)
