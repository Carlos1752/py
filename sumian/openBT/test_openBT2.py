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

# log日志配置

# logging.basicConfig(level=logging.DEBUG,filename='G:\py\sumian\openBT\openBT_%Y_%m_%d.log', format='%(asctime)s  --%(filename)s  --[line:%(lineno)d]  --%(levelname)s  --%(message)s')
#基础打印信息

CON_LOG = './yaml/log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()

logging.info('>>>>开始进行开关蓝牙回连压测>>>>')
logging.info('总测试次数：' + str(cycle_index))  # 打印本次要测试总次数
start1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logging.info('本轮开始测试时间：' + str(start1))  # 打印本轮压力测试的北京时间

i = 0
while i < cycle_index:
    os.system('adb shell am start -n com.sumian.app/com.sumian.sd.main.WelcomeActivity')  # 启动APP
    time.sleep(5)
    os.system('adb shell settings get global bluetooth_on')  # 判断当前蓝牙开关状态，1为打开，0为关闭
    os.system('adb shell service call statusbar 1')  # 下拉通知栏
    logging.info("下拉通知栏")
    time.sleep(3)
    # os.system('adb shell input tap 420 340') #目前是针对努比亚Z7MINI手机进行适配，屏幕分辨率是1080*1920
    # os.system('adb shell input tap 880 730')
    os.system('adb shell input tap 530 230')  # 360N5手机，屏幕分辨率是1080*1920
    # os.system('adb shell input tap 616 424')  #realme GT neo
    logging.info("关闭蓝牙")
    time.sleep(2)
    os.system('adb shell service call statusbar 2')  # 收起通知栏
    logging.info("收起通知栏")
    time.sleep(2)
    os.system('adb shell input tap 561 1140')  # 点击连接失败弹框的确定按钮
    time.sleep(2)
    os.system('adb shell input tap 522 1070')  # 点击首页开启蓝牙的大按钮
    # os.system('adb shell input tap 540 1182')  #realme GT NEO手机
    logging.info("开启蓝牙")
    start = datetime.datetime.now()  # 计时开始
    # time.sleep(15)
    os.system('python G:\py\sumian\daojishi.py') #调用倒计时脚本，默认是15秒

    os.system('adb shell input tap 960 525')  # 操作一次点击关闭，如果有的话就会生效
    # os.system('adb shell input tap 970 870')  #点击关闭，realme GT neo
    try:
        watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        while watch_battery == '已连接':
            time.sleep(1)
            logging.info('第' + str(i + 1) + '次：很快////' + watch_battery)  # log输出显示第几次连接成功
            print("我get到了~")
            break

        while watch_battery == '连接中':
            print("我还在连接中")
            time.sleep(10)
            os.system('adb shell input tap 960 525')  # 操作一次点击关闭，如果有的话就会生效
            watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
            if watch_battery == '已连接':
                print("222")
                time.sleep(1)
                logging.info('第' + str(i + 1) + '次：比较慢////' + watch_battery)  # log输出显示第几次连接成功
                break


            else:
                print("33333")
                time.sleep(10)
                watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
                if watch_battery == '已连接':
                    time.sleep(1)
                    logging.info('第' + str(i + 1) + '次：太慢了////' + watch_battery)  # log输出显示第几次连接成功
                    print("太慢了小趴菜")
                    break

                else:
                    print("44444")
                    time.sleep(1)
                    os.system('adb shell input tap 561 1140')  # 点击连接失败弹框的确定按钮
                    time.sleep(1)
                    logging.info('第' + str(i + 1) + '次：失败////' + watch_battery)  # 输出log判断第几次失败
                    print("失败了")
                    # os.system('adb shell input keyevent 25') #按音量下键
                    # os.system('adb shell input keyevent 26') #按电源键
                    # time.sleep(2)
                    break  #失败一次，结束

    except:
        # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        # while watch_battery != '已连接' and watch_battery != '连接中':
        #     print("失败失败失败了")
        #     os.system('adb shell am force-stop com.sumian.app')  # 结束APP进程
        logging.info('哎呀你咋连不上了呢，sumianA APP已关闭')
    i += 1  # 测试次数+1
    logging.info('第' + str(i) + '次结束')
    end = datetime.datetime.now()  # 计时结束
    logging.info(end - start)  # 计算单次测试连接时间




# while i == cycle_index:
#     end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     logging.info('程序结束测试时间：' + str(end))  # 打印本轮压力测试结束的北京时间
#     break

#运行搜索日志中关键词的脚本
def start():
    cmd = "G:\\py\\sumian\\openBT\\openBT_processLog.bat"  # 执行运行bat脚本
    # cmd = "D:\\ProgramFiles\\JetBrains\\PycharmProjects\\sumian\\py\\sumian\\openBT\\openBT_processLog.bat"  # 自己的惠普笔记本电脑路径
    win32api.ShellExecute(0, 'open', cmd, '', '', 1)  # 前台打开


start()
print('运行完成')
time.sleep(10)

#调用发送邮件的的脚本
send = os.system('python sendemailopen.py')
print("发送结束")
 

