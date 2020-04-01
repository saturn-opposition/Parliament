import pymysql
from  xml.etree import ElementTree as ET
import os

conn = pymysql.connect(host='129.204.72.246', port=3306, user='root', passwd='123456', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接


def one_xml(file_loc):
    global speech_id
    global speaker_id
    root = ET.parse(file_loc)
    major_heading_id = ''
    minor_heading_id = ''
    major_heading_name = ''
    major_url=''
    minor_heading_name = ''
    minor_url = ''
    saved_major = []
    saved_minor = []
    for node in root.iter():
        if (node.tag == 'minor-heading'):
            major_heading_id = node.get('id')
            # major_heading_name = node.text
            # major_url = node.get('url')
            # major_column = node.get('column')
            # if major_url ==None:
            #     major_url = ''
            # if major_column ==None:
            #     major_column = -1
            # if major_heading_id not in saved_major:
            #     row = cursor.execute(
            #     "insert into major_heading(major_heading_id ,major_heading_name,url,colnum)values(%s, %s,%s,%s)",
            #     (major_heading_id,major_heading_name,major_url,major_column))
            #     saved_major.append(major_heading_id)
            # conn.commit()
        if (node.tag == 'major-heading'):
            minor_heading_id = node.get('id')
            # minor_heading_name = node.text
            # minor_url = node.get('url')
            # minor_column = node.get('column')
            # if minor_url == None:
            #     minor_url = ''
            # if minor_column == None:
            #     minor_column = -1
            # if minor_heading_id not in saved_minor:
            #     row = cursor.execute(
            #     "insert into minor_heading(minor_heading_id ,minor_heading_name,url,colnum)values(%s, %s,%s,%s)",
            #     (minor_heading_id, minor_heading_name, minor_url, minor_column))
            #     saved_minor.append(minor_heading_id)
            # conn.commit()
        if node.tag == 'speech':
            s_id = node.get('id')
            spea_id = node.get('speakerid')

            if major_heading_id =='':
                major_heading_id = 'no_major_heading'
            if minor_heading_id =='':
                minor_heading_id = 'no_minor_heading'
            if spea_id==None:
                spea_id = 'no_speaker'

            row = cursor.execute(
                    "insert into speech(speech_id ,speaker_id,major_heading_id,minor_heading_id)values(%s, %s,%s,%s)",
                    (s_id,spea_id,major_heading_id,minor_heading_id))
            conn.commit()



# xml_files = []
# for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\lords"):
#    xml_files.append(files)
#
#
# for s in range(len(xml_files[0])):
#
#     xml_files[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords\\' + xml_files[0][s]
#
# xml_files = xml_files[0]
#
# for i in range(len(xml_files)):
#     one_xml(xml_files[i])
#     print('已完成'+xml_files[i])

one_xml(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\commons\1945-06-14a.xml")

conn.commit()
cursor.close()
conn.close()
