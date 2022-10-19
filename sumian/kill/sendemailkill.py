import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import win32api
import smtplib
import logging.config
import logging


# txt = "D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\kill\killAPP_Result.txt"  # 自己的惠普笔记本电脑路径
txt = "G:\py\sumian\kill\killAPP_Result.txt"  #公司电脑路径
f = open(txt,encoding="ANSI")
print(f.read())
f.close()
time.sleep(3)

#开始构造邮件内容
def sendEmail(msg_from, passwd, subject, msg_to, content, file_path1='', file_path2='', file_path3='', file_name1='',
              file_name2='', file_name3=''):
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = msg_from
    message['To'] = msg_to

    # 邮件正文内容
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    if file_path1 != '' and file_path2 != '' and file_path3 != '':
        # 构造附件1
        att_txt1 = MIMEText(open(file_path1, 'rb').read(), 'base64', 'gb2312')
        att_txt1["Content-Type"] = 'application/octet-stream'
        att_txt1.add_header("Content-Disposition", 'attachment', filename=file_name1)
        message.attach(att_txt1)
        # 构造附件2
        att_txt2 = MIMEText(open(file_path2, 'rb').read(), 'base64', 'gb2312')
        att_txt2["Content-Type"] = 'application/octet-stream'
        att_txt2.add_header("Content-Disposition", 'attachment', filename=file_name2)
        message.attach(att_txt2)

        # 构造附件3
        att_txt3 = MIMEText(open(file_path3, 'rb').read(), 'base64', 'gb2312')
        att_txt3["Content-Type"] = 'application/octet-stream'
        att_txt3.add_header("Content-Disposition", 'attachment', filename=file_name3)
        message.attach(att_txt3)

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
    msg_to = '1462940090@qq.com'  # 收件邮箱地址
    content = '测试结果：' \
              '1、本轮测试完成，请尽快查看测试数据和相关log' \
              '2、相关数据汇总请手动执行' \
              '3、有问题尽快反馈给开发大佬们哦'  # 邮件正文

    # 没有附件可以省略不写
    file_path1 = r'G:\py\sumian\kill\killAPP.log'  # 添加附件1的路径,公司电脑
    # file_path1 = r'D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\kill\killAPP.log'  # 自己惠普笔记本电脑路径
    file_name1 = 'kliiAPP.log'  # 添加附件1的名字

    file_path2 = r'G:\py\sumian\kill\killAPP_Result.txt'  # 添加附件2的路径，公司电脑
    # file_path2 = r'D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\kill\killAPP_Result.txt'  # 自己惠普笔记本电脑路径
    file_name2 = 'killAPP_Result.txt'  # 添加附件2的名字

    file_path3 = r'G:\py\sumian\kill\1666141592992.jpg'  # 添加附件3的路径,公司电脑
    # file_path3 = r'D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\kill\killAPP_Result.txt'  # 自己惠普笔记本电脑路径
    file_name3 = '夕阳.jpg'  # 添加附件2的名字

    # 1.发送带附件的qq邮件
    sendEmail(msg_from, passwd, subject, msg_to, content, file_path1, file_path2, file_path3, file_name1, file_name2,
              file_name3)
    # 2.发送不带附件的qq邮件
    # sendEmail(msg_from, passwd, subject, msg_to, content)
