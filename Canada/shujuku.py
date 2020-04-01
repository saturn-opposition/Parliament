import os
import csv
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='canada', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接

def insertData(filepath):
    global conn
    global cursor
    hid_list = []
    speech_date_list = []
    pid_list = []
    opid_list = []
    speakeroldname_list = []
    speakerposition_list = []
    maintopic_list = []
    subtopic_list = []
    subsubtopic_list = []
    speechtext_list = []
    speakerparty_list = []
    speakerriding_list = []
    speakername_list = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            hid_list.append(row[1])
            speech_date_list.append(row[2])
            pid_list.append(row[3])
            opid_list.append(row[4])
            speakeroldname_list.append(row[5])
            speakerposition_list.append(row[6])
            maintopic_list.append(row[7])
            subtopic_list.append(row[8])
            subsubtopic_list.append(row[9])
            speechtext_list.append(row[10])
            speakerparty_list.append(row[11])
            speakerriding_list.append(row[12])
            speakername_list.append(row[13])
        print(hid_list)
        print(speech_date_list)
        for i in range(len(hid_list)-1):

            row = cursor.execute(
                "insert into file(hid ,speechdate,pid,opid,speaker_old_name,speaker_position,main_topic,sub_topic,sub_sub_topic,speech_text,speaker_party,speakerriding,speaker_name)values(%s, %s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s,%s)",
                (hid_list[i+1],speech_date_list[i+1],pid_list[i+1],opid_list[i+1],speakeroldname_list[i+1],speakerposition_list[i+1],maintopic_list[i+1],subtopic_list[i+1],subsubtopic_list[i+1],speechtext_list[i+1],speakerparty_list[i+1],speakerriding_list[i+1],speakername_list[i+1]))
            conn.commit()







files_list = []
d = []
r = ''
f = []
filespath = []
for root, dirs, files in os.walk(r"C:\Users\Pluto\Desktop\加拿大补充数据"):
   r = root
   d = dirs
   f = files
   if d ==[]:
       for i in range(len(f)):
           file = os.path.join(root,f[i])
           if file not in filespath:
                filespath.append(os.path.join(root,f[i]))
                insertData(file)
                print(file)






