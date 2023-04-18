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
    os.system('adb shell am force-stop com.sumian.sd') #结束进程
    time.sleep(15)
    # os.system('adb shell am start -n com.sumian.app/com.sumian.sd.main.WelcomeActivity')  # 启动测试版APP
    os.system('adb shell am start -n com.sumian.sd/com.sumian.sd.main.WelcomeActivity')  # 启动测试版APP
    time.sleep(5)
    device(resourceId="com.sumian.sd:id/tb_diary").click()  # 点击设备Tab


    getBT = os.system('adb shell settings get global bluetooth_on') # 判断当前蓝牙开关状态，1为打开，0为关闭
    if getBT == '0':
        logging.info('当前蓝牙状态：开启')
    else:
        logging.info('当前蓝牙状态：关闭')

    os.system('adb shell service call statusbar 1')  # 下拉通知栏
    logging.info("下拉通知栏")
    time.sleep(3)
    # os.system('adb shell input tap 420 340') #目前是针对努比亚Z7MINI手机进行适配，屏幕分辨率是1080*1920
    # os.system('adb shell input tap 880 730')
    # os.system('adb shell input tap 530 230')  # 360N5手机，屏幕分辨率是1080*1920
    # os.system('adb shell input tap 616 424')  #realme GT neo


    os.system('adb shell input swipe 625 311 625 1424 3000') #平板上在通知中心界面下拉展开
    time.sleep(3)
    os.system('adb shell input tap 413 590') #平板点击蓝牙开关
    time.sleep(1)
    os.system('adb shell input tap 860 88')
    logging.info("关闭蓝牙")
    time.sleep(1)
    os.system('adb shell service call statusbar 2')  # 收起通知栏
    logging.info("收起通知栏")
    time.sleep(1)
    os.system('adb shell input tap 1068 690')  # 点击连接失败弹框的确定按钮
    time.sleep(1)
    # os.system('adb shell input tap 522 1070')  # 点击首页开启蓝牙的大按钮
    os.system('adb shell input tap 695 330')  #平板上点击开启蓝牙
    # os.system('adb shell input tap 540 1182')  #realme GT NEO手机
    logging.info("开启蓝牙")
    start = datetime.datetime.now()  # 计时开始
    # time.sleep(15)
    os.system('python G:\py\sumian\daojishi.py') #调用倒计时脚本，默认是15秒

    os.system('adb shell input tap 1068 689')  # 操作一次点击关闭，如果有的话就会生效
    # {"x": 1068, "y": 689, "width": 72, "height": 72}
    # os.system('adb shell input tap 970 870')  #点击关闭，realme GT neo
    try:
        # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        watch_battery = device(resourceId="com.sumian.sd:id/tv_monitor_status").get_text() #获取监测仪设备连接状态
        # logging.info('当前获取的连接状态信息--'+watch_battery)
        while watch_battery == '已连接':
            time.sleep(1)
            # watch_battery2 = device(resourceId="com.sumian.sd:id/tv_sleep_master_status").get_text()#获取速眠仪连接状态
            # logging.info('速眠仪：' + watch_battery2)#打印速眠仪当前连接状态
            # if watch_battery2 == '已连接':
            #     logging.info('第' + str(i + 1) + '次：很快/' + '监测仪：' + watch_battery + ',速眠仪：' + watch_battery2)  # log输出显示第几次连接成功
            #     print("小哥哥好厉害哦~")
            #     break

            # else:
            #     time.sleep(2)
            #     logging.info('第' + str(i + 1) + '次：/'  + '监测仪：' + watch_battery + ',速眠仪：' + watch_battery2)
            #     print("速眠仪你不在吗~+1")
            #     break

            logging.info('第' + str(i + 1) + '次：/'  + '监测仪：' + watch_battery)
            break



        # while watch_battery != '已连接':
        #     print("我还在连接中")
        #     time.sleep(10)
        #     # os.system('python daojishi.py')
        #     os.system('adb shell input tap 960 525')  # 操作一次点击关闭，如果有的话就会生效
        #     # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        #     watch_battery = device(resourceId="com.sumian.sd:id/tv_monitor_status").get_text()  # 获取监测仪设备连接状态
        #     if watch_battery == '已连接':
        #         print("等一下哦~")
        #         time.sleep(3)
        #         watch_battery2 = device(resourceId="com.sumian.sd:id/tv_sleep_master_status").get_text()  # 获取速眠仪连接状态
        #         logging.info(watch_battery2)  # 打印速眠仪当前连接状态
        #         logging.info('第' + str(i + 1) + '次：比较慢////' + watch_battery)  # log输出显示第几次连接成功
        #         break
        #
        #
        #     else:
        #         print("再等一下哈！")
        #         time.sleep(10)
        #         # os.system('python daojishi.py')
        #         # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        #         watch_battery = device(resourceId="com.sumian.sd:id/tv_monitor_status").get_text()  # 获取监测仪设备连接状态
        #         if watch_battery == '已连接':
        #             time.sleep(3)
        #             watch_battery2 = device(resourceId="com.sumian.sd:id/tv_sleep_master_status").get_text()  # 获取速眠仪连接状态
        #             logging.info(watch_battery2)  # 打印速眠仪当前连接状态
        #             logging.info('第' + str(i + 1) + '次：太慢了////' + watch_battery)  # log输出显示第几次连接成功
        #             print("太慢了小趴菜")
        #             break
        #
        #         else:
        #             print("最后再努力一把~")
        #             time.sleep(1)
        #             os.system('adb shell input tap 561 1140')  # 点击连接失败弹框的确定按钮
        #             time.sleep(1)
        #             os.system('adb shell input tap 561 1140')  # 点击连接失败弹框的确定按钮
        #             time.sleep(1)
        #             logging.info('第' + str(i + 1) + '次：失败////' + watch_battery)  # 输出log判断第几次失败
        #             print("失败了")
        #             # os.system('adb shell input keyevent 25') #按音量下键
        #             # os.system('adb shell input keyevent 26') #按电源键
        #             # time.sleep(2)
        #             break  #失败一次，结束

    except:
        os.system('adb shell input tap 695 330')  # 操作一次点击重连
        time.sleep(2)
        watch_battery4 = device(resourceId="com.sumian.sd:id/tv_no_device_title").get_text()  #获取连接中状态
        logging.info(watch_battery4)
        time.sleep(2)
        os.system('adb shell input tap 695 330')  # 操作一次点击重连
        if watch_battery4 == '监测仪连接中…':
            print("我还在连接中")
            os.system('adb shell input tap 695 330')
            print("再等一下哈！")
            print("最后再努力一把~")
            time.sleep(8)
            os.system('adb shell input tap 960 525')  # 操作一次点击关闭，如果有的话就会生效
            # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
            watch_battery = device(resourceId="com.sumian.sd:id/tv_no_device_title").get_text()  # 获取监测仪设备连接状态
            logging.info(watch_battery)
            time.sleep(5)
            watch_battery3 = device(resourceId="com.sumian.sd:id/tv_no_device_title").get_text()  # 获取监测仪设备连接状态
            logging.info(watch_battery3)
            time.sleep(5)
            os.system('adb shell input tap 695 330')  # 操作一次点击重连
            os.system('python G:\py\sumian\daojishi.py')  # 调用倒计时脚本，默认是15秒

            watch_battery5 = device(resourceId="com.sumian.sd:id/vg_no_device").get_text()
            if watch_battery5 == "监测仪连接中":
                logging.info('第' + str(i + 1) + '次：等了好久也不知道连上没有////')  # log输出显示第几次连接成功
                break




        else:
            print("结束前多等一下吧")
            time.sleep(10)
            os.system('adb shell input tap 561 1140')  # 点击连接失败弹框的确定按钮
            time.sleep(1)
            os.system('adb shell input tap 561 1140')  # 点击连接失败弹框的确定按钮
            time.sleep(1)
            logging.info('第' + str(i + 1) + '次：失败////')  # 输出log判断第几次失败
            # print("失败了")
            logging.info('哎呀你咋连不上了呢')
            break




    i += 1  # 测试次数+1
    logging.info('第' + str(i) + '次结束')
    end = datetime.datetime.now()  # 计时结束
    logging.info(end - start)  # 计算单次测试连接时间


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