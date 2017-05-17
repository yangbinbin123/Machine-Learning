#coding:utf-8
import xlrd
from xlwt import Workbook
import MySQLdb

#16进制转换
def function_uk(code):
    result = ''
    warehouse = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
#无限循环使用了连续取余的方法得到16进制的每一位数字
    while 1:
        temp = divmod(code,16);
        code = temp[0]
        result = result + warehouse[temp[1]]
        if code == 0:
            break;
        else:
            continue;
    order = []
#这个循环用来逆序输出我们拼接的余数的字符串
    for i in result:
        order.append(i)
    order.reverse()
    return ''.join(order)



#2进制转换
def binary_SQE(code):
    f_result = '0000'
    result = ''
    while 1:
        temp = divmod(code,2)
        code = temp[0]
        result = result + str(temp[1])
        if code == 0:
            break
        else:
            continue
    order = []
    for i in result:
        order.append(i)
    order.reverse()
    final = ''.join(order)
    pc = 4-len(final)
    for i in range(pc,4):
        l = list(f_result)
        l[i] = final[i-4+len(final)]
        f_result = ''.join(l)
    return f_result

#解析16进制uk码
def Uk_ana(code):
    afterTransfer = ''
    warehouse = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for i in range (len(code)):
        for j in range(len(warehouse)):
            if code[i] == warehouse[j]:
                afterTransfer = afterTransfer + binary_SQE(j)
    return afterTransfer


choice = input("请问导入的产品的类型是什么？（1-股票 2-期货）")
if choice == 1:
    data = xlrd.open_workbook('test.xlsx')
    table = data.sheet_by_name(u'Sheet1')
    nrows = table.nrows
    ncols = table.ncols
    conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="datatest",charset="utf8")
    cursor = conn.cursor()
    sql = "insert into ukey(code,ukid,marketid,exchangeid,secutype1,secutype2,expiremonth) values(" \
          "%s,%s,%s,%s,%s,%s,%s)"
    sqlinfo = ['1',2,3,4,5,6,7]
    stock_temp = []
    stock = []
    goal_col = 0  #自动寻找名字为UK或者uk或者Uk的列(大小写自动转换)
    for i in range(nrows):
        if i == 0:
            for m in range(ncols):
                if table.cell(i,m).value.upper() == 'UK':
                    goal_col = m
                    continue
        else:
            temp = Uk_ana(table.cell(i,goal_col).value)
            print temp, i, nrows
            sqlinfo[0] = table.cell(i,1).value
            sqlinfo[1] = int(temp[32:64],2)
            sqlinfo[2] = int(temp[2:12],2)
            sqlinfo[3] = int(temp[2:12],2)
            sqlinfo[4] = int(temp[12:16],2)
            sqlinfo[5] = int(temp[16:20],2)
            sqlinfo[6] = int(temp[20:32],2)
            for i in range(0,7):
                stock_temp.append(sqlinfo[i])
            stock.append(tuple(stock_temp))
            stock_temp = []
    print stock
    cursor.executemany(sql,stock)
    cursor.close()
    conn.commit()
    conn.close()
