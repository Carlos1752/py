import os
import subprocess
import sys
import uiautomator2 as ut2
import logging

# 连接手机 ADB
devices = str(subprocess.check_output('adb devices')).replace(" ", "") \
    .replace("b'Listofdevicesattached", "").replace("device", "").replace("\\", "").replace("rn", "").replace("t'", "")
assert ut2.connect(devices), "请在cmd里输入adb devices确认设备是否存在"
device = ut2.connect(devices)

if devices != 'c7cff486' and devices != 'c23d076' and devices != '94a138a9' and devices != 'PZ8XW4SSOF69TKZH':  # nubia Z7mini手机,360N5，坚果手机
    print("未连接指定设备")
    sys.exit()
    # 判断是否指定的设备存在，如果不一致就结束

else:
    print(devices)
    os.system('adb shell wm size')  # 打印手机分辨率
    # 判断是否指定的设备存在，如果一致就继续，且打印出设备名称

print("请输入次数：", end="")
cycle_index = int(input())
logging.info('总测试次数：'+str(cycle_index))#打印本次要测试总次数