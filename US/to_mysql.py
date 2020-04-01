import pymysql
import os
import csv
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='US', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接
file_name = []
for files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\美国议会数据pdf\downloadpdf"):
   file_name = files[2]

country = []
country_abb = ['US','UN','JP','CN']
country_abb_n = ['United States','United Kingdom','Japan','China']
capital = []
country_fullname = []
with open(r"C:\Users\hjn\Desktop\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[1] for row in reader]
with open(r"C:\Users\hjn\Desktop\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    capital = [row[5] for row in reader]
with open(r"C:\Users\hjn\Desktop\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country_fullname = [row[4] for row in reader]
country.pop(0)
capital.pop(0)
country_fullname.pop(0)
for i in range(len(capital)):
    capital[i] = capital[i].strip()            #去掉空格
    country_fullname[i] = country_fullname[i].strip()


for i in range(len(file_name)):
   date = file_name[i][5:15]
   file_path = "C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\美国议会数据txt\\"+file_name[i][0:-4]+'.txt'
   f = open(file_path, 'r', encoding='utf-8')
   doc = f.read()
   f.close()
   words = doc.split()
   country_list = []
   print('1')
   for j in range(len(words)):
       for k in range(len(country)):
           if words[j] == country[k]:
               country_list.append(words[j])
           if words[j] == capital[k]:
               country_list.append(country[k])
       for t in range(len(country_abb)):
           if words[j] == country_abb[t]:
               country_list.append(country_abb_n[t])
   for j in range(len(country_fullname)):
        if country_fullname[j] in doc:
            country_list.append(country[j])
   country_list = list(set(country_list))
   country_str = ';'.join(country_list)
   row = cursor.execute(
         "insert into file(FILE_NAME,DATE,INVOLVE_COUNTRY)values(%s, %s,%s)",
         (file_name[i],date,country_str))
   conn.commit()
   print(file_name[i]+'已完成')