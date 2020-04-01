import pymysql
import re
import xml.dom.minidom
from xml.etree import ElementTree as ET
import csv
import os
nodetext = []
def findNodes(rootnodes):
    global nodetext


    if type(rootnodes.firstChild)==xml.dom.minidom.Text:
        nodetext.append(rootnodes.firstChild.data)
        return
    for c in rootnodes.childNodes:
        findNodes(c)
    return


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

country.pop(0)
country_abb.pop(0)
country_fullname.pop(0)


for i in range(len(country_fullname)):
    country_fullname[i] = country_fullname[i].strip()            #去掉空格

p_id = []
p_country = []
article_id = []
article_country = []
def one_xml(file_loc):
    global p_id
    global p_country
    global nodetext
    DOMTree = xml.dom.minidom.parse(file_loc)
    collection = DOMTree.documentElement
    p = collection.getElementsByTagName('p')
    thisfile_country = {}

    count = 0
    for node in p:

       thisp_country = {}
       findNodes(node)
       sentences = ''.join(nodetext)
       s = str.lower(sentences)
       nodetext = []


       for t in range(len(country_abb)):
           if country_abb[t] in sentences:
               if country[t] in thisfile_country.keys():
                   count = thisfile_country[country[t]] + 1
                   thisfile_country[country[t]] = count
               else:
                   thisfile_country[country[t]] = 1
               if country[t] in thisp_country.keys():
                   count = thisp_country[country[t]] + 1
                   thisp_country[country[t]] = count
               else:
                   thisp_country[country[t]] = 1
       for j in range(len(country)):
                if country[j].lower() in s:
                    if country[j] in thisfile_country.keys():
                        count = thisfile_country[country[j]] + 1
                        thisfile_country[country[j]] = count
                    else:
                        thisfile_country[country[j]] = 1
                    if country[j] in thisp_country.keys():
                        count = thisp_country[country[j]] + 1
                        thisp_country[country[j]] = count
                    else:
                        thisp_country[country[j]] = 1
                elif country_fullname[j].lower() in s:
                    if country[j] in thisfile_country.keys():
                        count = thisfile_country[country[j]] + 1
                        thisfile_country[country[j]] = count
                    else:
                        thisfile_country[country[j]] = 1
                    if country[j] in thisp_country.keys():
                        count = thisp_country[country[j]] + 1
                        thisp_country[country[j]] = count
                    else:
                        thisp_country[country[j]] = 1
       temp = []
       for key,value in thisp_country.items():
           if key!='':
            t = (key,value)
            temp.append(t)
       if temp!=[]:
        p_country.append(temp)
        p_id.append(node.getAttribute('pid'))


    return thisfile_country


xml_files = []
for root, dirs, files in os.walk("C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords"):
   xml_files.append(files)


for s in range(len(xml_files[0])):
    xml_files[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords\\' + xml_files[0][s]
xml_files = xml_files[0]

for i in range(len(xml_files)):
    temp_dict = one_xml(xml_files[i])
    temp = []
    for key, value in temp_dict.items():
        if key !='':
            t = (key, value)
            temp.append(t)
    article_id.append(xml_files[i][-15:-4])
    article_country.append(temp)


    print("成功完成文件"+xml_files[i])



header_p = ['p','country']

with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\段落涉及国家.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_p)
    csvwriter.writerows(zip(p_id,p_country))
csvfile.close()
header_a = ['article','country']
# with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\全文涉及国家.csv", "w", encoding='utf-8', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header_a)
#     csvwriter.writerows(zip(article_id,article_country))
# csvfile.close()
