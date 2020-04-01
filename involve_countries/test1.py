# from gensim import  corpora
# dictionary = corpora.Dictionary.load('dictionary')
#
# del_list = []
# for i in range(46):
#     for key in dictionary.token2id.keys():
#         del_list.append(key)
# for i in range(len(del_list)):
#     del dictionary[del_list[i]]
# temp = 0
# for key,value in dictionary.token2id.items():
#     temp = value-46
#     dictionary[key]=temp
#
# print(dictionary.token2id)


from  xml.etree import ElementTree as ET

root = ET.parse(r"C:\Users\hjn\Desktop\议会数据\议会数据\英国议会数据xml格式\commons\1935-12-04a.xml")

for node in root.findall('speech'):
       speaker_id = node.get('speakerid')
       if speaker_id!=None:
        speaker_name = node.get('speakername')
        url = 'https://www.publicwhip.org.uk/mp.php?id='+speaker_id
        hansard_membership_id = node.get('hansard_membership_id')
       print(node.text)
       print("***************************************************")
