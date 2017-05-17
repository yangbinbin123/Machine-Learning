#coding:utf-8
import sqlite3
conn = sqlite3.connect('C:\Users\Bean\UK.db')
conn.execute('''CREATE TABLE uk_code_SZZZ
       (ExchangeID VARCHAR(3)  NOT NULL,
       ChinName  VARCHAR(50),
       UKID       VARCHAR(50)  NOT NULL,
       UKCLASS   VARCHAR(10)   NOT NULL,
       UK_CODE   VARCHAR(50)   NOT NULL
       );''')

f = open("ZZ.txt")
line = f.readline()
while line:
    temp =  line.strip()
    temp_1 = temp.split('\t')
    conn.execute("INSERT INTO uk_code_SZZZ (ExchangeID,ChinName, UKID, UKCLASS,UK_CODE) VALUES ('"+temp_1[0]+"','"+temp_1[1]+"','"+temp_1[2]+"','"+temp_1[3]+"','"+temp_1[4]+"')")
    conn.commit()
    line = f.readline()
conn.close()
