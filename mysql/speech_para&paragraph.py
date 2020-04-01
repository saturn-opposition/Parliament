import pymysql
from  xml.etree import ElementTree as ET
import csv
import os
country = []
country_abb = []
capital = []
country_fullname = []
with open(r"C:\Users\hjn\Desktop\大创项目准备\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[1] for row in reader]
with open(r"C:\Users\hjn\Desktop\大创项目准备\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country_abb = [row[2] for row in reader]
with open(r"C:\Users\hjn\Desktop\大创项目准备\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country_fullname = [row[4] for row in reader]
with open(r"C:\Users\hjn\Desktop\大创项目准备\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    capital = [row[5] for row in reader]
country.pop(0)
country_abb.pop(0)
country_fullname.pop(0)
capital.pop(0)

for i in range(len(country_fullname)):
    country_fullname[i] = country_fullname[i].strip()            #去掉空格

for i in range(len(capital)):
    capital[i] = country_fullname[i].strip()            #去掉空格



conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接
# cursor.execute("select speech_id,meeting_id from meeting_speech")
#
# row = cursor.fetchall()
# speech_id = row[0]                                           #speech_id和meeting_id对应，speech在所有范围内都是独一无二的
# meeting_id = row[1]
# file_id = []
# xml_files = []
# for i in range(len(meeting_id)):
#     cursor.execute("select file_id from meeting_file where meeting_id = "+ meeting_id[i])
#     row = cursor.fetchall()
#     file_id=row[0]
#     for f in range(len(file_id)):
#         cursor.execute("select file_name,type from file where file_id = " + file_id[f])
#         row = cursor.fetchall()
#         file_name = row[0]
#         type = row[1]
#         xml_files.append('C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\' + type[0] + '\\' + file_name[0]) #一个meeting_id有多个xml文件
count = 0
def one_xml(file_loc):

    global country
    global country_fullname
    global country_abb
    global capital
    global count
    major_heading_id = ''
    minor_heading_id = ''
    root = ET.parse(file_loc)

    for node in root.findall('speech'):
        s_id = node.get('id')
        if s_id == None:
            s_id = 'no_speech_id'
        for p in node.findall('p'):
                if p!= None:
                    p_id = p.get('pid')

                    if p_id !=None:
                        para_content = p.text
                        para_id = 'p'+str(count)

                        s = str.lower(para_content)
                        thisp_country = []

                        wordslist = para_content.split()
                        for w in range(len(wordslist)):
                            for t in range(len(country_abb)):
                                    if country_abb[t]== w:
                                        thisp_country.append(country[t])


                        for k in range(len(capital)):
                            if capital[k].lower() in s:
                                thisp_country.append(country[k])
                        for j in range(len(country)):
                            if country[j].lower() in s:
                                thisp_country.append(country[j])
                            elif country_fullname[j].lower() in s:
                                thisp_country.append(country[j])

                        thisp_country = set(thisp_country)
                        para_involve_country_count = len(thisp_country)
                        para_involve_country = ';'.join(thisp_country)+';'


                        row = cursor.execute(
                            "insert into paragraph(para_id ,para_content,para_involve_country,para_involve_country_count,pid)values(%s, %s,%s,%s,%s)",
                            (para_id, para_content, para_involve_country, para_involve_country_count,p_id ))
                        row = cursor.execute(
                            "insert into speech_para(speech_id ,para_id,number_sp)values(%s, %s,%s)",
                            (s_id, para_id,1))
                        conn.commit()





xml_files = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\lords"):
   xml_files.append(files)


for s in range(len(xml_files[0])):

    xml_files[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords\\' + xml_files[0][s]

xml_files = xml_files[0]

for i in range(len(xml_files)):
    one_xml(xml_files[i])
    print('已完成'+xml_files[i])




conn.commit()
cursor.close()
conn.close()
