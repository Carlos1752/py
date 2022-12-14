import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import win32api
import smtplib

f = open("G:\py\sumian\OTA\OTA_Result.txt",encoding="ANSI")#公司电脑路径
# f = open("D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\OTA\OTA_Result.txt", encoding="ANSI")  # 个人电脑路径
print(f.read())
f.close()
time.sleep(3)


# 开始构建邮件内容
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
    # 构造附件
        att_txt1 = MIMEText(open(file_path1, 'rb').read(), 'base64', 'gb2312')
        att_txt1["Content-Type"] = 'application/octet-stream'
        att_txt1.add_header("Content-Disposition", 'attachment', filename=file_name1)
        message.attach(att_txt1)
    # 构造附件2
        att_txt2 = MIMEText(open(file_path2, 'rb').read(), 'base64', 'gb2312')
        att_txt2["Content-Type"] = 'application/octet-stream'
        att_txt2.add_header("Content-Disposition", 'attachment', filename=file_name2)
        message.attach(att_txt2)
    # 构造图片1
        att_img = MIMEText(open(file_path3, 'rb').read(), 'base64', 'gb2312')
        att_img["Content-Type"] = 'application/octet-stream'
        att_img.add_header("Content-Disposition", 'attachment', filename=file_name3)
        message.attach(att_img)

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
    subject = 'OTA压测报告'  # 邮件主题
    msg_to = '1462940090@qq.com'  # 收件邮箱地址
    content = '本轮测试完成，请尽快查看测试数据和相关log，有问题尽快反馈给开发大佬们哦'  # 邮件正文
    # 没有附件可以省略不写
    file_path1 = r'G:\py\sumian\OTA\OTA.log'  # 添加附件1的路径,公司电脑
    # file_path1 = r'D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\OTA\OTA.log'  # 个人电脑
    file_name1 = 'OTA.log'  # 添加附件1的名字

    file_path2 = r'G:\py\sumian\OTA\OTA_Result.txt'  # 添加附件2的路径，公司电脑
    # file_path2 = r'D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\OTA\OTA_Result.txt'  # 个人电脑
    file_name2 = '运行结果汇总.txt'  # 添加附件2的名字

    file_path3 = r'G:\py\sumian\OTA\20220927181802.png'  # 添加附件中图片的路径，公司电脑
    # file_path3 = r'D:\ProgramFiles\JetBrains\PycharmProjects\sumian\py\sumian\OTA\20220927181802.png'  # 个人电脑
    file_name3 = '亮剑.png'  # 添加图片的名字

    # 1.发送带附件的qq邮件
    sendEmail(msg_from, passwd, subject, msg_to, content, file_path1, file_path2, file_path3, file_name1, file_name2,
              file_name3)
    # 2.发送不带附件的qq邮件
    # sendEmail(msg_from, passwd, subject, msg_to, content)
