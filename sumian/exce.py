import xlsxwriter as xw

with open('G:\\py\\sumian\\kill\\killAPP_Result.txt') as file_object:
    lines = file_object.readlines() # 以行的形式进行读取文件
    file_object.close()# 关闭文件


workbook = xw.Workbook('G:/py/sumian/日志分析.xlsx')
sheet0 = workbook.add_worksheet('测试结果1') # 第一页sheet表命名为“语音台数据”
# sheet1 = workbook.add_worksheet('测试结果2')# 第二页sheet表命名为“数据台数据”
centered = workbook.add_format({'align': 'center'})     # 写excel的单元格，使用的对齐方式：居中
sheet0.write(1, 0, '很快', centered)# 第一页sheet标题命名为“时间”“场强数据”
sheet0.write(0, 1, '次数', centered)# 第一页sheet标题命名为“时间”“场强数据”
sheet0.write(2, 0, '中', centered)# 第一页sheet标题命名为“时间”“场强数据”
sheet0.write(3, 0, '慢', centered)# 第一页sheet标题命名为“时间”“场强数据”
sheet0.write(4, 0, '失败', centered)# 第一页sheet标题命名为“时间”“场强数据”

# sheet1.write(0, 0, '时间', centered)# 第二页sheet标题命名为“时间”“场强数据”
# sheet1.write(0, 1, '场强数据', centered)# 第二页sheet标题命名为“时间”“场强数据”


i = 1
for line1 in lines:

    if "很快" in line1:
        line1 = line1.strip('\n') # 去掉换行符
        line1 = line1.split('\t')# 去掉缩进符
        print(line1) # 打印line1结果，可不用
        time2 = line1[0]# 赋值第一列
        data2 = line1[2]# 赋值第二列

        sheet0.write(i, 0, time2, )# sheet1表写入第一列
        sheet0.write(i, 1, data2, )# sheet1表写入第二列
        i += 1
#
#
#
#
# i = 1
# for line2 in lines:
#
#     if "比较慢" in line2:
#         line2 = line2.strip('\n')
#         line2 = line2.split('\t')
#         time1 = line2[0]
#         data1 = line2[2]
#
#         sheet0.write(i, 0, time1, )
#         sheet0.write(i, 2, data1, )
#
#         i += 1
workbook.close()
