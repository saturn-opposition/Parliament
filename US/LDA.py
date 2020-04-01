import os
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import  corpora
import csv
from gensim.test.utils import datapath
#获取文件路径名
files_list = []
d = []
r = ''
f = []
for root, dirs, files in os.walk("C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\美国议会数据txt2017"):
   r = root
   d = dirs
   f = files
for i in range(len(f)):
    files_list.append(os.path.join(root,f[i]))

#获取停用词表
stop = set(stopwords.words('english'))

with open(r"C:\Users\hjn\Desktop\大创项目准备\LDA\stopwords\ENstopwords-US.txt",'r', encoding='utf-8') as stopwordfile:
    for line in stopwordfile :
        stop.add(line.strip('\n'))

exclude = set(string.punctuation)                                #标点符号
lemma = WordNetLemmatizer()                                      #词干提取



def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if (i not in stop) & (i.isalpha())])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    normalized_stop = " ".join(word for word in normalized.split() if (word not in stop) & (word.isalpha()))
    return normalized_stop

doc_clean = []

for i in range(len(files_list)):
    f = open(files_list[i],'r',encoding='utf-8')
    doc = f.read()
    f.close()
    doc_clean.append(clean(doc).split())

dictionary = corpora.Dictionary(doc_clean)

# print(len(dictionary))
# dictionary.filter_extremes(no_below=10,no_above= 0.5)           #词必须出现10次以上，但不在20%的文档内出现
# print(len(dictionary))
dictionary.save("C:\\Users\\hjn\\Desktop\\大创项目准备\\LDA\\dictionary")
# dictionary = corpora.Dictionary.load('dictionary')
word = []
id = []
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
print(len(doc_term_matrix))

# ldamodel = gensim.models.ldamulticore.LdaMulticore(doc_term_matrix, num_topics=100, id2word = dictionary, passes=200,eval_every = 1,iterations=2000,workers=3)
ldamodel = gensim.models.ldamodel.LdaModel(doc_term_matrix, num_topics=100, id2word = dictionary,passes=200,eval_every = 1,iterations=2000)
#使用多核LDA模型，workers为多线程数量
temp_file = datapath("model")
ldamodel.save(temp_file)
#保存训练完毕的LDA模型
topic_csv = []
terms = []
print("模型训练结束 ")
for topic in ldamodel.print_topics(num_topics=20):    #输出预测主题（整个文档集的主题）
    termNumber = topic[0]
    topic_csv.append(dictionary[int(topic[0])])
    terms.append(topic[1])
    print(dictionary[int(topic[0])], ':', sep='')
    listOfTerms = topic[1].split('+')
    terms.append(listOfTerms)
    for term in listOfTerms:
        listItems = term.split('*')
        print('  ', listItems[1], '(', listItems[0], ')', sep='')

header = ['topic_id','words']
file_topics = []
index = []
id = []

with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\LDA\\topic_1.1.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(topic_csv,terms))
csvfile.close()

file_topics = []
most_prob_topics = []
most_prob_topics_p = []
for i in ldamodel.get_document_topics(doc_term_matrix)[:]:   #输出每个文档的预测主题并保存
    # listj=[]
    # for j in i:
    #     listj.append(j[1])
    #     bz=listj.index(max(listj))
    print(i)
    topic_str = ''
    max_p = 0
    max_topic = ''
    for j in range(len(i)):

        topic = dictionary[i[j][0]]
        p = i[j][1]
        if p>max_p:
            max_p = p
            max_topic = topic
        if topic_str!='':
            topic_str = topic_str + ';'+topic+':'+str(p)
        else:
            topic_str = topic+':'+str(p)

    file_topics.append(topic_str)
    most_prob_topics.append(max_topic)
    most_prob_topics_p.append(max_p)


    # print(i[bz][0],i,listj,listj.index(max(listj)))
    # print(i[bz][0])
    # id.append(i[bz][0])
    # index.append(listj.index(max(listj)))
header = ['id','topic','first','p']
with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\LDA\\topic_1.2.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(zip(files_list,file_topics,most_prob_topics,most_prob_topics_p))
csvfile.close()
