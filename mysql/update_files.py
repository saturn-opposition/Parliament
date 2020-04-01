import  pymysql
import os
from collections import Counter
from  xml.etree import ElementTree as ET
import csv

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='test', charset='utf8')
cursor = conn.cursor()
country = []
capital = []
country_fullname = []
f = 0
m = 0
meeting_mf = 0
num_sf = 0
pid = 0
saved_major = []
saved_minor = []
saved_speaker = []
saved_meeting_id = []

def get_existed_id():
    global conn,f,m,mf,saved_major,saved_minor,saved_speaker,pid,saved_meeting_id,meeting_mf,num_sf
    cursor.execute("select file_id from file")
    row = cursor.fetchall()
    file_id = []
    for i in range(len(row)):
        file_id.append(int(row[i][0].strip('f')))
    f = max(file_id) + 1
    cursor.execute("select meeting_id from meeting")
    row = cursor.fetchall()
    meeting_id = []
    for i in range(len(row)):
        meeting_id.append(int(row[i][0].strip('m')))
    m = max(meeting_id) + 1

    cursor.execute("select number_mf from meeting_file")
    row = cursor.fetchall()
    temp = []
    for i in range(len(row)):
        temp.append(int(row[i][0]))
    meeting_mf = max(temp) + 1

    cursor.execute("select num_sp from speech_para")
    row = cursor.fetchall()
    temp = []
    for i in range(len(row)):
        temp.append(int(row[i][0]))
    num_sf = max(temp) + 1

    cursor.execute("select para_id from paragraph")
    row = cursor.fetchall()
    para_id = []
    for i in range(len(row)):
        para_id.append(int(row[i][0].strip('p')))
    pid = max(para_id) + 1

    cursor.execute("select major_heading_id from major_heading")
    row = cursor.fetchall()
    for i in range(len(row)):
        saved_major.append(row[i][0])
    cursor.execute("select minor_heading_id from minor_heading")
    row = cursor.fetchall()
    for i in range(len(row)):
        saved_minor.append(row[i][0])

    cursor.execute("select speaker_id from speaker")
    row = cursor.fetchall()
    saved_speaker = []
    for i in range(len(row)):
        saved_speaker.append(row[i][0])

    cursor.execute("select meeting_id from meeting")
    row = cursor.fetchall()
    saved_meeting_id = []
    for i in range(len(row)):
        saved_meeting_id.append(row[i][0])


def get_files(path):
    file_names = []
    file_paths = []
    for root, dirs, files in os.walk(path):
        file_names.append(files)

    for s in range(len(file_names[0])):
        file_paths.append("C:\\Users\\Pluto\\Desktop\\UK\\lordspages\\" + file_names[0][s])
    return file_names[0],file_paths

def insert_file(file_names,type):
    global conn,cursor,f
    update_file_id = []
    update_file_type = []
    for i in range(len(file_names)):
        file_id = 'f' + str(f)
        file_name = file_names[i]
        row = cursor.execute(
            "insert into file(file_id ,file_name,type)values(%s, %s,%s)",
            (file_id, file_name, type))
        conn.commit()
        f = f + 1
        update_file_id.append(file_id)
        update_file_type.append(type)

    print("file表更新完毕")
    return update_file_id,update_file_type,file_names

