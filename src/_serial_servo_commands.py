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
# title           :_serial_servo_commands.py
# author          :Hiwonder, LuYongping(Lucas)
# date            :20210205
# notes           :
# ==============================================================================

import time
import struct
import threading
import serial
from ._common import GPIO

FRAME_HEADER = 0x55
MOVE_TIME_WRITE = 1
MOVE_TIME_READ = 2
MOVE_TIME_WAIT_WRITE = 7
MOVE_TIME_WAIT_READ = 8
MOVE_START = 11
MOVE_STOP = 12
ID_WRITE = 13
ID_READ = 14
ANGLE_OFFSET_ADJUST = 17
ANGLE_OFFSET_WRITE = 18
ANGLE_OFFSET_READ = 19
ANGLE_LIMIT_WRITE = 20
ANGLE_LIMIT_READ = 21
VIN_LIMIT_WRITE = 22
VIN_LIMIT_READ = 23
TEMP_MAX_LIMIT_WRITE = 24
TEMP_MAX_LIMIT_READ = 25
TEMP_READ = 26
VIN_READ = 27
POS_READ = 28
OR_MOTOR_MODE_WRITE = 29
OR_MOTOR_MODE_READ = 30
LOAD_OR_UNLOAD_WRITE = 31
LOAD_OR_UNLOAD_READ = 32
LED_CTRL_WRITE = 33
LED_CTRL_READ = 34
LED_ERROR_WRITE = 35
LED_ERROR_READ = 36

_rx_pin = 7
_tx_pin = 13
_serial_handle = serial.Serial("/dev/ttyAMA0", 115200)  # 初始化串口， 波特率为115200
lock = threading.Lock()


def port_init():
    GPIO.setup(_rx_pin, GPIO.OUT)  # 配置RX_CON 即 GPIO17 为输出
    GPIO.output(_rx_pin, 0)
    GPIO.setup(_tx_pin, GPIO.OUT)  # 配置TX_CON 即 GPIO27 为输出
    GPIO.output(_tx_pin, 1)


def port_as_write():  # 配置单线串口为输出
    GPIO.output(_rx_pin, 0)  # 拉低RX_CON 即 GPIO17
    GPIO.output(_tx_pin, 1)  # 拉高TX_CON 即 GPIO27


def port_as_read():  # 配置单线串口为输入
    GPIO.output(_tx_pin, 0)  # 拉低TX_CON 即 GPIO27
    GPIO.output(_rx_pin, 1)  # 拉高RX_CON 即 GPIO17


def port_reset():
    time.sleep(0.1)
    _serial_handle.close()
    GPIO.output(_rx_pin, 1)
    GPIO.output(_tx_pin, 1)
    _serial_handle.open()
    time.sleep(0.1)


def write_cmd(id_, cmd, params=None):
    """
    写指令
    :param id_:
    :param cmd:
    :param params:
    :return: None
    """
    with lock:
        port_as_write()
        # 写数据
        params_buf = []
        if isinstance(params, list):
            for p in params:
                params_buf.extend([p % 256, p // 256 % 256])  # 分低8位 高8位 放入缓存
        else:
            if isinstance(params, int) and 0 <= params < 256:
                params_buf.append(params)
        buf = [0x55, 0x55, id_, len(params_buf) + 3 if params else 3, cmd]
        buf.extend(params_buf)
        buf.append(255 - (sum(buf[2:]) % 256))
        _serial_handle.write(bytes(buf))  # write


def send_read_cmd(id_=None, cmd=None):
    """
    发送读取命令
    :param id_:
    :param cmd:
    :return:
    """
    port_as_write()
    buf = [0x55, 0x55, id_, 3, cmd, 0x00]
    buf[-1](255 - (sum(buf[2:-1]) % 256))
    _serial_handle.write(buf)  # 发送
    time.sleep(0.00034)


def _read_msg_base(cmd):
    """
    # 获取指定读取命令的数据
    :param cmd: 读取命令
    :return: 数据
    """
    _serial_handle.flushInput()  # 清空接收缓存
    port_as_read()  # 将单线串口配置为输入
    time.sleep(0.005)  # 稍作延时，等待接收完毕
    recv_len = _serial_handle.inWaiting()  # 获取接收缓存中的字节数
    if recv_len < 5:
        return None
    # for i in recv_data:
    #     print('%#x' %ord(i))

    recv_data = _serial_handle.read(recv_len)  # 读取接收到的数据
    cmd_len = recv_data[3]
    if recv_data[0] != FRAME_HEADER or recv_data[1] != FRAME_HEADER or cmd != recv_data[3]:
        return None
    if cmd_len == 3:
        return True
    elif cmd_len + 2 <= recv_len:
        return struct.unpack({4: "<c", 5: "<h", 7: "<hh"}[cmd_len], recv_data[5: 5 + cmd_len - 3])
    else:
        return None


def read_msg(id_, cmd, retry=50):
    for i in range(retry):
        with lock:
            send_read_cmd(id_, cmd)
            msg = _read_msg_base(cmd)
            if msg is not None:
                return msg
