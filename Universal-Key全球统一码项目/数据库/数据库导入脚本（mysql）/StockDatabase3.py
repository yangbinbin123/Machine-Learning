#coding:utf-8
import xlrd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="isonukdb",charset="utf8")
cursor = conn.cursor()
sql = "insert into references_data(ukid,codeid,compcodeid,markid,exchangeid,secutype,ccy,volume,amt,position," \
      "positionchange,preclear,preclose,open,high,low,last,close,handnums,netasset,totalvolume,tradevolume," \
      "stat,suspendtime,suspendflg,descb,updatetime) " \
      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

data = xlrd.open_workbook('references_data.xlsx')
table = data.sheet_by_name(u'Sheet1')
nrows = table.nrows
ncols = table.ncols
references_data = []
stock = []
for i in range(nrows):
    if i == 0:
        continue
    for j in range(ncols):
        if j == 1 or j ==2 or j ==3 or j ==4 or j ==5 or j==6 or j==18 or j==22 or j==24:
            stock.append(int(table.cell(i,j).value))
        else:
            if j==7 or j==8 or j==9 or j==10 or j==11 or j==12 or j==13 or j==14 or j==15 or j==16 or j==17 or j==19 or j==20 or j==21:
                stock.append(float(table.cell(i,j).value))
            else:
                stock.append(table.cell(i,j).value)
    references_data.append(tuple(stock))
    stock = []
print references_data
cursor.executemany(sql,references_data)
cursor.close()
conn.commit()
conn.close()
