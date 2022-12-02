import logging
import datetime
import logging.config
import os
import subprocess
import sys
import time
import uiautomator2 as ut2
import win32api
from sumian.devicescan import *

# log日志配置 logging.basicConfig(level=logging.DEBUG,filename='D:\py\sumian\kill\kliiAPP.log', format='%(asctime)s  --%(
# filename)s  --[line:%(lineno)d]  --%(levelname)s  --%(message)s')  #以基础配置打印出时间、行数、信息

#思考，如何将一个脚本做成所有的APP通用，1、每次重连成功的判断节点
#2、等待的时间
# 3、下一步操作的顺序
#4、log打印



#dev测试版本APP包名是com.sumian.app,正式版本APP包名是com.sumian.sd

# cf = './yaml/log.conf'  # 使用log.conf配置文件输出
logging.config.fileConfig("./yaml/log.conf")
# cf = configparser.RawConfigParser()
logging = logging.getLogger()


logging.info('>>>>开始进行杀进程回连压测>>>>')
logging.info('总测试次数：' + str(cycle_index))  # 打印本次要测试总次数
start1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logging.info('本次开始测试时间：' + str(start1))  # 打印本轮压力测试的北京时间

i = 0
while i < cycle_index:
    os.system('adb shell settings get global bluetooth_on')  # 判断当前蓝牙开关状态
    time.sleep(2)
    # os.system('adb shell am force-stop com.sumian.app')  # 结束APP进程,测试版本APP
    os.system('adb shell am force-stop com.sumian.sd')#结束APP进程，正式版本APP
    logging.info('我被关闭啦')
    time.sleep(5)
    # os.system('adb shell am start -n com.sumian.app/com.sumian.sd.main.WelcomeActivity')  # 启动APP,测试版本APP
    os.system('adb shell am start -n com.sumian.sd/com.sumian.sd.main.WelcomeActivity') #正式版本APP
    time.sleep(5)
    logging.info('我又起来啦')
    device(resourceId="com.sumian.sd:id/tb_diary").click()  # 点击设备Tab


    start = datetime.datetime.now()  # 计时开始
    # time.sleep(15)
    os.system('python G:\py\sumian\daojishi.py')#调用倒计时脚本，默认是15秒

    os.system('adb shell input tap 960 525')  # 操作一次点击关闭，如果有的话就会生效
    try:
        # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        watch_battery = device(resourceId="com.sumian.sd:id/tv_monitor_status").get_text() #获取监测仪设备连接状态
        logging.info('当前获取的连接状态信息--'+watch_battery)
        while watch_battery == '已连接':
            time.sleep(3)
            watch_battery2 = device(resourceId="com.sumian.sd:id/tv_sleep_master_status").get_text()#获取速眠仪连接状态
            logging.info(watch_battery2)#打印速眠仪当前连接状态
            if watch_battery2 == '已连接':
                logging.info('第' + str(i + 1) + '次：很快/' + '监测仪：' + watch_battery + '速眠仪：' + watch_battery2)  # log输出显示第几次连接成功
                print("小哥哥好厉害哦~")
                break

            else:
                time.sleep(2)
                logging.info('第' + str(i + 1) + '次：速眠仪连接失败/'  + '监测仪：' + watch_battery + '速眠仪：' + watch_battery2)
                print("速眠仪连不上了~+1")
                break

        while watch_battery == '连接中':
            print("我还在连接中")
            time.sleep(10)
            # os.system('python daojishi.py')
            os.system('adb shell input tap 960 525')  # 操作一次点击关闭，如果有的话就会生效
            # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
            watch_battery = device(resourceId="com.sumian.sd:id/tv_monitor_status").get_text()  # 正式版本APP
            if watch_battery == '已连接':
                print("等一下哦~")
                time.sleep(3)
                watch_battery2 = device(resourceId="com.sumian.sd:id/tv_sleep_master_status").get_text()  # 获取速眠仪连接状态
                logging.info(watch_battery2)  # 打印速眠仪当前连接状态
                logging.info('第' + str(i + 1) + '次：比较慢////' + watch_battery)  # log输出显示第几次连接成功
                break


            else:
                print("再等一下哈！")
                time.sleep(10)
                # os.system('python daojishi.py')
                # watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
                watch_battery = device(resourceId="com.sumian.sd:id/tv_monitor_status").get_text()  # 正式版本APP
                if watch_battery == '已连接':
                    time.sleep(3)
                    watch_battery2 = device(resourceId="com.sumian.sd:id/tv_sleep_master_status").get_text()  # 获取速眠仪连接状态
                    logging.info(watch_battery2)  # 打印速眠仪当前连接状态
                    logging.info('第' + str(i + 1) + '次：太慢了////' + watch_battery)  # log输出显示第几次连接成功
                    print("太慢了小趴菜")
                    break

                else:
                    print("最后再努力一把~")
                    time.sleep(1)
                    os.system('adb shell input tap 561 1140')  # 点击连接失败弹框的确定按钮
                    time.sleep(1)
                    watch_battery2 = device(resourceId="com.sumian.sd:id/tv_sleep_master_status").get_text()  # 获取速眠仪连接状态
                    logging.info('第' + str(i + 1) + '次：失败////' + watch_battery +watch_battery2)  # 输出log判断第几次失败
                    print("唉呀妈呀连不上啦~")
                    # 失败后执行一次开关手机的蓝牙
                    os.system('adb shell service call statusbar 1')  # 下拉通知栏
                    logging.info("下拉通知栏")
                    time.sleep(2)
                    os.system('adb shell input tap 530 230')  # 360N5手机，屏幕分辨率是1080*1920
                    logging.info("关闭蓝牙")
                    time.sleep(2)
                    os.system('adb shell input tap 530 230')  # 360N5手机，屏幕分辨率是1080*1920
                    logging.info("开启蓝牙")
                    os.system('adb shell service call statusbar 2')  # 收起通知栏
                    logging.info("收起通知栏")
                    break  #失败一次，结束

    except:
        logging.info('哎呀你咋连不上了呢，sumianA APP已关闭')
        break
        #以上这步操作就是当每次开始时进行get连接状态信息不到时直接结束并流转到后续操作

    i += 1  # 测试次数+1
    logging.info('第' + str(i) + '次结束')
    end = datetime.datetime.now()  # 计时结束
    logging.info(end - start)  # 计算单次测试连接时间

#运行搜索日志中关键词的脚本
def start():
    cmd = "G:\\py\\sumian\\kill\\killAPP_processLog.bat"  # 执行运行bat脚本，公司电脑路径
    # cmd = "D:\\ProgramFiles\\JetBrains\\PycharmProjects\\sumian\\py\\sumian\\kill\\killAPP_processLog.bat"  # 自己的惠普笔记本电脑路径
    win32api.ShellExecute(0, 'open', cmd, '', '', 1)  # 前台打开

start()
print('运行完成')
time.sleep(20)

#调用发送邮件的的脚本
os.system('python sendemailkill.py')
print("发送结束")

