import os
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import nltk
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import collections
import re

stop = set(stopwords.words('english'))

with open(r"C:\Users\hjn\Desktop\大创项目准备\LDA\stopwords\ENstopwords-US.txt", 'r', encoding='utf-8') as stopwordfile:
    for line in stopwordfile:
        stop.add(line.strip('\n'))
stop.add('mr')
stop.add('hr')

exclude = set(string.punctuation)  # 标点符号
lemma = WordNetLemmatizer()  # 词干提取


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if (i not in stop) & (i.isalpha())])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    normalized_stop = " ".join(word for word in normalized.split() if (word not in stop) & (word.isalpha()))
    return normalized_stop


files_list = []
d = []
r = ''
f = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\美国议会数据2018txt"):
    r = root
    d = dirs
    f = files
for i in range(len(f)):
    files_list.append(os.path.join(root, f[i]))

doc_clean = []
frequency = []
doc_clean_huawei = []
frequency_huawei = []
doc_clean_ZTE = []
frequency_ZTE = []
top = []
top_huawei = []
top_zte = []

for i in range(196,200):
    f = open(files_list[i], 'r', encoding='utf-8')
    doc = f.read()
    f.close()
    # print(doc)
    sentences = doc.split('.')
    print(sentences)
    mention_CN = []
    mention_huawei = []
    mention_zte = []
    print(sentences)
    for j in range(len(sentences)):
        if ('China' in sentences[j]) or ('Beijing' in sentences[j]) or ('Shanghai' in sentences[j]):

            if (j > 1) & ((j + 1) < len(sentences)):
                l = j - 1
                r = j + 1
                for t in range(l, r):
                    if sentences[t] not in mention_CN:
                        mention_CN.append(sentences[t])
                        print(sentences[t])
            elif j <= 1:
                l = 0
                r = j + 1
                for t in range(l, r):
                    if sentences[t] not in mention_CN:
                        mention_CN.append(sentences[t])
                        print(sentences[t])
            elif (j + 1) >= len(sentences):
                l = j - 1
                r = len(sentences)
                for t in range(l, r):
                    if sentences[t] not in mention_CN:
                        mention_CN.append(sentences[t])
                        print(sentences[t])

        if 'Huawei' in sentences[j]:
            if (j > 1) & ((j + 1) < len(sentences)):
                l = j - 1
                r = j + 1
                for t in range(l, r):
                    if sentences[t] not in mention_huawei:
                        mention_huawei.append(sentences[t])
            elif j <= 1:
                l = 0
                r = j + 1
                for t in range(l, r):
                    if sentences[t] not in mention_huawei:
                        mention_huawei.append(sentences[t])
            elif (j + 1) >= len(sentences):
                l = j - 1
                r = len(sentences)
                for t in range(l, r):
                    if sentences[t] not in mention_huawei:
                        mention_huawei.append(sentences[t])

        if 'ZTE' in sentences[j]:
            if (j > 1) & ((j + 1) < len(sentences)):
                l = j - 1
                r = j + 1
                for t in range(l, r):
                    if sentences[t] not in mention_zte:
                        mention_zte.append(sentences[t])
            elif j <= 1:
                l = 0
                r = j + 1
                for t in range(l, r):
                    if sentences[t] not in mention_zte:
                        mention_zte.append(sentences[t])
            elif (j + 1) >= len(sentences):
                l = j - 1
                r = len(sentences)
                for t in range(l, r):
                    if sentences[t] not in mention_zte:
                        mention_zte.append(sentences[t])

    doc_clean.append(clean('.'.join(mention_CN)))
    fdist = nltk.FreqDist(clean('.'.join(mention_CN)).split())

    for key, values in fdist.items():
        for m in range(int(values)):
            top.append(key)
    fdist = sorted(fdist.items(), key=lambda k: k[1])
    fdist.reverse()
    frequency.append(fdist[0:20])

    doc_clean_huawei.append(clean('.'.join(mention_huawei)))
    fdist = nltk.FreqDist(clean('.'.join(mention_huawei)).split())

    for key, values in fdist.items():
        for m in range(int(values)):
            top_huawei.append(key)
    fdist = sorted(fdist.items(), key=lambda k: k[1])
    fdist.reverse()
    frequency_huawei.append(fdist[0:20])

    doc_clean_ZTE.append(clean('.'.join(mention_zte)))
    fdist = nltk.FreqDist(clean('.'.join(mention_zte)).split())

    for key, values in fdist.items():
        for m in range(int(values)):
            top_zte.append(key)
    fdist = sorted(fdist.items(), key=lambda k: k[1])
    fdist.reverse()
    frequency_ZTE.append(fdist[0:20])

    if mention_zte != []:
        print('ZTE 已完成' + files_list[i])
    if mention_huawei != []:
        print('华为 已完成' + files_list[i])
    print('已完成' + files_list[i])



header_a = ['frequency']
with open(r"美国提及中国的词频_2018.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_a)
    csvwriter.writerows(zip(frequency))
csvfile.close()


header_a = ['frequency']
with open(r"美国提及华为的词频_2018.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_a)
    csvwriter.writerows(zip(frequency_huawei))
csvfile.close()

header_a = ['frequency']
with open(r"美国提及ZTE的词频_2018.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_a)
    csvwriter.writerows(zip(frequency_ZTE))
csvfile.close()


fdist = dict(collections.Counter(top))
print(collections.Counter(top))
print(fdist)
wordcloud = WordCloud(background_color='white')
wordcloud = wordcloud.fit_words(fdist)
plt.imshow(wordcloud)
plt.show()
plt.savefig(r"美国提及中国的词频云图_2018.png")

fdist = dict(collections.Counter(top_huawei))
wordcloud = WordCloud(background_color='white')
if fdist!={}:
    wordcloud = wordcloud.fit_words(fdist)
    plt.imshow(wordcloud)
    plt.show()
    plt.savefig(r"美国提及华为的词频云图_2018.png")



fdist = dict(collections.Counter(top_zte))
if fdist!={}:
    wordcloud = WordCloud(background_color='white')
    wordcloud = wordcloud.fit_words(fdist)
    plt.imshow(wordcloud)
    plt.show()
    plt.savefig(r"美国提及ZTE的词频云图_2018.png")

