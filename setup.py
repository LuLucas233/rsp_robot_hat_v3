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
# title           :setup.py
# author          :Hiwonder
# date            :20210205
# notes           :
# ==============================================================================

from setuptools import setup, find_packages

setup(name='rsp_robot_hat_v3',
      version='1.0',
      keywords=["robot", "Hiwonder"],
      description="Hiwonder robot raspberry pi hat v3 sdk",
      license="GPL v3 Licence",
      url="https://hiwonder.com",
      author="Hiwonder",
      author_email="support@hiwonder.com",

      include_package_data=True,
      zip_safe=False,
      packages=["rsp_robot_hat_v3", ],
      package_dir={"rsp_robot_hat_v3": "./src"},
      install_requires=[],
      )
