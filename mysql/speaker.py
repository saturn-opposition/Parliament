import pymysql
from  xml.etree import ElementTree as ET
import  os
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接
file_name = []
type = []
cursor.execute("select speaker_id from speaker")
row = cursor.fetchall()
saved_speaker = []
for i in range(len(row)):
    saved_speaker.append(row[i][0])


#
# for i in range(len(row)):
#    file_name.append(row[i][0])
#    type.append(row[i][1])
#
#
# xml_files = []
# for s in range(len(file_name)):
#     xml_files.append('C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\' +type[s]+'\\'+file_name[s])

# saved_speaker = []
def one_xml(file_loc):
    global saved_speaker
    root = ET.parse(file_loc)

    for node in root.findall('speech'):
       speaker_id = node.get('speakerid')
       if (speaker_id != None) & (speaker_id not in saved_speaker):
        speaker_name = node.get('speakername')
        url = 'https://www.publicwhip.org.uk/mp.php?id='+speaker_id
        hansard_membership_id = node.get('hansard_membership_id')


        row = cursor.execute(
           "insert into speaker(speaker_id ,speaker_name,url,hansard_membership_id)values(%s, %s,%s,%s)",
           (speaker_id,speaker_name,url,hansard_membership_id))
        conn.commit()
        saved_speaker.append(speaker_id)

xml_files = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\commons"):
   xml_files.append(files)


for s in range(len(xml_files[0])):

    xml_files[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\commons\\' + xml_files[0][s]

xml_files = xml_files[0]


for i in range(len(xml_files)):
    one_xml(xml_files[i])
    print('已完成'+xml_files[i])


conn.commit()
cursor.close()
conn.close()
