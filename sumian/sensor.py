import logging
import datetime
import logging.config
import os
import subprocess
import sys
import time
import uiautomator2 as ut2
import win32api
from devicescan import *

#该脚本是调用NFR connect APP做下发sensor的动作，循环重复动作

logging.basicConfig(level=logging.DEBUG,filename='G:\py\sumian\sensor\sensor.log', format='%(asctime)s  --%(filename)s  --[line:%(lineno)d]  --%(levelname)s  --%(message)s')  #以基础配置打印出时间、行数、信息
logging = logging.getLogger()


logging.info('>>>>开始进行sensor压测>>>>')
logging.info('总测试次数：' + str(cycle_index))  # 打印本次要测试总次数
start1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logging.info('本次开始测试时间：' + str(start1))  # 打印本轮压力测试的北京时间

i = 0
while i < cycle_index:
    os.system('adb shell settings get global bluetooth_on')  # 判断当前蓝牙开关状态
    os.system('adb shell input tap 516 576')  # 点击发送服务入口
    time.sleep(1)
    os.system('adb shell input tap 1160 656') #点击发送服务入口
    time.sleep(2)
    logging.info('点击服务')
    os.system('adb shell input text sensor')  # 输入文本
    time.sleep(4)
    os.system('adb shell input tap 947 803')  # 点击发送

    # time.sleep(15)
    os.system('python G:\py\sumian\daojishi.py')#调用倒计时脚本，默认是15秒
    i += 1  # 测试次数+1
    logging.info('已发送' + str(i) + '次')   #记录在文本内
    print('第' + str(i) + '次结束')  #打印在窗口

