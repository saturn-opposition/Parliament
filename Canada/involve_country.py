import pymysql
import csv
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='canada', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接

cursor.execute("select speechdate, speech_text,ID from file")
row = cursor.fetchall()
speech_text = []
date = []
id = []
for i in range(len(row)):
    speech_text.append(row[i][1])
    date.append(row[i][0])
    id.append(row[i][2])

country = []
# country_abb = ['US','UN','JP','CN']
# country_abb_n = ['United States','United Kingdom','Japan','China']
capital = []
country_fullname = []
with open(r"D:\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[1] for row in reader]
with open(r"D:\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    capital = [row[5] for row in reader]
with open(r"D:\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country_fullname = [row[4] for row in reader]
country.pop(0)
capital.pop(0)
country_fullname.pop(0)
for i in range(len(capital)):
    capital[i] = capital[i].strip()            #去掉空格
    country_fullname[i] = country_fullname[i].strip()

import nltk
def find_country(doc):
    country_dict = {}
    sentences = nltk.sent_tokenize(doc)

    for j in range(len(sentences)):
        for k in range(len(country)):
            if country[k] in sentences[j]:
                if country[k] in country_dict.keys():
                    count = country_dict[country[k]] + 1
                    country_dict[country[k]] = count
                else:
                    country_dict[country[k]] = 1
            if capital[k] in sentences[j]:
                if country[k] in country_dict.keys():
                    count = country_dict[country[k]] + 1
                    country_dict[country[k]] = count
                else:
                    country_dict[country[k]] = 1
            if country_fullname[k] in sentences[j]:
                if country_fullname[k] in country_dict.keys():
                    count = country_dict[country[k]] + 1
                    country_dict[country[k]] = count
                else:
                    country_dict[country[k]] = 1
        # for t in range(len(country_abb)):
        #     if words[j]==country_abb[t]:
        #         if country_abb_n[t] in country_dict.keys():
        #             count = country_dict[country_abb_n[t]] + 1
        #             country_dict[country_abb_n[t]] = count
        #         else:
        #             country_dict[country_abb_n[t]] = 1

    return country_dict

csv_country = []
csv_frequency = []
for i in range(953046,len(id)):

    c_dict = find_country(speech_text[i])
    csv_country.append(','.join(c_dict.keys()))
    country_str = ','.join(c_dict.keys())

    sql =  "update file set involve_country = \'" + country_str + "\' where ID = \'" + str(id[i]) + "\'"
    print(sql)
    row = cursor.execute(sql
       )
    conn.commit()
    csv_frequency.append(c_dict)

header_a = ['date','country','frequency']
csvfile = open("C:\\Users\\Pluto\\Desktop\\加拿大国家词频.csv", "w", encoding='utf-8', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(header_a)
csvwriter.writerows(zip(date,csv_country,csv_frequency))




