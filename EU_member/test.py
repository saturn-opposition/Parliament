import csv
import re
# chair = ''
# member = ''
# substitute = ''
# with open(r"D:\大创项目-新\欧盟议员信息库\EuPerson\101039\2-HOME.csv", 'r', encoding='utf-8') as f:
#             reader = csv.reader(f)
#             header = []
#             n = 0
#             items = []
#             for row in reader:
#                 if n == 0:
#                     for j in range(len(row)):
#                         header.append(row[j])
#                     n = 9
#                 else:
#                     for j in range(len(row)):
#                         items.append(row[j])
#
#             print(len(header))
#             print(len(items))
#             print(items)
            # chair = c[1].replace('\'','').replace('[','').replace(']','')
            # member = m[1].replace('\'','').replace('[','').replace(']','')
            # substitute = s[1].replace('\'','').replace('[','').replace(']','')
# print(chair)
# print(member)
# print(substitute)

# with open(r"D:\大创项目-新\欧盟议员信息库\EuPerson\840\3-DEBATES.csv" ,'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     t = []
#     c = 1
#     for row in reader:
#         if c ==1:
#             c = 2
#             pass
#         else:
#                 t.extend(row)
# meet_name = []
# meet_date = []
# speech = []
#
# for j in range(len(t)):
#     splits = t[j].split('\': ')
#     meet_name.append(splits[1][0:-13])
#     meet_date.append(splits[2][0:-10])
#     speech.append(splits[3][0:-2])



Accredited_assistants = []
grouping = []
pay = []
with open(r"D:\大创项目-新\欧盟议员信息库\EuPerson\197746\7-ASSISTANTS.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        n = 0
        header = []
        items = []
        for row in reader:
            if n == 0:
                print(row)
                for j in range(len(row)):
                    header.append(row[j])
                n = 9
            else:
                for j in range(len(row)):
                    items.append(row[j])
        for j in range(len(header)):
            if "Accredited assistants" in header[j]:
                acc = items[j].replace('\'', '').replace('[', '').replace(']', '')
            if "Service providers" in header[j]:
                members = items[j].replace('\'', '').replace('[', '').replace(']', '')
            if "substitute" in header[j]:
                substitute = items[j].replace('\'', '').replace('[', '').replace(']', '')
acc = Accredited_assistants[1].replace('\'', '').replace('[', '').replace(']', '').split(',')
gro = grouping[1].replace('\'', '').replace('[', '').replace(']', '').split(',')
pa = pay[1].replace('\'', '').replace('[', '').replace(']', '').split(',')
print(acc)
print(gro)
print(pa)