def meeting_file(update_file_id,update_file_type,file_names):
    global f,saved_meeting_id,meeting_mf
    date_connect_type = []
    update_meeting_id = []
    for i in range(len(update_file_type)):
        if update_file_type[i] == 'lords':
            date_connect_type.append('lords' + file_names[i][7:17])
        elif type[i] == 'commons':
            date_connect_type.append('commons' + file_names[i][7:17])

    result = Counter(date_connect_type)

    for date, count in result.items():
        s_id = 'm' + str(f)
        if date[0] == 'l':
            d = date[5:]

            row = cursor.execute(
                "insert into meeting(date ,country,type,file_count,meeting_id)values(%s, %s,%s,%s,%s)",
                (d, 'UK', 'lords', count, s_id))  # 尚未插入包含国家
            conn.commit()
            saved_meeting_id.append(s_id)
            update_meeting_id.append(s_id)
            f = f + 1
        elif date[0] == 'c':
            d = date[7:]

            row = cursor.execute(
                "insert into meeting(date ,country,type,file_count,meeting_id)values(%s, %s,%s,%s,%s)",
                (d, 'UK', 'commons', count, s_id))  # 尚未插入包含国家
            conn.commit()
            saved_meeting_id.append(s_id)
            update_meeting_id.append(s_id)
            f = f + 1

    for i in range(len(file_names)):
        cursor.execute(
            "select meeting_id from meeting where date = \'" + file_names[i][7:17] + "\' and type =\'lords\'")
        row = cursor.fetchall()
        conn.commit()
        meeting_id = row[0]
        row = cursor.execute(
            "insert into meeting_file(meeting_id ,file_id,number_mf)values(%s, %s,%s)",
            (meeting_id, update_file_id[i], meeting_mf))
        conn.commit()
        meeting_mf = meeting_mf + 1
    print("meeting表、meeting_file表更新完毕")
    return update_meeting_id

def speech_minor_major(file_paths):
    global saved_major,saved_minor,saved_speaker
    for i in range(len(file_paths)):
        root = ET.parse(file_paths[i])
        major_heading_id = ''
        minor_heading_id = ''
        major_heading_name = ''
        major_url = ''
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
                if major_heading_id not in saved_major:
                    row = cursor.execute(
                    "insert into major_heading(major_heading_id ,major_heading_name,url,colnum)values(%s, %s,%s,%s)",
                    (major_heading_id,major_heading_name,major_url,major_column))
                    saved_major.append(major_heading_id)
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
                if minor_heading_id not in saved_minor:
                    row = cursor.execute(
                    "insert into minor_heading(minor_heading_id ,minor_heading_name,url,colnum)values(%s, %s,%s,%s)",
                    (minor_heading_id, minor_heading_name, minor_url, minor_column))
                    saved_minor.append(minor_heading_id)
                    conn.commit()
            if node.tag == 'speech':
                s_id = node.get('id')
                spea_id = node.get('speakerid')

                if (major_heading_id == ''):
                    major_heading_id = 'no_major_heading'
                if minor_heading_id == '':
                    minor_heading_id = 'no_minor_heading'
                if spea_id == None:
                    spea_id = 'no_speaker'
                if spea_id not in saved_speaker:
                    spea_id = 'no_speaker'
                try:
                    row = cursor.execute(
                            "insert into speech(speech_id ,speaker_id,major_heading_id,minor_heading_id)values(%s, %s,%s,%s)",
                            (s_id, spea_id, major_heading_id, minor_heading_id))
                    conn.commit()
                except:
                    pass


    print("speech表等更新完毕")


