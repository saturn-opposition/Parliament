import os
import pymysql
import csv
import re

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='euromember', charset='utf8')
cursor = conn.cursor()

count_m = 0
count_speech = 0
count_a = 0

def to_mysql(path):
    global count_m,count_speech,count_a
    temp = os.listdir(path)
    member_id = 'm' + str(count_m)

    # 1 基本信息
    try:
        name = []
        party = []
        status = []
        country = []
        with open(path+'\\'+'1-基本信息.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name.append(row[0])
                party.append(row[1])
                status.append(row[2])
                country.append(row[3])
        row = cursor.execute(
            "insert into member(member_id,name,party,status,country)values(%s, %s,%s,%s, %s)",
            (member_id, name[1], party[1], status[1], country[1]))
        conn.commit()
        count_m = count_m + 1

        if "2-HOME.csv" in temp:
            chair = ''
            members = ''
            substitute = ''
            with open(r"D:\大创项目-新\欧盟议员信息库\EuPerson\101039\2-HOME.csv", 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = []
                n = 0
                items = []
                for row in reader:
                    if n == 0:
                        for j in range(len(row)):
                            header.append(row[j])
                        n = 9
                    else:
                        for j in range(len(row)):
                            items.append(row[j])
                for j in range(len(header)):
                    if "chair" in header[j]:
                        chair = items[j].replace('\'','').replace('[','').replace(']','')
                    if "member" in header[j]:
                        members = items[j].replace('\'','').replace('[','').replace(']','')
                    if "substitute" in header[j]:
                        substitute = items[j].replace('\'','').replace('[','').replace(']','')
            row = cursor.execute(
                "update member set chair = \'" + chair + "\' where member_id = \'" + member_id + "\'")
            row = cursor.execute(
                "update member set members = \'" + members + "\' where member_id = \'" + member_id + "\'")
            row = cursor.execute(
                "update member set substitute = \'" + substitute + "\' where member_id = \'" + member_id + "\'")
            conn.commit()

        if "3-DEBATES.csv" in temp:
            with open(path+'\\'+'3-DEBATES.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                t = []
                c = 1
                for row in reader:
                    if c == 1:
                        c = 2
                        pass
                    else:
                        t.extend(row)

            for j in range(len(t)):
                splits = t[j].split('\': ')
                meet_name = splits[1][0:-13]
                meet_date = splits[2][0:-10]
                speech = splits[3][0:-2]
                row = cursor.execute(
                    "insert into speech(speech_id,speaker_id,date,meeting_name,content)values(%s, %s,%s,%s, %s)",
                    ('s'+str(count_speech), member_id, meet_date, meet_name, speech))
                conn.commit()
                count_speech = count_speech + 1

        if '7-ASSISTANTS.csv' in temp:
            with open(r"D:\大创项目-新\欧盟议员信息库\EuPerson\197746\7-ASSISTANTS.csv", 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                n = 0
                header = []
                items = []
                for row in reader:
                    if n == 0:
                        for j in range(len(row)):
                            header.append(row[j])
                        n = 9
                    else:
                        for j in range(len(row)):
                            items.append(row[j])
            header[0] =header[0][8:]
            for j in range(len(header)):
                    name_lists = items[j].replace('\'', '').replace('[', '').replace(']', '').split(',')
                    for k in range(len(name_lists)):
                        row = cursor.execute(
                        "insert into assistants(id,name,type,speaker_id)values(%s, %s,%s,%s)",
                        ('a'+str(count_a), name_lists[k],header[j],member_id))
                        conn.commit()
                        count_a = count_a + 1
        print(name[1]+'已完成')
    except:
        print("check"+path)
        pass


li = os.listdir(r"D:\大创项目-新\欧盟议员信息库\EuPerson")
dirs = []
for i in range(len(li)):
    to_mysql("D:\\大创项目-新\\欧盟议员信息库\\EuPerson\\"+li[i])