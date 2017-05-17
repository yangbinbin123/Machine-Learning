#coding:utf-8
import xlrd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="isonukdb",charset="utf8")
cursor = conn.cursor()
sql = "insert into exchange_information(exchangeid,exchangetype,enname,chname,markstat) values(%s,%s,%s,%s,%s)"
data = xlrd.open_workbook('exchange_information.xlsx')
table = data.sheet_by_name(u'Sheet1')
nrows = table.nrows
ncols = table.ncols
exchange_information = []
stock = []
for i in range(nrows):
    if i == 0:
        continue
    for j in range(ncols):
        if j == 0 or j ==1:
            stock.append(int(table.cell(i,j).value))
        else:
            stock.append(table.cell(i,j).value)
    exchange_information.append(tuple(stock))
    stock = []
print exchange_information
cursor.executemany(sql,exchange_information)
cursor.close()
conn.commit()
conn.close()
