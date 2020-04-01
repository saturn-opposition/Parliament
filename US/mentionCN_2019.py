#encoding = utf8
import os
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import nltk
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
stop = set(stopwords.words('english'))
print(len(stop))
with open(r"C:\Users\hjn\Desktop\大创项目\LDA\stopwords\ENstopwords-US.txt",'r', encoding='utf-8') as stopwordfile:
    for line in stopwordfile :
        print(line.strip('\n'))
        stop.add(line.strip('\n'))
stop.add('mr')
stop.add('hr')
print(len(stop))
exclude = set(string.punctuation)                                #标点符号
lemma = WordNetLemmatizer()                                      #词干提取


def clean(doc):

    stop_free = " ".join([i for i in doc.lower().split() if (i not in stop)&(i.isalpha())])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    normalized_stop = " ".join(word for word in normalized.split() if (word not in stop)&(word.isalpha()))
    return normalized_stop

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


doc_clean = []
frequency = []
for i in range(len(files_list)):
    f = open(files_list[i],'r',encoding='utf-8')
    doc = f.read()
    f.close()
    doc_clean.append(clean(doc))

    fdist = nltk.FreqDist(clean(doc).split())

    fdist = sorted(fdist.items(), key=lambda k: k[1])
    fdist.reverse()
    frequency.append(fdist[0:20])

    print('已完成'+files_list[i])

doc_clean = '.'.join(doc_clean)
fdist = nltk.FreqDist(clean(doc_clean).split())
wordcloud = WordCloud(background_color='white')
wordcloud = wordcloud.fit_words(fdist)
plt.imshow(wordcloud)
plt.show()
plt.savefig(r"C:\Users\hjn\Desktop\美国词频云图_2019.png")


header_a = ['frequency']
with open(r"C:\Users\hjn\Desktop\美国词频_2019.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header_a)
    csvwriter.writerows(zip(frequency))
csvfile.close()



