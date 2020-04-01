import csv
from  xml.etree import ElementTree as ET
import os
country = []
capital = []
country_fullname = []
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
    country_fullname[i] = country_fullname[i].strip()            #去掉空格

for i in range(len(capital)):
    capital[i] = country_fullname[i].strip()            #去掉空格


def one_xml(path):
    global country
    global country_fullname
    global capital
    try:
        root = ET.parse(path).getroot()
    except:
        print(path)
        pass
    this_xml = []
    this_xml_count = []
    this_xml_date = []
    for p in root.iter('p'):
        if p.text != None:
            para_content = p.text.lower()
        else:
            para_content = ''
        # print(para_content)
        thisp_country = []
        for k in range(len(capital)):
            if capital[k].lower() in para_content:
                    thisp_country.append(country[k])
        for j in range(len(country)):
            if country[j].lower() in para_content:
                    thisp_country.append(country[j])
            elif country_fullname[j].lower() in para_content:
                    thisp_country.append(country[j])

        thisp_country = set(thisp_country)
        para_involve_country_count = len(thisp_country)
        para_involve_country = ';'.join(thisp_country)
        if para_involve_country != '':
            this_xml.append(para_involve_country)
            this_xml_count.append(para_involve_country_count)
            this_xml_date.append(path[-15:-5])
    return this_xml_date,this_xml,this_xml_count

xml_files = []
for root, dirs, files in os.walk(r"C:\Users\Pluto\Desktop\UK\lordspages"):
   xml_files.append(files)


for s in range(len(xml_files[0])):

    xml_files[0][s] =  "C:\\Users\\Pluto\\Desktop\\UK\\lordspages\\" + xml_files[0][s]

xml_files = xml_files[0]

row1 = []
row2 = []
row3 = []
for i in range(len(xml_files)):
    t1,t2,t3 = one_xml(xml_files[i])
    print("已完成"+xml_files[i])
    row1.extend(t1)
    row2.extend(t2)
    row3.extend(t3)

header_a = ['date','country','frequency']
csvfile = open("C:\\Users\\Pluto\\Desktop\\2019.csv", "w", encoding='utf-8', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(header_a)
csvwriter.writerows(zip(row1,row2,row3))
csvfile.close()

