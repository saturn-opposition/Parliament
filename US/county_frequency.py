#encoding = utf8
import os
import csv

files_list = []
d = []
r = ''
f = []
for root, dirs, files in os.walk(r"C:\Users\Pluto\Desktop\美国议会数据txt"):
   r = root
   d = dirs
   f = files
for i in range(len(f)):
    files_list.append(os.path.join(root,f[i]))
csv_file = []
for i in range(len(f)):
    csv_file.append(f[i][5:-4])
country = []
country_abb = ['US','UN','JP','CN']
country_abb_n = ['United States','United Kingdom','Japan','China']
capital = []
country_fullname = []
with open(r"C:\Users\Pluto\Desktop\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[1] for row in reader]
with open(r"C:\Users\Pluto\Desktop\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    capital = [row[5] for row in reader]
with open(r"C:\Users\Pluto\Desktop\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country_fullname = [row[4] for row in reader]
country.pop(0)
capital.pop(0)
country_fullname.pop(0)
for i in range(len(capital)):
    capital[i] = capital[i].strip()            #去掉空格
    country_fullname[i] = country_fullname[i].strip()


def find_country(filepath):
    country_dict = {}
    f = open(filepath, 'r', encoding='utf-8')
    doc = f.read()
    f.close()
    words = doc.split()

    for j in range(len(words)):
        for k in range(len(country)):
            if words[j]==country[k]:
                if words[j] in country_dict.keys():
                    count = country_dict[words[j]] + 1
                    country_dict[words[j]] = count
                else:
                    country_dict[words[j]] = 1
            if words[j]==capital[k]:
                if country[k] in country_dict.keys():
                    count = country_dict[country[k]] + 1
                    country_dict[country[k]] = count
                else:
                    country_dict[country[k]] = 1
        for t in range(len(country_abb)):
            if words[j]==country_abb[t]:
                if country_abb_n[t] in country_dict.keys():
                    count = country_dict[country_abb_n[t]] + 1
                    country_dict[country_abb_n[t]] = count
                else:
                    country_dict[country_abb_n[t]] = 1
    print('已完成'+files_list[i])
    return country_dict

csv_country = []
csv_frequency = []
for i in range(len(files_list)):
    c_dict = find_country(files_list[i])
    csv_country.append(','.join(c_dict.keys()))
    csv_frequency.append(c_dict)
header_a = ['file','country','frequency']
csvfile = open("C:\\Users\\Pluto\\Desktop\\美国国家词频.csv", "w", encoding='utf-8', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(header_a)
csvwriter.writerows(zip(csv_file,csv_country,csv_frequency))




