import pymysql
import csv
import os
from  xml.etree import ElementTree as ET

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接

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
capital.pop(0)                                           #国家词表导入

for i in range(len(country_fullname)):
    country_fullname[i] = country_fullname[i].strip()            #去掉空格
    capital[i] = capital[i].strip()

date = []
country_britain = []
type = []
file_count = []
involve_country = []  #文件层面的county
#以上都是文件层面
speech_id = []
para_id = []
para_content = []
para_involve_country = []
para_involve_country_count = []
speaker_id = []
major_heading_id = []
minor_heading_id = []
no_speaker = []
para_id = []

def one_xml(file_path):
    global para_involve_country
    global para_content
    global minor_heading_id
    global major_heading_id
    global speech_id
    global para_id
    global para_involve_ocuntry_count
    global speaker_id
    global no_speaker
    global para_id
    global involve_country
    thisfile_country = set()          #函数内的临时变量
    root = ET.parse(file_path)
    for node in root.iter():
        # if (node.tag == 'minor-heading'):
        #     minor_id = node.get('id')
        # if (node.tag == 'major-heading'):
        #     major_h = node.get('id')
        if (node.tag == 'p') & (node.text != None):

            para_id.append(node.get('pid'))
            para_content.append(node.text)
            sentences = node.text
            s = str.lower(sentences)
            thispara_involve_country = set()
            wordslist = sentences.split()
            for w in range(len(wordslist)):
                for t in range(len(country_abb)):
                    if country_abb[t] == wordslist[w]:
                            thisfile_country.add(country[t])
                            thispara_involve_country.add(country[t])
            for k in range(len(capital)):
                if capital[k].lower() in s:
                       thisfile_country.add(country[k])
                       thispara_involve_country.add(country[k])
            for j in range(len(country)):
                if country[j].lower() in s:
                        thisfile_country.add(country[j])
                        thispara_involve_country.add(country[j])
                if country_fullname[j].lower() in s:
                    thisfile_country.add(country[j])
                    thispara_involve_country.add(country[j])
            temp = list(thispara_involve_country)
            para_involve_country_count.append(len(temp))
            para_involve_country.append(';'.join(temp))
            temp = list(thisfile_country)
            thisfile_country_str = ';'.join(temp)



    return thisfile_country_str


xml_files_lords = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\lords"):
   xml_files_lords.append(files)


for s in range(len(xml_files_lords[0])):
    xml_files_lords[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords\\' + xml_files_lords[0][s]
xml_files_lords = xml_files_lords[0]
date_str = ''
country_str = ''
count = 1
for i in range(500):
    if date_str!=xml_files_lords[i][-15:-5]:
        date_str = xml_files_lords[i][-15:-5]
        date.append(date_str)
        file_count.append(count)
        type.append('lords')
        country_britain.append('Britain')
        involve_country.append(country_str)
        country_str = ''
        count = 0
    count = count + 1
    country_str = country_str + one_xml(xml_files_lords[i])
    print("成功完成文件"+xml_files_lords[i])

sql_data = []
for i in range(len(date)):
    t = (date[i],country_britain[i],type[i],file_count[i],involve_country[i])
    sql_data.append(t)
row = cursor.executemany("insert into meeting(date ,country, type,file_count,involve_country)values(%s, %s, %s,%s,%s)", sql_data)

sql_data = []
for i in range(len(para_id)):
    t = (para_id[i],para_content[i],para_involve_country[i],para_involve_country_count[i])
    sql_data.append(t)

row = cursor.executemany("insert into paragraph(para_id ,para_content, para_involve_country,para_involve_country_count)values(%s, %s, %s,%s)", sql_data)
conn.commit()
cursor.close()
conn.close()









