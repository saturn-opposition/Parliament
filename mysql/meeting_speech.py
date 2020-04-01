import pymysql
from  xml.etree import ElementTree as ET
import os
import re

conn = pymysql.connect(host='129.204.72.246', port=3306, user='root', passwd='123456', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接
cursor.execute("select meeting_id,date,type from meeting")
row = cursor.fetchall()
meeting_id = []
date = []
type = []
for i in range(len(row)):
    meeting_id.append(row[i][0])
    date.append(row[i][1])
    type.append(row[i][2])

cursor.execute("select speech_id from speech")
row = cursor.fetchall()
exist_speech_id = []
for i in range(len(row)):
    exist_speech_id.append(row[i][0])
cursor.execute("select number_ms from meeting_speech")
row = cursor.fetchall()
number_ms = []
num_ms = 0
for i in range(len(row)):
    number_ms.append(row[i][0])
    tmp_num_ms = int(re.sub("\D", "", row[i][0]))
    if tmp_num_ms>num_ms:
        num_ms = tmp_num_ms

num_ms = num_ms + 1

# xml_files = []
# for root, dirs, files in os.walk(r"议会数据/lords"):
#    xml_files.append(files)
# for s in range(len(xml_files[0])):
#     xml_files[0][s] =  '议会数据/lords/' + xml_files[0][s]
# xml_files = xml_files[0]

def one_xml(file_path):
    global meeting_id
    global date
    global num_ms
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
            "insert into meeting_speech(meeting_id ,speech_id,number_ms)values(%s, %s,%s)",
            (m_id, speech_id, num_ms))
            conn.commit()
            num_ms = num_ms + 1

# for i in range(len(xml_files)):
#     one_xml(xml_files[i])
#     print('已完成'+xml_files[i])

one_xml(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\commons\1945-06-14a.xml")
conn.commit()
cursor.close()
conn.close()





































# for i in range(len(row)):
#    meeting_id.append(row[i][0])
#    file_id.append(row[i][1])
#
# xml_files = []
# for root, dirs, files in os.walk(r"议会数据/lords"):
#    xml_files.append(files)
#
#
# for s in range(len(xml_files[0])):
#
#     xml_files[0][s] =  '议会数据/lords/' + xml_files[0][s]
#
# xml_files = xml_files[0]
# cursor.execute("select speech_id from speech")
# row = cursor.fetchall()
# exist_speech_id = []
# for i in range(len(row)):
#     exist_speech_id.append(row[i][0])
# count = 0
# def one_xml(file_loc,m):
#     global meeting_id
#     global count
#     global exist_speech_id
#     root = ET.parse(file_loc)
#
#     for node in root.findall('speech'):
#         speech_id = node.get('id')
#         if speech_id in exist_speech_id:
#             row = cursor.execute(
#             "insert into meeting_speech(meeting_id ,speech_id,number_ms)values(%s, %s,%s)",
#             (meeting_id[m], speech_id, count))
#             conn.commit()
#             count = count + 1
#
#
#
#
# for i in range(len(xml_files)):
#     one_xml(xml_files[i],i)
#     print('已完成'+xml_files[i])
#
#
# conn.commit()
# cursor.close()
# conn.close()
