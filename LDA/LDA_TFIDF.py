from gensim.models import LdaModel,TfidfModel
from gensim import similarities
from gensim import corpora
from gensim.test.utils import datapath
import os
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import matplotlib.pyplot as plt
import math
import random
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s : ', level=logging.INFO)

random.seed(11091987)

def clean(doc):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)  # 标点符号
    lemma = WordNetLemmatizer()  # 词干提取
    stop_free = " ".join([i for i in doc.lower().split() if (i not in stop) & (i.isalpha())])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)

    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())

    normalized_stop = " ".join(word for word in normalized.split() if (word not in stop) & (word.isalpha()))

    return normalized_stop


def create_data(fileholder):#构建数据，先后使用doc2bow和tfidf model对文本进行向量表示
    f = []
    files_list = []
    for root, dirs, files in os.walk(fileholder):
        f = files
    for i in range(len(f)):
        files_list.append(os.path.join(fileholder, f[i]))

    doc_clean = []
    for i in range(len(files_list)):
        f = open(files_list[i], 'r', encoding='utf-8')
        doc = f.read()
        f.close()
        doc_clean.append(clean(doc).split())
    # 对文本进行处理，得到文本集合中的词表
    dictionary = corpora.Dictionary(doc_clean)
    # 利用词表，对文本进行cbow表示
    corpus = [dictionary.doc2bow(text) for text in doc_clean]
    # 利用cbow，对文本进行tfidf表示
    tfidf = TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return files_list,dictionary, corpus, corpus_tfidf

# def lda_model(dictionary,corpus_tfidf):#使用lda模型，获取主题分布
#     lda = LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=20)
#     model = datapath("lda_model")
#     lda.save(model)
#     perplex = lda.per

files_list,dictionary, corpus, corpus_tfidf = create_data(r"C:\Users\hjn\Desktop\议会数据\议会数据\美国议会数据txt")
grid = []

n_topics = 20
lda = LdaModel(corpus_tfidf, num_topics=n_topics, id2word = dictionary,iterations = 500)
model = datapath("lda_model")
lda.save(model)
    # lda.log_perplexity(corpus_tfidf)
    # perplex = lda.bound(corpus_tfidf)
    # grid_1.append(perplex)
    # print(perplex)
    # print("**************************")
top_topics = lda.top_topics(corpus_tfidf)
perplex = math.exp(sum(t[1] for t in top_topics)/n_topics)
    # grid_2.append(perplex)
    # print(perplex)
    # print("**************************")
    # perplex = math.exp(-lda.bound(corpus_tfidf))
    # grid_3.append(perplex)
print(perplex)

grid.append(perplex)

# topics = range(1,50,2)
# plt.plot(topics,grid)


# plt.title("topic_perplexity图")
# plt.savefig(r"C:\Users\hjn\Desktop\议会数据\议会数据\lda.jpg")
# plt.show()






