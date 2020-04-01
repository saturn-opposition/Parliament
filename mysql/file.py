import pymysql
import csv
import os

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接

xml_files = []
raw_xml_files = []
# for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\lords"):
#
#    raw_xml_files.append(files)
#
#
# for s in range(len(raw_xml_files[0])):
#     xml_files.append("C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords" + raw_xml_files[0][s])
#
#
# for i in range(len(xml_files)):
#     file_id = 'f'+str(i)
#     file_name = raw_xml_files[0][i]
#     row = cursor.execute(
#         "insert into file(file_id ,file_name,type)values(%s, %s,%s)",
#         (file_id,file_name,'lords'))
#     print('已插入'+'lords'+file_name)
#     conn.commit()
xml_files = []
raw_xml_files = []

for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\commons"):

   raw_xml_files.append(files)

for s in range(len(raw_xml_files[0])):
    xml_files.append('C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\commons\\' + raw_xml_files[0][s])
t = 3612
for i in range(len(xml_files)):
    file_id = 'f'+str(t)
    file_name = raw_xml_files[0][i]
    row = cursor.execute(
        "insert into file(file_id ,file_name,type)values(%s, %s,%s)",
        (file_id,file_name,'commons'))
    t = t + 1

    conn.commit()
    print('已插入' + 'commons' + file_name)
cursor.close()
conn.close()


