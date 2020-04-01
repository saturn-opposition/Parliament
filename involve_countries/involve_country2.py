import csv
import os
from  xml.etree import ElementTree as ET

p_content = []
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
    capital = [row[5] for row in reader]
country.pop(0)
country_abb.pop(0)
country_fullname.pop(0)
capital.pop(0)

for i in range(len(country_fullname)):
    country_fullname[i] = country_fullname[i].strip()            #去掉空格

for i in range(len(capital)):
    capital[i] = country_fullname[i].strip()            #去掉空格


p_country = []
article_id = []
article_country = []
article_only_country = []
year = []
month = []
p_only_country = []
p_year = []
p_month = []
minor_heading = []
major_heading = []
def one_xml(file_loc):

    global p_country

    global p_content
    global p_only_country
    global month
    global year
    global p_year
    global p_month
    global minor_heading
    global major_heading
    year.append(file_loc[-15:-11])
    month.append(file_loc[-10:-8])
    thisfile_country = {}
    root = ET.parse(file_loc)
    minor_h = 'null'
    major_h = 'null'


    for node in root.iter():
        if (node.tag == 'minor-heading'):
            minor_h = node.text
        if (node.tag == 'major-heading'):
            major_h = node.text
        if (node.tag == 'p') & (node.text!=None):

            # p_id.append(node.find('pid'))
            sentences = node.text
            s = str.lower(sentences)
            thisp_country = {}

            wordslist = sentences.split()
            for w in range(len(wordslist)):
                for t in range(len(country_abb)):
                    if country_abb[t]==wordslist[w]:
                    #     if country[t] in thisfile_country.keys():
                    #         count = thisfile_country[country[t]] + 1
                    #         thisfile_country[country[t]] = count
                    #     else:
                    #         thisfile_country[country[t]] = 1
                        if country[t] in thisp_country.keys():
                            count = thisp_country[country[t]] + 1
                            thisp_country[country[t]] = count
                        else:
                            thisp_country[country[t]] = 1
            for k in range(len(capital)):
                if capital[k].lower() in s:
                    # if country[k] in thisfile_country.keys():
                    #     count = thisfile_country[country[k]] + 1
                    #     thisfile_country[country[k]] = count
                    # else:
                    #    thisfile_country[country[k]] = 1
                    if country[k] in thisp_country.keys():
                        count = thisp_country[country[k]] + 1
                        thisp_country[country[k]] = count
                    else:
                        thisp_country[country[k]] = 1
            for j in range(len(country)):
                if country[j].lower() in s:
                #     if country[j] in thisfile_country.keys():
                #         count = thisfile_country[country[j]] + 1
                #         thisfile_country[country[j]] = count
                #     else:
                #         thisfile_country[country[j]] = 1
                    if country[j] in thisp_country.keys():
                        count = thisp_country[country[j]] + 1
                        thisp_country[country[j]] = count
                    else:
                        thisp_country[country[j]] = 1
                elif country_fullname[j].lower() in s:
                    # if country[j] in thisfile_country.keys():
                    #     count = thisfile_country[country[j]] + 1
                    #     thisfile_country[country[j]] = count
                    # else:
                    #     thisfile_country[country[j]] = 1
                    if country[j] in thisp_country.keys():
                        count = thisp_country[country[j]] + 1
                        thisp_country[country[j]] = count
                    else:
                        thisp_country[country[j]] = 1
            temp = []
            p_c = []

            for key,value in thisp_country.items():
                if key!='':
                    t = (key,value)
                    p_c.append(key)

                    temp.append(t)
            if temp!=[]:
                        p_country.append(temp)

                        key_str = ';'.join(p_c)

                        p_only_country.append(key_str)
                        minor_heading.append(minor_h)
                        major_heading.append(major_h)
                        p_year.append(file_loc[-15:-11])
                        p_month.append(file_loc[-10:-8])
                        p_content.append(node.text)


    return thisfile_country


xml_files = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\commons_2009-2018"):
   xml_files.append(files)


for s in range(len(xml_files[0])):

    xml_files[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\commons_2009-2018\\' + xml_files[0][s]

xml_files = xml_files[0]

for i in range(len(xml_files)):
    temp_dict = one_xml(xml_files[i])
    # temp = []
    # a_c = []
    # for key, value in temp_dict.items():
    #     if key !='':
    #         t = (key, value)
    #         temp.append(t)
    #         a_c.append(key)
    # article_id.append(xml_files[i][-15:-4])
    # key_str = ';'.join(a_c)
    # article_only_country.append(key_str)


    # article_country.append(temp)


    print("成功完成文件"+xml_files[i])

print(len(minor_heading))
print(len(major_heading))
print(len(p_content))
header_p = ['year','month','minor_heading','major_heading','p_content','p_country','frequency']

with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\commons_no.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_p)
    csvwriter.writerows(zip(p_year,p_month,minor_heading,major_heading,p_content,p_country,p_only_country))
csvfile.close()

# header_p = ['year','month','p_content','country']
#
# with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\段落涉及国家2.0（commons).csv", "w", encoding='utf-8', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header_p)
#     csvwriter.writerows(zip(p_year,p_month,p_content,p_country))
# csvfile.close()


# header_a = ['year','month','article_id','country']
# with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\全文涉及国家2.0（lords）.csv", "w", encoding='utf-8', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header_a)
#     csvwriter.writerows(zip(year,month,article_id,article_country))
# csvfile.close()

# with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\段落涉及国家2.1（commons).csv", "w", encoding='utf-8', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header_p)
#     csvwriter.writerows(zip(p_year,p_month,p_content,p_only_country))
# csvfile.close()

# with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\全文涉及国家2.1（lords).csv", "w", encoding='utf-8', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(header_a)
#     csvwriter.writerows(zip(year,month,article_id,article_only_country))
# csvfile.close()
