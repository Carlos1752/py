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


#log日志配置
# logging.basicConfig(level=logging.INFO,filemode='a',filename='G:\py\sumian\OTA\OTA.log',
#                     format='%(asctime)s  --%(filename)s  --[line:%(lineno)d]  --%(levelname)s  --%(message)s')  #以基础配置打印出时间、行数、信息

CON_LOG='./yaml/log.conf'  #使用log.conf配置文件输出
logging.config.fileConfig(CON_LOG)
logging=logging.getLogger()


# 连接手机 ADB
devices = str(subprocess.check_output('adb devices')).replace(" ", "")\
    .replace("b'Listofdevicesattached", "").replace("device", "").replace("\\", "").replace("rn", "").replace("t'", "")
assert ut2.connect(devices), "请在cmd里输入adb devices确认设备是否存在"
device = ut2.connect(devices)


if devices != 'c7cff486' and  devices != 'c23d076' and devices != '94a138a9':                   #nubia Z7mini手机,360N5，坚果手机
    print("未连接设备")
    sys.exit()
    #判断是否指定的设备存在，如果不一致就结束

else:
    print(devices)
    os.system('adb shell wm size') #打印手机分辨率
    #判断是否指定的设备存在，如果一致就继续，且打印出设备名称


print("请输入次数：", end="")
cycle_index = int(input())
logging.info('>>>>开始进行OTA压测>>>>')
logging.info('总测试次数：'+str(cycle_index))#打印本次要测试总次数

device.app_start("com.sumian.app")


i = 0
while i < cycle_index:
    start1 = datetime.datetime.now()
    os.system('adb shell am force-stop com.sumian.app')  # 结束APP进程
    time.sleep(3)
    logging.info('本次开始测试时间：' + str(start1))  # 打印本轮压力测试的北京时间
    os.system('adb shell am start -n com.sumian.app/com.sumian.sd.main.WelcomeActivity')  # 启动APP
    time.sleep(15)
    os.system('adb shell settings get global bluetooth_on')#判断当前蓝牙开关状态
    time.sleep(5)

    watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text() #获取设备连接状态
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
        time.sleep(240)
        logging.info('我静静地等你showtime完成！')
        logging.info('哈哈，小比崽子传完了吧，我要返回了哦。')
        device(resourceId="com.sumian.app:id/bt_confirm").click()   #点击升级成功确认按钮
        logging.info('升级成功')
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
            logging.info('第'+str(i + 1) + '次：升级失败////' + watch_battery) #输出升级重连失败


    else:
        logging.info('哎呀，怎么连接失败了呢，升级不了啦。。。')
        time.sleep(3)
        watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        logging.info('第'+str(i+1)+'次：连接失败////'+watch_battery)   #输出log判断第几次失败

    i+=1  #测试次数+1
    logging.info('第'+str(i)+'次结束')
    end = datetime.datetime.now() #计时结束
    logging.info(end-start1) #计算单次测试连接时间

while i == cycle_index:
    logging.info(str(i)+'次OTA搞完啦，请尽快查看数据')
    print('大兄弟，我搞完啦。你来呀~~~')
    break

def start():
    cmd = "G:\\py\\sumian\\OTA\\OTA_processLog.bat"  # 执行运行bat脚本
    win32api.ShellExecute(0, 'open', cmd, '', '', 1)  # 前台打开

start()
print('运行完成')
time.sleep(3)