#     book = Workbook()
#     sheet = book.add_sheet('Sheet1')
#     sheet.write(0,0,'code')
#     sheet.write(0,1,'CHName')
#     sheet.write(0,2,'ukcode') #第三列填写股票的完整uk代码
#     sheet.write(0,3,'ukid') #第四列填写股票的顺序码
#     sheet.write(0,4,'marketid') #第五列填写交易所代码
#     sheet.write(0,5,'marketid') #第六列填写交易所代码
#     sheet.write(0,6,'secutype1') #第七列填写大类
#     sheet.write(0,7,'secutype2') #第八列填写小类
#     sheet.write(0,8,'expiremonth') #第九列填写到期月份，股票为0
#     prefix = '40111000'
#     print prefix
#     for i in range(nrows):
#         if i == 0:
#             continue
#         else:
#             future_code = '00000000'
#             temp = function_uk(i)
#             change_cp = 8 - len(temp)
#             for h in range(0,len(temp)):
#                 l = list(future_code)
#                 l[change_cp] = temp[h]
#                 future_code = ''.join(l)
#                 change_cp = change_cp + 1
#             uk_code = prefix + future_code
#             print uk_code
#             sheet.write(i,0,table.cell(i,0).value)
#             sheet.write(i,1,table.cell(i,1).value)
#             sheet.write(i,2,uk_code) #第三列填写股票的完整uk代码
#             sheet.write(i,3,i) #第四列填写股票的顺序码
#             sheet.write(i,4,1) #第五列填写交易所代码
#             sheet.write(i,5,1) #第六列填写交易所代码
#             sheet.write(i,6,1) #第七列填写大类
#             sheet.write(i,7,1) #第八列填写小类
#             sheet.write(i,8,0) #第九列填写到期月份，股票为0
#     book.save('SZGPR.xls')
#
#     data_SEC = xlrd.open_workbook('SZGPR.xls')
#     table_SEC = data_SEC.sheet_by_name(u'Sheet1')
#     nrows = table_SEC.nrows
#     ncols = table_SEC.ncols
#     print ncols
#     print nrows
#     conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="datatest",charset="utf8")
#     cursor = conn.cursor()
#     sql = "insert into ukey(code,ukid,marketid,exchangeid,secutype1,secutype2,expiremonth) values(" \
#           "%s,%s,%s,%s,%s,%s,%s)"
#     ukey = []
#     stock = []
#     for i in range(nrows):
#         if i == 0:
#             continue
#         for j in range(ncols):
#             if j == 0:
#                 stock.append((table_SEC.cell(i,j).value))
#             else:
#                 if j == 3 or j == 4 or j == 5 or j == 6 or j == 7 or j == 8:
#                     stock.append(int(table_SEC.cell(i,j).value))
#         ukey.append(tuple(stock))
#         stock = []
#     print ukey
#     cursor.executemany(sql,ukey)
#     cursor.close()
#     conn.commit()
#     conn.close()
else:
    if choice == 2:
        book = Workbook()
        sheet = book.add_sheet('Sheet1')
        sheet.write(0,0,'ukid')
        sheet.write(0,1,'marketid')
        sheet.write(0,2,'exchangeid')
        sheet.write(0,3,'secutype1')
        sheet.write(0,4,'secutype2')
        sheet.write(0,5,'expiremonth')

        data = xlrd.open_workbook(u'金.xlsx')  #注意中文命名的文件
        table = data.sheet_by_name(u'Sheet1')
        nrows = table.nrows
        ncols = table.ncols
        conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="datatest",charset="utf8")
        cursor = conn.cursor()
        sql = "insert into ukey(ukid,marketid,exchangeid,secutype1,secutype2,expiremonth) values(" \
              "%s,%s,%s,%s,%s,%s)"
        sqlinfo = ['a','b','c','d','f','g']
        stock_temp = []
        stock = []
        goal_col = 0  #自动寻找名字为UK或者uk或者Uk的列(大小写自动转换)
        for i in range(nrows):
            if i == 0:
                for m in range(ncols):
                    if table.cell(i,m).value.upper() == 'UK':
                        goal_col = m
                        continue
            else:
                temp = Uk_ana(table.cell(i,goal_col).value)
                print temp
                sqlinfo[0] = i
                sqlinfo[1] = int(temp[2:12],2)
                sqlinfo[2] = int(temp[2:12],2)
                sqlinfo[3] = int(temp[12:16],2)
                sqlinfo[4] = int(temp[16:20],2)
                sqlinfo[5] = int(temp[20:32],2)
                for i in range(0,6):
                    stock_temp.append(sqlinfo[i])
                stock.append(tuple(stock_temp))
                stock_temp = []
        print stock
        cursor.executemany(sql,stock)
        cursor.close()
        conn.commit()
        conn.close()







