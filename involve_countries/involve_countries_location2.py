import pymysql
import re
import xml.dom.minidom
from xml.etree import ElementTree as ET
import csv
import os
import matplotlib.pyplot as plt
def find_minor_heading(num,topic):
    a = 0
    for i in range(len(topic)):
        a = a + topic[i]
        if num < a or num == a:
            return i
    if num == sum(j for j in topic) + 1:
        return len(topic)-1
    return -1


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
    city = [row[6] for row in reader]
country.pop(0)
country_abb.pop(0)
country_fullname.pop(0)
city.pop(0)

for i in range(len(country_fullname)):
    country_fullname[i] = country_fullname[i].strip()
while '' in city:
    city.remove('')

# conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='irlab', db='parliament', use_unicode=True,
#                        charset='utf8')
# cur = conn.cursor()
# cur.execute('select date,involving_country,type from meeting ')
# r = cur.fetchall()
# for rl in r:
#     date.append(rl[0])
#     country.append(rl[1])
#     type.append(rl[2])
#
# for i in range(len(country)):
#     if country[i] != None:
#         # country[i] = country[i].split(';')
#         country[i] = re.split(r'[,;.:；]',country[i])
#
# total_country = {}
# print(country)
# for i in range(len(country)):
#     if country[i] != None:
#         for s in range(len(country[i])):
#             if country[i][s] not in total_country.keys():
#                 total_country[country[i][s]] = i
#
# for key,value in total_country.items():
#     print('{key}:{value}'.format(key = key, value = value))             #数据库中包含国家的信息分得有点乱 还有单词拼写错误
country_dict = {}

def one_xml(file_loc):
    global country_dict
    year = file_loc[-15:-4]
    # dom = xml.dom.minidom.parse(file_loc)
    # root = dom.documentElement
    dom = ET.parse(file_loc)
    root = dom.findall('./')



    topic_speech_num = []
    temp = 0
    flag = True
    minor_heading = []
    for i in root.iter():
        if i.text == 'minor-heading':
            t = i.text
            t = t.strip('\n')
            t = t.strip('\t')





    # for i in range(2):
    #     if root.find().text == 'minor-heading':
    #         t = root.childNodes[i].firstChild.data
    #         t = t.strip('\n')
    #         t = t.strip('\t')
    #         minor_heading.append(t)
    # for i in range(2,len(root.childNodes)):
    #     if root.childNodes[i].nodeName == 'gidredirect':
    #         break
    #
    #
    #     if root.childNodes[i].nodeName == 'minor-heading':
    #         t = root.childNodes[i].firstChild.data
    #         t = t.strip('\n')
    #         t = t.strip('\t')
    #         minor_heading.append(t)
    #         flag = False
    #     if flag == True & (root.childNodes[i].nodeName =='speech'):
    #         temp = temp +1
    #     if flag == False:
    #         topic_speech_num.append(temp-1)
    #         temp = 0
    #         flag = True
    # topic_speech_num.append(temp-1)
    #
    #
    #
    # sentences = []
    # speech_id = []
    # speech_location = []
    # speaker_id = []
    #
    # speech = dom.getElementsByTagName('speech')
    # count = 0
    #

    for i in range(len(speech)):
        speech_id.append(speech[i].getAttribute('id')[-17:])
        speaker_id.append(speech[i].getAttribute('speakerid'))
        pnode = speech[i].getElementsByTagName('p')
        temp = ''
        count = count + 1

        for node in pnode:
            temp = node.find().text

            # if type(node) == xml.dom.minidom.NodeList:
            #     for s in node:
            #             temp = temp + s.firstChild.data
            #
            # else:
            #     temp = temp + node.firstChild.data






        sentences.append(temp)
        if topic_speech_num != []:

            k = find_minor_heading(count,topic_speech_num)
            if k!= -1:

                speech_location.append(minor_heading[k])




    for i in range(len(sentences)):
        temp_sen = sentences[i].lower()
        for j in range(len(country)):
            if country[j].lower() in temp_sen:

                if country[j] in country_dict.keys():
                    temp_tuple = (year,speech_id[i],speech_location[i] ,speaker_id[i])
                    country_dict[country[j]].append(temp_tuple)
                else:
                    country_dict[country[j]] = [(year,speech_id[i],speech_location[i] ,speaker_id[i])]

            elif country_fullname[j].lower() in temp_sen:
                if country[j] in country_dict.keys():
                    temp_tuple = (year, speech_id[i], speech_location[i], speaker_id[i])
                    country_dict[country[j]].append(temp_tuple)
                else:
                    country_dict[country[j]] = [(year, speech_id[i], speech_location[i], speaker_id[i])]

        for k in range(len(city)):
            if city[k].lower() in temp_sen:
                if city[k] in country_dict.keys():
                    temp_tuple = (year, speech_id[i], speech_location[i], speaker_id[i])
                    country_dict[city[k]].append(temp_tuple)
                else:
                    country_dict[city[k]] = [(year,speech_id[i],speech_location[i],speaker_id[i])]
        for t in range(len(country_abb)):
            if country_abb[t] in sentences:
                if country[t] in country_dict.keys():
                    temp_tuple = (year, speech_id[i], speech_location[i], speaker_id[i])
                    country_dict[country[j]].append(temp_tuple)
                else:
                    country_dict[country[j]] = [(year, speech_id[i], speech_location[i], speaker_id[i])]





xml_files = []
for root, dirs, files in os.walk("C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords"):

    xml_files.append(files)


for s in range(len(xml_files[0])):
    xml_files[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords\\' + xml_files[0][s]
xml_files = xml_files[0]

for i in range(5):
    one_xml(xml_files[i])
    print("成功完成文件"+xml_files[i])

# print(len(country_dict.keys()))
# print(len(country_dict.keys()))
    # print(len(country)+len(city))
    #
    # for d,x in country_dict.items():
    #     print("key:"+d)
    #     print(x)
    #     print("**************************************************************************************************************")
country_name = []

templist = []
year = []
speech_id_per_country = []
location = []
speaker_id_per_country = []
c = []
t = []
for key ,value in country_dict.items():
    print(key)
    print(value)
    print("**************************************")
for key,value in country_dict.items():
    templist = value
    c.append(key)
    t.append(len(templist))

    for i in range(len(templist)):
        country_name.append(key)
        year.append(templist[i][0])
        speech_id_per_country.append(templist[i][1])
        location.append(templist[i][2])
        speaker_id_per_country.append((templist[i][3]))

header = ['country','date','speech_id','topic','speaker_id']

with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\涉及的国家及相关信息.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(country_name,year,speech_id_per_country,location,speaker_id_per_country))
csvfile.close()

print("输出.csv文件完毕")

labels = c
size = t
patches, text1, text2 = plt.pie(size, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, pctdistance=0.6)
plt.axis('equal')
plt.legend()
print("开始存图")
plt.savefig("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\国家被提及比例.png")
plt.show()


# one_xml("C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords\\2002-03-11a.xml")







