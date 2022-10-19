import unittest
import os
import subprocess
import time
import random
import uiautomator2 as ut2
import datetime
import logging
import logging.config
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import win32api
from sumian.devicescan import *


#log日志配置
# logging.basicConfig(level=logging.INFO,filemode='a',filename='G:\py\sumian\OTA\OTA.log',
#                     format='%(asctime)s  --%(filename)s  --[line:%(lineno)d]  --%(levelname)s  --%(message)s')  #以基础配置打印出时间、行数、信息

CON_LOG='./yaml/log.conf'  #使用log.conf配置文件输出
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()


logging.info('>>>>开始进行OTA压测>>>>')


# device.app_start("com.sumian.app")


i = 0
while i < cycle_index:
    start1 = datetime.datetime.now()
    os.system('adb shell am force-stop com.sumian.app')  # 结束APP进程
    time.sleep(3)
    logging.info('本次开始测试时间：' + str(start1))  # 打印本轮压力测试的北京时间
    os.system('adb shell am start -n com.sumian.app/com.sumian.sd.main.WelcomeActivity')  # 启动APP
    time.sleep(10)
    os.system('adb shell settings get global bluetooth_on')#判断当前蓝牙开关状态
    time.sleep(2)
    os.system('adb shell input tap 960 525')  # 操作一次点击关闭，如果有的话就会生效
    time.sleep(3)

    watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text() #获取设备连接状态
    #如果判断是已连接的状态，则走开始升级的流程
    if watch_battery == '已连接': #判断设备如果是“已连接”状态
        time.sleep(1)
        os.system('adb shell am start -n com.sumian.app/com.sumian.sd.examine.main.me.ExamineVersionUpdateActivity') #调用版本界面
        # os.system('adb shell input tap 350 1435')#点击坐标监测仪升级入口
        logging.info('进入到版本界面')
        device(resourceId="com.sumian.app:id/tv_desc").click()  # 通过ID点击监测仪升级入口按钮
        # os.system('adb shell input tap 500 1327') #点击坐标点击下载按钮
        logging.info('进入监测仪升级检测界面')
        device(resourceId="com.sumian.app:id/bt_download").click()  #通过ID点击下载按钮
        logging.info('开始下载')
        time.sleep(5)
        device(resourceId="com.sumian.app:id/bt_upgrade").click()  #通过ID点击升级按钮
        logging.info('开始升级，请耐心等待~')
        # os.system('adb shell input tap 500 1327') #点击坐标点击升级按钮
        time.sleep(10)
        logging.info('我静静地等你showtime完成！')
        os.system('python totaltime.py')  #调用倒计时脚本进行倒计时，默认是160秒，时间可以调整

        # time.sleep(190)

        logging.info('哈哈，检查一下你小比崽子是不是还在传，再多等一会吧。')

        upgrade = device(resourceId="com.sumian.app:id/tv_version_title").get_text()#获取升级成功弹框的button文案
        print('get到了:'+upgrade)
        if upgrade == '固件升级中':
            #若还是处于升级中，则继续等待
            time.sleep(10)
            print("继续等待10秒")
            time.sleep(10)
            print("继续等待20秒")
            time.sleep(10)
            print("继续等待30秒")
            time.sleep(10)
            print("继续等待40秒")
            time.sleep(10)
            print("继续等待50秒")
            time.sleep(10)
            print("继续等待60秒")
            time.sleep(10)
            print("继续等待70秒")
            time.sleep(10)
            print("继续等待80秒")

            # print("继续等待80秒")
            # time.sleep(80)

        else:
        # 判断是否有升级弹框或者弹框文案为确认
            time.sleep(1)
            print("OMG~小老弟挺快啊")


        d = device(resourceId="com.sumian.app:id/bt_confirm").get_text()  #获取升级成功弹框按钮文案
        print('get到了:'+d)#打印按钮的文案
        time.sleep(1)
        device(resourceId="com.sumian.app:id/bt_confirm").click()   #点击升级成功确认按钮
        time.sleep(2)
        os.system('adb shell input keyevent 4')  #点击返回键
        logging.info('返回设置界面')
        time.sleep(2)
        device(resourceId="com.sumian.app:id/tab_device").click()  #点击第一个Tab入口
        logging.info('返回首页')
        # os.system('adb shell am start -n com.sumian.app/com.sumian.sd.main.WelcomeActivity') #返回到首页
        time.sleep(2)

        watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        logging.info('开始获取连接状态信息')

        if watch_battery == '已连接':
            logging.info('第'+str(i + 1) + '次：升级成功////' + watch_battery)  # log输出显示第几次连接成功

        else:
            logging.info('第'+str(i + 1) + '次：升级连接失败////' + watch_battery) #输出升级重连失败
#如果判断已经不是已连接的状态，即走失败流程
    else:
        logging.info('哎呀，怎么连接失败了呢，升级不了啦。。。')
        time.sleep(3)
        watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        logging.info('第'+str(i+1)+'次：连接失败////'+watch_battery)   #输出log判断第几次失败
#循环累计，直到达到设计的次数
    i+=1  #测试次数+1
    logging.info('第'+str(i)+'次结束')
    end = datetime.datetime.now() #计时结束
    logging.info(end-start1) #计算单次测试连接时间

#当达到设计的次数，则执行以下log打印并结束测试
while i == cycle_index:
    logging.info(str(i)+'次OTA搞完啦，请尽快查看数据')
    print('大兄弟，我搞完啦。你来呀~~~')
    break
#执行运行汇总脚本
def start():
    cmd = "G:\\py\\sumian\\OTA\\OTA_processLog.bat"  # 执行运行bat脚本
    # cmd = "D:\\ProgramFiles\\JetBrains\\PycharmProjects\\sumian\\py\\sumian\\OTA\\OTA_processLog.bat"
    win32api.ShellExecute(0, 'open', cmd, '', '', 1)  # 前台打开

start()
print('运行完成')
time.sleep(3)


send = os.system('python sendemailOTA.py')
print('发送结束')