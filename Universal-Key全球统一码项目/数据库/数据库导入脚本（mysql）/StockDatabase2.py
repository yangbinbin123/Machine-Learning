#coding:utf-8
import xlrd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="isonukdb",charset="utf8")
cursor = conn.cursor()
sql = "insert into futures_quotations(trday,ukid,codeid,markid,exchangeid,contoptionid," \
      "highlimit,lowlimit,preclear,preclose,open,high,low,last,close,volume,amt,clear," \
      "deliverydate,position,positionchange,stat,updatetime) " \
      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

data = xlrd.open_workbook('futures_quotations.xlsx')
table = data.sheet_by_name(u'Sheet1')
nrows = table.nrows
ncols = table.ncols
futures_quotations = []
stock = []
for i in range(nrows):
    if i == 0:
        continue
    for j in range(ncols):
        if j ==2 or j ==3 or j ==4 or j ==5:
            stock.append(int(table.cell(i,j).value))
        else:
            if j==6 or j==7 or j==8 or j==9 or j==10 or j==11 or j==12 or j==13 or j==14 or j==15 or j==16 or j==17 or j==19 or j==20:
                stock.append(float(table.cell(i,j).value))
            else:
                stock.append(table.cell(i,j).value)
    futures_quotations.append(tuple(stock))
    stock = []
print futures_quotations
cursor.executemany(sql,futures_quotations)
cursor.close()
conn.commit()
conn.close()
