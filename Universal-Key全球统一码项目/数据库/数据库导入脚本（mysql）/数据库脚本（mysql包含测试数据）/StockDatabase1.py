#coding:utf-8
import xlrd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="isonukdb",charset="utf8")
cursor = conn.cursor()
sql = "insert into futures_information(futuresid,markid,exchangeid,jycode,windcode,futypeid2,contoptionid,contmutil," \
      "priunit,ticksize,dailychgrange,contmonth,trdate,lasttrdate,lasttrtime,deliverydate," \
      "lastdeliverydate,deliverygrade,deliverymethod,settpricecode,Settpricedesc,deliseprice,conttrrate,conttrfee,condeliveryfee) " \
      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
data = xlrd.open_workbook('futures_information.xlsx')
table = data.sheet_by_name(u'Sheet1')
nrows = table.nrows
ncols = table.ncols
futures_information = []
stock = []
for i in range(nrows):
    if i == 0:
        continue
    for j in range(ncols):
        if j == 0 or j ==1 or j==2 or j==3 or j==5 or j==17 or j==18 or j==19:
            stock.append(int(table.cell(i,j).value))
        else:
            if  j == 21 or j == 22 or j == 23 or j==24:
                stock.append(float(table.cell(i,j).value))
            else:
                stock.append(table.cell(i,j).value)
    futures_information.append(tuple(stock))
    stock = []
print futures_information
cursor.executemany(sql,futures_information)
cursor.close()
conn.commit()
conn.close()

