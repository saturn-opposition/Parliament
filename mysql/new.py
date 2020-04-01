import pymysql
from  xml.etree import ElementTree as ET
import os
import re
import csv
country = []
country_abb = ['US','UN','JP','CN']
country_abb_n = ['United States','United Kingdom','Japan','China']
capital = []
country_fullname = []
with open(r"世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[1] for row in reader]
with open(r"世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    capital = [row[5] for row in reader]
with open(r"世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country_fullname = [row[4] for row in reader]
country.pop(0)
capital.pop(0)
country_fullname.pop(0)
for i in range(len(capital)):
    capital[i] = capital[i].strip()            #去掉空格
    country_fullname[i] = country_fullname[i].strip()




conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接


cursor.execute("select speech_id from speech")
row = cursor.fetchall()
exist_speech_id = []
for i in range(len(row)):
    exist_speech_id.append(row[i][0])

cursor.execute("select major_heading_id from major_heading")
row = cursor.fetchall()
exist_majorheading_id = []
for i in range(len(row)):
    exist_majorheading_id.append(row[i][0])

cursor.execute("select minor_heading_id from minor_heading")
row = cursor.fetchall()
exist_minorheading_id = []
for i in range(len(row)):
    exist_minorheading_id.append(row[i][0])

cursor.execute("select speaker_id from speaker")
row = cursor.fetchall()
exist_speaker_id = []
for i in range(len(row)):
    exist_speaker_id.append(row[i][0])

cursor.execute("select meeting_id,date,type from meeting")
row = cursor.fetchall()
meeting_id = []
date = []
type = []
for i in range(len(row)):
    meeting_id.append(row[i][0])
    date.append(row[i][1])
    type.append(row[i][2])


def speech(file_loc):
    global exist_speech_id
    global exist_speaker_id
    global exist_majorheading_id
    global exist_minorheading_id

    root = ET.parse(file_loc)
    major_heading_id = ''
    minor_heading_id = ''
    major_heading_name = ''
    major_url=''
    minor_heading_name = ''
    minor_url = ''

    for node in root.iter():
        if (node.tag == 'minor-heading'):
            major_heading_id = node.get('id')
            major_heading_name = node.text
            major_url = node.get('url')
            major_column = node.get('column')
            if major_url ==None:
                major_url = ''
            if major_column ==None:
                major_column = -1
            if major_heading_id not in exist_majorheading_id:
                row = cursor.execute(
                "insert into major_heading(major_heading_id ,major_heading_name,url,colnum)values(%s, %s,%s,%s)",
                (major_heading_id,major_heading_name,major_url,major_column))
                exist_majorheading_id.append(major_heading_id)
            conn.commit()
        if (node.tag == 'major-heading'):
            minor_heading_id = node.get('id')
            minor_heading_name = node.text
            minor_url = node.get('url')
            minor_column = node.get('column')
            if minor_url == None:
                minor_url = ''
            if minor_column == None:
                minor_column = -1
            if minor_heading_id not in exist_minorheading_id:
                row = cursor.execute(
                "insert into minor_heading(minor_heading_id ,minor_heading_name,url,colnum)values(%s, %s,%s,%s)",
                (minor_heading_id, minor_heading_name, minor_url, minor_column))
                exist_minorheading_id.append(minor_heading_id)
            conn.commit()
        if node.tag == 'speech':
            s_id = node.get('id')
            spea_id = node.get('speakerid')
            speaker_name = node.get('speakername')
            url = 'https://www.publicwhip.org.uk/mp.php?id=' + spea_id
            hansard_membership_id = node.get('hansard_membership_id')

            if major_heading_id =='':
                major_heading_id = 'no_major_heading'
            if minor_heading_id =='':
                minor_heading_id = 'no_minor_heading'
            if spea_id==None:
                spea_id = 'no_speaker'
            elif spea_id not in exist_speaker_id:
                row = cursor.execute(
                    "insert into speaker(speaker_id ,speaker_name,url,hansard_membership_id)values(%s, %s,%s,%s)",
                    (spea_id, speaker_name, url, hansard_membership_id))
                conn.commit()
                exist_speaker_id.append(spea_id)

            row = cursor.execute(
                    "insert into speech(speech_id ,speaker_id,major_heading_id,minor_heading_id)values(%s, %s,%s,%s)",
                    (s_id,spea_id,major_heading_id,minor_heading_id))
            exist_speech_id.append(s_id)
            conn.commit()

cursor.execute("select para_id from paragraph")
row = cursor.fetchall()
para_id = []
count = 0
for i in range(len(row)):
    para_id.append(row[i][0])
    tmp_count = int(re.sub("\D", "", row[i][0]))
    if tmp_count>count:
        count = tmp_count

count = count + 1


def speech_paragraph(file_loc):

    global country
    global country_fullname
    global country_abb
    global country_abb_n
    global capital
    root = ET.parse(file_loc)

    for node in root.findall('speech'):
        s_id = node.get('id')
        if s_id == None:
            s_id = 'no_speech_id'
        for p in node.findall('p'):
                if p!= None:
                    p_id = p.get('pid')
                    para_content = p.text
                    para_id = 'p'+str(count)
                    s = str.lower(para_content)
                    thisp_country = []

                    wordslist = para_content.split()
                    for w in range(len(wordslist)):
                        for t in range(len(country_abb)):
                                if country_abb[t]== w:
                                     thisp_country.append(country_abb_n[t])


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
                            "insert into speech_para(speech_id ,para_id)values(%s, %s)",
                            (s_id, para_id))
                    conn.commit()
                    count = count + 1

def meeting_speech(file_path):
    global meeting_id
    global date
    global exist_speech_id
    global type
    m_id = ''
    for j in range(len(date)):
        if (str(date[j]) in file_path)&(type[j]=='lords'):
            m_id = meeting_id[j]
    root = ET.parse(file_path)
    for node in root.findall('speech'):
        speech_id = node.get('id')
        if speech_id in exist_speech_id:
            row = cursor.execute(
            "insert into meeting_speech(meeting_id ,speech_id)values(%s, %s)",
            (m_id, speech_id))
            conn.commit()


xml_files = []
for root, dirs, files in os.walk(r"议会数据/lords"):
   xml_files.append(files)


for s in range(len(xml_files[0])):

    xml_files[0][s] =  '议会数据/lords/' + xml_files[0][s]

xml_files = xml_files[0]

cursor.execute("select meeting_id,date,type from meeting where involve_country is null")
row = cursor.fetchall()
m_id = []
d = []
t = []
for i in range(len(row)):
    m_id.append(row[i][0])
    d.append(row[i][1])
    t.append(row[i][2])

for i in range(len(xml_files)):
    for j in range(d):
        if d[j] in xml_files[i] & t[j] =='lords':
            speech(xml_files[i])
            speech_paragraph((xml_files[i]))
            meeting_speech(xml_files[i])








