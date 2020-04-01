import pymysql
import csv
import os
from collections import Counter
number_mf = 0
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接
cursor.execute("select file_id,file_name,type from file")
row = cursor.fetchall()

file_id = []
file_name = []
type = []
file_date=[]
date_connect_type = []
for i in range(len(row)):
   file_id.append(row[i][0])
   file_name.append(row[i][1])
   type.append(row[i][2])
   if row[i][1][0:3]=='day':
        file_date.append(row[i][1][7:17])
   elif row[i][1][0:3]=='deb':
       file_date.append(row[i][1][7:17])
   else:
       file_date.append(row[i][1][0:10])

for i in range(len(type)):
    if type[i]=='lords':
        date_connect_type.append('lords'+file_date[i])
    elif type[i]=='commons':
        date_connect_type.append('commons'+file_date[i])
    else:
        print('error')

result = Counter(date_connect_type)

s_id = ''
count_id = 0

for date,count in result.items():
   s_id = 'm'+str(count_id)
   if date[0]=='l':
        d = date[5:]
        print(d)
        row = cursor.execute(
        "insert into meeting(date ,country,type,file_count,meeting_id)values(%s, %s,%s,%s,%s)",
        (d, 'UK', 'lords', count, s_id))  # 尚未插入包含国家
        conn.commit()
   elif date[0]=='c':
        d = date[7:]
        print(d)
        row = cursor.execute(
        "insert into meeting(date ,country,type,file_count,meeting_id)values(%s, %s,%s,%s,%s)",
        (d, 'UK', 'commons', count, s_id))  # 尚未插入包含国家
   conn.commit()
   count_id = count_id +1

for i in range(len(file_date)):
    cursor.execute("select meeting_id from meeting where date = \'"+file_date[i]+'\' and type =\''+type[i]+'\'')
    row = cursor.fetchall()

    meeting_id = row[0]
    row = cursor.execute(
        "insert into meeting_file(meeting_id ,file_id,number_mf)values(%s, %s,%s)",
        (meeting_id, file_id[i], number_mf))
    number_mf = number_mf + 1

conn.commit()
cursor.close()
conn.close()

