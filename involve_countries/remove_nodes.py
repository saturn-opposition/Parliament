import xml.etree.ElementTree as ET
import os
import  xml.dom.minidom
xml_files = []
# for root, dirs, files in os.walk("C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords"):
#
#     xml_files.append(files)
#
#
# for s in range(len(xml_files[0])):
#     xml_files[0][s] =  'C:\\Users\\hjn\\Desktop\\议会数据\\议会数据\\英国议会数据xml格式\\lords\\' + xml_files[0][s]
# xml_files = xml_files[0]
#
# for file_loc in xml_files:
#     tree = ET.parse(file_loc)
#     root = tree.getroot()
#     for i in root.findAll():
#         if i.nodeName == 'a':
#             i.remove()
#             print("删除a"+file_loc)
#         if i.nodeName == 'phrase':
#             i.remove()
#             print('删除phrase'+file_loc)
#         if i.nodeName == 'i':
#             i.remove()
#             print('删除i'+file_loc)

dom = xml.dom.minidom.parse(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\lords\2004-06-22a.xml")
root = dom.documentElement
# for i in range(len(root.childNodes)):
speech = dom.getElementsByTagName('speech')
print(len(speech))

words = []
for i in range(len(speech)):

    pnode = speech[i].getElementsByTagName('p')
    temp = ''


    for node in pnode:


            temp = temp + node.firstChild.data
    words.append(temp)
for i in words:
    print(i)
    print("*************************************")



