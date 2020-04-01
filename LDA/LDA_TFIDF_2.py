import os
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import matplotlib.pyplot as plt
import math
import random
import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
from sklearn.decomposition import LatentDirichletAllocation
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

fileholder =''
f = []
files_list = []
for root, dirs, files in os.walk(r'C:\Users\hjn\Desktop\议会数据\LDA测试'):
    f = files
for i in range(len(f)):
    files_list.append(os.path.join(r'C:\Users\hjn\Desktop\议会数据\LDA测试', f[i]))

doc_clean = []
for i in range(len(files_list)):
    f = open(files_list[i], 'r', encoding='utf-8')
    doc = f.read()
    f.close()
    doc_clean.append(clean(doc).split())



tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,stop_words='english')
tf = tf_vectorizer.fit_transform(doc_clean)

grid = []
for i in range(1,50,1):
    n_topics = i

    lda = LatentDirichletAllocation(n_topics=n_topics,
                                max_iter=50,
                                learning_method='batch')
    lda.fit(tf)
    print(lda.perplexity(tf))
    grid.append(lda.perplexity(tf))


topics = range(1,50,1)
plt.plot(topics,grid)


plt.title("topic_perplexity图")
plt.savefig(r"C:\Users\hjn\Desktop\大创项目\LDA\lda.jpg")
plt.show()

