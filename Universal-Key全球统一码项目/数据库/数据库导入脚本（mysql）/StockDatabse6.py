#coding:utf-8
import xlrd
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="1017",db="isonukdb",charset="utf8")
cursor = conn.cursor()
sql = "insert into ukey(ukid,jycode,windcode,markid,exchangeid,secutype1,secutype2," \
      "ccy,expiremonth,codeid,futurespriceid,futurestypeid,spmonthdiff,sptypea,sptypeb,stockfu_priceid,stockfu_typeid,exchangerate_ccya," \
      "exchangerate_ccyb,exchangerate_ccy,exchratefu_ccya,exchratefu_ccyb,exchratefu_ccy) " \
      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

data = xlrd.open_workbook('ukey.xlsx')
table = data.sheet_by_name(u'Sheet1')
nrows = table.nrows
ncols = table.ncols
ukey = []
stock = []
for i in range(nrows):
    if i == 0:
        continue
    for j in range(ncols):
        if j == 2 or j==0:
            stock.append(table.cell(i,j).value)
        else:
            stock.append(int(table.cell(i,j).value))
    ukey.append(tuple(stock))
    stock = []
print ukey
cursor.executemany(sql,ukey)
cursor.close()
conn.commit()
conn.close()
