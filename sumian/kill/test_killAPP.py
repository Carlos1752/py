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
# logging.basicConfig(level=logging.DEBUG,filename='D:\py\sumian\kill\kliiAPP.log',
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
logging.info('>>>>开始进行杀进程回连压测>>>>')
logging.info('总测试次数：'+str(cycle_index))#打印本次要测试总次数
start1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logging.info('本次开始测试时间：' + str(start1))  # 打印本轮压力测试的北京时间



i = 0
while i < cycle_index:
    os.system('adb shell settings get global bluetooth_on')#判断当前蓝牙开关状态
    time.sleep(2)
    os.system('adb shell am force-stop com.sumian.app')  # 结束APP进程
    logging.info('我被关闭啦')
    time.sleep(5)
    os.system('adb shell am start -n com.sumian.app/com.sumian.sd.main.WelcomeActivity') #启动APP
    logging.info('我又起来啦')
    start = datetime.datetime.now()  #计时开始
    time.sleep(15)

    os.system('adb shell input tap 960 525')#操作一次点击关闭，如果有的话就会生效
    watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text() #获取设备连接状态


    if watch_battery == '已连接': #判断设备如果是“已连接”状态
        time.sleep(1)
        logging.info('第'+str(i + 1) + '次：很快////' + watch_battery)  # log输出显示第几次连接成功
        print('小哥哥好厉害哦~')


    else:
        time.sleep(15)
        watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
        if watch_battery == '已连接':
            time.sleep(1)
            logging.info('第'+str(i + 1) + '次：比较慢////' + watch_battery)  # log输出显示第几次连接成功
            print('你好慢啊，小趴菜~')

        else:
            time.sleep(18)
            watch_battery = device(resourceId="com.sumian.app:id/tv_monitor_status").get_text()  # 获取设备连接状态
            if watch_battery == '已连接':
                logging.info('第' + str(i + 1) + '次：太慢////' + watch_battery)  # log输出显示第几次连接成功
                print('你太慢啊，小趴菜~')

            else:
                time.sleep(1)
                logging.info('第'+str(i+1)+'次：失败////'+watch_battery)   #输出log判断第几次失败
                print('唉呀妈呀连不上啦~')
            #失败后执行一次开关手机的蓝牙
                os.system('adb shell service call statusbar 1');  # 下拉通知栏
                logging.info("下拉通知栏")
                time.sleep(2)
                os.system('adb shell input tap 530 230'); #360N5手机，屏幕分辨率是1080*1920
                logging.info("关闭蓝牙")
                time.sleep(2)
                os.system('adb shell input tap 530 230'); #360N5手机，屏幕分辨率是1080*1920
                logging.info("开启蓝牙")
                os.system('adb shell service call statusbar 2')  # 收起通知栏
                logging.info("收起通知栏")
                #time.sleep(2)
                # break #结束本轮测试


    i+=1  #测试次数+1
    logging.info('第'+str(i)+'次结束')
    end = datetime.datetime.now() #计时结束
    logging.info(end-start) #计算单次测试连接时间

while i == cycle_index:
    end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info('程序结束测试时间：'+str(end))  #打印本轮压力测试结束的北京时间
    print('结束了')
    break  # 结束

def start():
    cmd = "G:\\py\\sumian\\kill\\killAPP_processLog.bat"  # 执行运行bat脚本
    win32api.ShellExecute(0, 'open', cmd, '', '', 1)  # 前台打开

start()
print('运行完成')
time.sleep(3)

def sendEmail(msg_from, passwd, subject, msg_to, content, file_path1='', file_path2='', file_name1='', file_name2=''):
        # 创建一个带附件的实例
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = msg_from
    message['To'] = msg_to

        # 邮件正文内容
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    if file_path1 != '' and file_path2 != '':
            # 构造附件1
        att_txt1 = MIMEText(open(file_path1, 'rb').read(), 'base64', 'gb2312')
        att_txt1["Content-Type"] = 'application/octet-stream'
        att_txt1.add_header("Content-Disposition", 'attachment', filename=file_name1)
        message.attach(att_txt1)
            #构造附件2
        att_txt2 = MIMEText(open(file_path2, 'rb').read(), 'base64', 'gb2312')
        att_txt2["Content-Type"] = 'application/octet-stream'
        att_txt2.add_header("Content-Disposition", 'attachment', filename=file_name2)
        message.attach(att_txt2)



    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(msg_from, passwd)
    try:
        server.sendmail(msg_from, msg_to, message.as_string())
        server.close()
        print('本轮测试完成，请尽快查看测试数据和相关log，有问题尽快反馈给开发大佬们哦！')
    except:
        print('发送失败')


if __name__ == '__main__':
    msg_from = '937643549@qq.com'  # 你的邮箱地址
    passwd = 'irylqahuuqxtbfbj'  # 你邮箱的授权码
    subject = '杀进程重连压测报告'  # 邮件主题
    msg_to = '1462940090@qq.com' # 收件邮箱地址
    content = '测试结果：' \
                  '1、本轮测试完成，请尽快查看测试数据和相关log' \
                  '2、相关数据汇总请手动执行' \
                  '3、有问题尽快反馈给开发大佬们哦'  # 邮件正文
        # 没有附件可以省略不写
    file_path1 = r'G:\py\sumian\kill\killAPP.log'  # 添加附件1的路径
    file_name1 = 'kliiAPP.log'  # 添加附件1的名字

    file_path2 = r'G:\py\sumian\kill\killAPP_Result.txt'  # 添加附件2的路径
    file_name2 = 'killAPP_Result.txt'  # 添加附件2的名字

        # 1.发送带附件的qq邮件
    sendEmail(msg_from, passwd, subject, msg_to, content, file_path1, file_path2, file_name1, file_name2)
        # 2.发送不带附件的qq邮件
    # sendEmail(msg_from, passwd, subject, msg_to, content)





