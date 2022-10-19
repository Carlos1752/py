import time
import sys
# import tkinter as tk
#
# root = tk.Tk()
# root.title("倒计时")
# root.geometry("114x514")


#开始倒计时
totalTime = 100  # 倒计时160秒
while totalTime > 0:
    print('还剩%d秒' % totalTime)
    time.sleep(10)
    totalTime -= 10

# b = 50
# def addone():
#     global b
#     b -= 10
#     print(b)
#
# a = tk.Button(root,text="你楸啥",command = addone).pack()
# root.mainloop()