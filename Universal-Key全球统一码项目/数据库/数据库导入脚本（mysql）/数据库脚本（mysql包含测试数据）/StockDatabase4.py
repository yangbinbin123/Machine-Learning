#coding:utf-8
import xlrd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="isonukdb",charset="utf8")
cursor = conn.cursor()
sql = "insert into shares_information(sharesid,markid,exchangeid,jycode,windcode,chiname," \
      "chinameabbr,engname,engnameabbr,secuabbr,chispell,listplate,Liststate,listdate,delistdate,updatetime) " \
      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

data = xlrd.open_workbook('shares_information.xlsx')
table = data.sheet_by_name(u'Sheet1')
nrows = table.nrows
ncols = table.ncols
shares_information = []
stock = []
for i in range(nrows):
    if i == 0:
        continue
    for j in range(ncols):
        if j == 0 or j ==1 or j ==2 or j ==3 or j ==11 or j==12:
            stock.append(int(table.cell(i,j).value))
        else:
            stock.append(table.cell(i,j).value)
    shares_information.append(tuple(stock))
    stock = []
print shares_information
cursor.executemany(sql,shares_information)
cursor.close()
conn.commit()
conn.close()
