#encoding = utf8
import os
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

files_list = []
d = []
r = ''
f = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\file_txt"):
   r = root
   d = dirs
   f = files
for i in range(len(f)):
    files_list.append(os.path.join(root,f[i]))

country = []
country_abb = ['US','UN','JP','CN']
capital = []

with open(r"C:\Users\hjn\Desktop\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[1] for row in reader]
with open(r"C:\Users\hjn\Desktop\大创项目\数据\世界各国全称简称(中英文对照).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    capital = [row[5] for row in reader]
country.pop(0)
capital.pop(0)

for i in range(len(capital)):
    capital[i] = capital[i].strip()            #去掉空格

country_dict = {}
for i in range(len(files_list)):
    f = open(files_list[i], 'r', encoding='utf-8')
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
                if words[j] in country_dict.keys():
                    count = country_dict[words[j]] + 1
                    country_dict[words[j]] = count
                else:
                    country_dict[words[j]] = 1
        for t in range(len(country_abb)):
            if words[j]==country_abb[t]:
                if words[j] in country_dict.keys():
                    count = country_dict[words[j]] + 1
                    country_dict[words[j]] = count
                else:
                    country_dict[words[j]] = 1
    print('已完成'+files_list[i])

wordcloud = WordCloud(background_color='white')
wordcloud = wordcloud.fit_words(country_dict)
plt.imshow(wordcloud)
plt.show()
plt.savefig(r"C:\Users\hjn\Desktop\议会数据\议会数据\file_txt\美国国家词频云图_2019.png")


header_a = ['country','frequency']
with open(r"C:\Users\hjn\Desktop\议会数据\议会数据\file_txt\美国国家词频_2019.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_a)
    csvwriter.writerows(zip(country_dict.keys(),country_dict.values()))
csvfile.close()

