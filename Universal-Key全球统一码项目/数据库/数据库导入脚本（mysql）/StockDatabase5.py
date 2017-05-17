#coding:utf-8
import xlrd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="isonukdb",charset="utf8")
cursor = conn.cursor()
sql = "insert into shares_quotations(trday,ukid,codeid,markid,exchangeid,highlimit,lowlimit,preclear,preclose,open," \
      "high,low,last,close,volume,amt,clear,stat,updatetime) " \
      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

data = xlrd.open_workbook('shares_quotations.xlsx')
table = data.sheet_by_name(u'Sheet1')
nrows = table.nrows
ncols = table.ncols
shares_quotations = []
stock = []
for i in range(nrows):
    if i == 0:
        continue
    for j in range(ncols):
        if j ==2 or j ==3 or j ==4:
            stock.append(int(table.cell(i,j).value))
        else:
            if j==5 or j ==6 or j==7 or j==8 or j==9 or j==10 or j==11 or j==12 or j==13 or j==14 or j==15 or j==16 :
                stock.append(float(table.cell(i,j).value))
            else:
                stock.append(table.cell(i,j).value)
    shares_quotations.append(tuple(stock))
    stock = []
print shares_quotations
cursor.executemany(sql,shares_quotations)
cursor.close()
conn.commit()
conn.close()
