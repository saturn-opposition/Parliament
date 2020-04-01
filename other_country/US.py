import csv
import os
import re
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

txt_files = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\txt\txt"):
   txt_files.append(files)

for s in range(len(txt_files[0])):

    txt_files[0][s] =  "C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\txt\\txt\\" + txt_files[0][s]
txt_files = txt_files[0]

def one_txt(file_loc):
    passage = ''
    with open(file_loc,'r',encoding='utf-8')as f:
        passage = f.read()
    country_dict = {}
    lower_passage = passage.lower()

    for k in range(len(capital)):
        if capital[k].lower() in lower_passage:
                if country[k] in country_dict.keys():
                    count = country_dict[country[k]] + 1
                    country_dict[country[k]] = count
                else:
                    country_dict[country[k]] = 1

        if country[k].lower() in lower_passage:
                if country[k] in country_dict.keys():
                    count = country_dict[country[k]] + 1
                    country_dict[country[k]] = count
                else:
                    country_dict[country[k]] = 1
        if country_fullname[k].lower() in lower_passage:
                if country[k] in country_dict.keys():
                    count = country_dict[country[k]] + 1
                    country_dict[country[k]] = count
                else:
                    country_dict[country[k]] = 1
    return country_dict

process = []
for i in range(len(txt_files)):
    if int(txt_files[i][44:48]) in range(2009,2018):
        process.append(txt_files[i])
year = []
month = []
file_country = []
file_country_num = []
for i in range(len(process)):
    temp_dict = one_txt(process[i])
    temp = []
    a_c = []
    for key, value in temp_dict.items():
        if key !='':
            t = (key, value)
            temp.append(t)
            a_c.append(key)
    month.append(process[i][49:51])
    year.append(process[i][44:48])
    key_str = ';'.join(a_c)
    file_country.append(key_str)
    file_country_num.append(temp)

    print("成功完成文件"+process[i])


header_p = ['year','month','country','country_num']

with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\US(2009-2017).csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_p)
    csvwriter.writerows(zip(year,month,file_country,file_country_num))
csvfile.close()