def load_data():
    global country,capital,country_fullname
    with open(r"D:\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        country = [row[1] for row in reader]
    with open(r"D:\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        country_fullname = [row[4] for row in reader]
    with open(r"D:\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        capital = [row[5] for row in reader]
    country.pop(0)
    country_fullname.pop(0)
    capital.pop(0)

    for i in range(len(country_fullname)):
        country_fullname[i] = country_fullname[i].strip()  # 去掉空格

    for i in range(len(capital)):
        capital[i] = country_fullname[i].strip()  # 去掉空格


def speech_para(file_paths):
    global country,capital,country_fullname,pid,num_sf
    for i in range(len(file_paths)):

        root = ET.parse(file_paths[i])

        for node in root.findall('speech'):
            s_id = node.get('id')
            if s_id == None:
                s_id = 'no_speech_id'
            for p in node.findall('p'):
                if p != None:
                    p_id = p.get('pid')

                    if p_id != None and p.text != None:
                        para_content = p.text
                        para_id = 'p' + str(pid)

                        s = str.lower(para_content)
                        thisp_country = []

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
                        para_involve_country = ';'.join(thisp_country) + ';'

                        row = cursor.execute(
                            "insert into paragraph(para_id ,para_content,para_involve_country,para_involve_country_count,pid)values(%s, %s,%s,%s,%s)",
                            (para_id, para_content, para_involve_country, para_involve_country_count, p_id))
                        conn.commit()
                        pid = pid + 1
                        try:
                            row = cursor.execute(
                                "insert into speech_para(speech_id ,para_id,num_sp)values(%s, %s,%s)",
                                (s_id, para_id, num_sf))
                            conn.commit()
                        except:
                            pass

    print("paragraph表等更新完毕")



def speaker(file_paths):
    global saved_speaker
    for i in range(len(file_paths)):
        root = ET.parse(file_paths[i])

        for node in root.findall('speech'):
            speaker_id = node.get('speakerid')
            try:
                if (speaker_id != None) & (speaker_id not in saved_speaker):
                    speaker_name = node.get('speakername')
                    url = 'https://www.publicwhip.org.uk/mp.php?id=' + speaker_id
                    hansard_membership_id = node.get('hansard_membership_id')

                    row = cursor.execute(
                        "insert into speaker(speaker_id ,speaker_name,url,hansard_membership_id)values(%s, %s,%s,%s)",
                        (speaker_id, speaker_name, url, hansard_membership_id))
                    conn.commit()
                    saved_speaker.append(speaker_id)
            except:
                print("error")
                pass
    print('speaker表更新完毕')

def meeting_speech(file_paths,file_names,type):
    for i in range(len(file_paths)):
        root = ET.parse(file_paths[i])
        cursor.execute(
            "select meeting_id from meeting where date = \'" + file_names[i][7:17] + '\' and type =\'' + type[i] + '\'')
        row = cursor.fetchall()

        meeting_id = row[0]
        for node in root.findall('speech'):
            speech_id = node.get('id')

            row = cursor.execute(
                    "insert into meeting_speech(meeting_id ,speech_id,number_ms)values(%s, %s,%s)",
                    (meeting_id, speech_id, 1))
            conn.commit()
    print('meeting_speech表更新完毕')

def complete_meeting():
    global conn
    cursor.execute("select speech_id,meeting_id from meeting_speech")
    row = cursor.fetchall()
    meeting_speech_dict = {}
    for i in range(len(row)):
        if row[i][1] in meeting_speech_dict.keys():
            speech_id_str = meeting_speech_dict[row[i][1]] + ';' + row[i][0]
            meeting_speech_dict[row[i][1]] = speech_id_str
        else:
            meeting_speech_dict[row[i][1]] = row[i][0]
    temp_m_id = ''
    temp_s_id = ''
    one_meeting_country = ''
    one_speech_country = ''
    meeting_country_dict = {}

    for meeting_id, speech_id in meeting_speech_dict.items():
        speech_id_list = speech_id.split(';')
        para_id_list = []
        country_list = []
        for i in range(len(speech_id_list)):
            cursor.execute("select para_id from speech_para where speech_id = \'" + speech_id_list[i] + '\'')
            row = cursor.fetchall()
            if len(row) != 0:

                for t in range(len(row)):
                    para_id_list.append(row[t][0])
                for j in range(len(para_id_list)):
                    cursor.execute(
                        "select para_involve_country from paragraph where para_id = \'" + para_id_list[j] + '\'')
                    row = cursor.fetchall()
                    for z in range(len(row)):
                        country_list.append(row[z][0])
        country_list = set(country_list)
        country_str = ''.join(country_list)
        print(country_str)
        row = cursor.execute(
            "update meeting set involve_country = \'" + country_str + "\' where meeting_id = \'" + meeting_id + "\'")
        conn.commit()

    print('最后一步')
get_existed_id()
file_names,file_paths = get_files(r"C:\Users\Pluto\Desktop\UK\lordspages")
update_file_id,update_file_type,file_names = insert_file(file_names,'lords')
update_meeting_id = meeting_file(update_file_id,update_file_type,file_names)
speaker(file_paths)
speech_minor_major(file_paths)
load_data()
speech_para(file_paths)
meeting_speech(file_paths,file_names,update_file_type)
complete_meeting()

conn.commit()



