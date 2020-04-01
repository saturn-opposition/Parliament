import os
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

doc = []
for i in range(len(files_list)):
    f = open(files_list[i], 'r', encoding='utf-8')
    t = f.read()
    f.close()
    doc.append(t)
    print('已完成'+files_list[i])
str_2017 = '.'.join(doc)

with open('C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\2017.txt','w',encoding='utf-8') as f:    #设置文件对象
     f.write(str_2017)