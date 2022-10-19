import time
import sys

#开始倒计时
totalTime = 100  # 倒计时160秒
while totalTime > 0:
    print('还剩%d秒' % totalTime)
    time.sleep(10)
    totalTime -= 10
