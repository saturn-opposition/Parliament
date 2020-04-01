import os
import pymysql
import csv

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='canadamember', charset='utf8')
cursor = conn.cursor()
count = 0
count_s = 0
def get_files_path(dir):
    files_ = []
    list = os.listdir(dir)
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if os.path.isdir(path):
            files_.extend(get_files_path(path))
        if os.path.isfile(path):
            files_.append(path)
    return files_

def to_mysql(path1,path2):
        global count,count_s
        href = []
        name = []
        party = []
        address = []
        election = []
        keypoint = []
        terms = []
        with open(path1, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                href.append(row[0])
                name.append(row[1])
                terms.append(row[2])
                party.append(row[3])
                address.append(row[4])
                election.append(row[5])
                keypoint.append(row[6])
        row = cursor.execute(
            "insert into member_old(member_id,name,terms,party,address,election,keypoint,href,state)values(%s, %s,%s,%s, %s,%s,%s, %s,%s)",
            ('o'+str(count),name[1],terms[1],party[1],address[1],election[1],keypoint[1],href[1],"Y"))
        conn.commit()

        topic = []
        content = []
        date = []
        url = []
        with open(path2, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    topic.append(row[1])
                    content.append(row[3])
                    date.append(row[2])
                    url.append(row[0])
            except:
                print(name[1]+"无发言记录")
        for j in range(1,len(topic)):
            row = cursor.execute(
                "insert into speech_old(speech_id,speaker_id,date,url,topic,content)values(%s, %s,%s,%s, %s,%s)",
                ('os'+str(count_s),'o'+str(count),date[j],"https://openparliament.ca"+url[j],topic[j],content[j]))
            conn.commit()
            count_s = count_s + 1

        count = count + 1
        print("已完成"+name[1])

files = get_files_path(r"D:\大创项目-新\加拿大议员信息库\CAPOLD")
print(len(files))

for i in range(len(files)):
    # print(files[i])
    if "基本信息" in files[i]:
        to_mysql(files[i],files[i+1])