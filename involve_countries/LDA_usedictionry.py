import os
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from  xml.etree import ElementTree as ET
import gensim
from gensim import  corpora
import csv
from gensim import  corpora
from gensim.test.utils import datapath
dictionary = corpora.Dictionary.load('dictionary')        #导入已经建好的词典

xml_files = []
for root, dirs, files in os.walk(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\lords_2009-2018"):

    xml_files.append(files)

for s in range(len(xml_files[0])):
    xml_files[0][s] ='C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords_2009-2018\\' + xml_files[0][s]
xml_files = xml_files[0]

stop = set(stopwords.words('english'))
print(len(stop))
with open(r"C:\Users\hjn\Desktop\大创项目准备\LDA\stopwords\ENstopwords.txt",'r', encoding='utf-8') as stopwordfile:
    for line in stopwordfile :
        stop.add(line.strip('\n'))
stop.add('lord')
stop.add('noble')
print(len(stop))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def preprocessing(filepath):
    passage = []
    root = ET.parse(filepath)
    for node in root.iter():
            passage.append(node.text)
    return passage
def clean(doc):

    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = []
for i in range(len(xml_files)):
    temp = preprocessing(xml_files[i])
    strs = ''.join(str(s) for s in temp if s not in ['NONE','NULL'])
    doc_clean.append(clean(strs).split())

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

print('开始训练模型')
ldamodel = gensim.models.ldamulticore.LdaMulticore(doc_term_matrix, num_topics=100, id2word = dictionary, passes=200,eval_every = 1,iterations=1500,workers=3)
#使用多核LDA模型，workers为多线程数量
temp_file = datapath("model")
ldamodel.save(temp_file)
#保存训练完毕的LDA模型
topic_csv = []
terms = []
print("模型训练结束 ")
for topic in ldamodel.print_topics(num_topics=50):    #输出预测主题（整个文档集的主题）
    termNumber = topic[0]
    topic_csv.append(topic)
    print(topic[0], ':', sep='')
    listOfTerms = topic[1].split('+')
    terms.append(listOfTerms)
    for term in listOfTerms:
        listItems = term.split('*')
        print('  ', listItems[1], '(', listItems[0], ')', sep='')

header = ['topic_id','words']
xml_topics = []
index = []
id = []
with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\LDA\\topic_1.1.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(topic_csv,terms))
csvfile.close()
for i in ldamodel.get_document_topics(doc_term_matrix)[:]:   #输出每个文档的预测主题并保存
    listj=[]
    for j in i:
        listj.append(j[1])
        bz=listj.index(max(listj))
    xml_topics.append(i)

    print(i[bz][0],i,listj,listj.index(max(listj)))
    print(i[bz][0])
    id.append(i[bz][0])
    index.append(listj.index(max(listj)))
header = ['id','topic','index']
with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\LDA\\topic_1.1.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(xml_files,xml_topics))
csvfile.close()
