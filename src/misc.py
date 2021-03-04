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
# title           :misc.py
# author          :Hiwonder, LuYongping(Lucas)
# date            :20210205
# notes           :
# ==============================================================================


def val_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def empty_func(args=None):
    return args


def set_bounds(x, x_min, x_max):
    return x_min if x < x_min else x_max if x > x_max else x
