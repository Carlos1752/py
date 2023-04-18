import time
import sys

#开始倒计时
totalTime = 10  # 倒计时x秒
while totalTime > 0:
    print('还剩%d秒' % totalTime)
    time.sleep(1)
    totalTime -= 1
