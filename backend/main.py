# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:58
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : main.py
# @Project : test_platform
# @Description : launch file
from apps import app

from settings import HOST, PORT, AUTO_RELOAD, DEBUG, ACCESS_LOG


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, auto_reload=AUTO_RELOAD, debug=DEBUG, access_log=ACCESS_LOG)
