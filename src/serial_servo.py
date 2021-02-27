import time
from .misc import set_bounds
from . import serial_servo_commands as ssc


def set_id(new_id, old_id=0xFE):
    """
    设置舵机id
    :param new_id:
    :param old_id:
    :return:
    """
    ssc.write_cmd(old_id, ssc.ID_WRITE, new_id)


def get_id(id_=None, retry=50):
    """
    读取串口舵机id
    :param id_: 默认为空
    :param retry:
    :return: 返回舵机id
    """
    id_ = id_ if id_ else 0xFE
    return ssc.read_msg(id_, ssc.ID_READ, retry)


def set_position(id_, position, duration):
    """
    驱动串口舵机转到指定位置
    :param id_: 要驱动的舵机id
    :param position: 位置
    :param duration: 转动需要的时间
    """
    position = set_bounds(position, 0, 1000)
    duration = set_bounds(duration, 0, 30000)
    ssc.write_cmd(id_, ssc.MOVE_TIME_WRITE, [position, duration])


def stop(id_=None):
    """
    停止舵机运行
    :param id_:
    :return:
    """
    ssc.write_cmd(id_, ssc.MOVE_STOP)


def set_deviation(id_, d=0):
    """
    调整偏差
    :param id_: 舵机id
    :param d:  偏差
    """
    ssc.write_cmd(id_, ssc.ANGLE_OFFSET_ADJUST, d)


def save_deviation(id_):
    """
    配置偏差，掉电保护
    :param id_: 舵机id
    """
    ssc.write_cmd(id_, ssc.ANGLE_OFFSET_WRITE)


def get_deviation(id_, retry=50):
    """
    读取偏差值
    :param id_: 舵机号
    :param retry: 重试次数
    :return:
    """
    return ssc.read_msg(id_, ssc.ANGLE_OFFSET_READ)


def set_position_limit(id_, low, high):
    """
    设置舵机转动范围
    :param id_:
    :param low:
    :param high:
    :return:
    """
    ssc.write_cmd(id_, ssc.ANGLE_LIMIT_WRITE, [low, high])


def get_position_limit(id_, retry=50):
    """
    读取舵机转动范围
    :param id_:
    :param retry:
    :return: 返回元祖 0： 低位  1： 高位
    """
    return ssc.read_msg(ssc.ANGLE_LIMIT_READ, retry)


def set_vin_limit(id_, low, high):
    """
    设置舵机电压范围
    :param id_:
    :param low:
    :param high:
    :return:
    """
    ssc.write_cmd(id_, ssc.VIN_LIMIT_WRITE, [low, high])


def get_vin_limit(id_, retry=50):
    """
    读取舵机转动范围
    :param id_:
    :return: 返回元祖 0： 低位  1： 高位
    """
    return ssc.read_msg(id_, ssc.VIN_LIMIT_READ, retry)


def set_thermal_limit(id_, m_temp):
    """
    设置舵机最高温度报警
    :param id_:
    :param m_temp:
    :return:
    """
    ssc.write_cmd(ssc.TEMP_MAX_LIMIT_WRITE, m_temp)


def get_thermal_limit(id_, retry=50):
    """
    读取舵机温度报警范围
    :param id_:
    :param retry:
    :return:
    """
    return ssc.read_msg(id_, ssc.TEMP_MAX_LIMIT_READ, retry)


def get_position(id_, retry=50):
    """
    读取舵机当前位置
    :param id_:
    :param retry:
    :return:
    """
    return ssc.read_msg(id_, ssc.POS_READ, retry)


def get_temperature(id_, retry=50):
    """
    读取舵机温度
    :param id_:
    :param retry:
    :return:
    """
    return ssc.read_msg(id_, ssc.TEMP_READ, retry)


def get_vin(id_, retry=50):
    """
    读取舵机电压
    :param id_:
    :param retry:
    :return:
    """
    return ssc.read_msg(id_, ssc.VIN_READ, retry)


def reset_all(id_):
    """
    舵机清零偏差和P值中位（500）
    :param id_:
    :return:
    """
    set_deviation(id_, 0)  # 清零偏差
    time.sleep(0.1)
    ssc.write_cmd(id_, ssc.MOVE_TIME_WRITE, [500, 1000])  # 中位


def unload(id_):
    """
    舵机掉电
    :param id_:
    :return:
    """
    ssc.write_cmd(id_, ssc.LOAD_OR_UNLOAD_WRITE, 0)


def get_load_state(id_, retry=50):
    """
    获取舵机负载状态
    :param id_:
    :param retry:
    :return:
    """
    return ssc.read_msg(id_, ssc.LOAD_OR_UNLOAD_READ, retry)
