import csv
involve_country = []
with open(r"D:\大创项目\US\美国国家词频.csv", "r", encoding='utf-8', newline='') as csvfile:
    reader = csv.reader(csvfile)
    involve_country = [row[1] for row in reader]
with open(r"D:\大创项目\US\预处理数据.txt", "w", encoding='utf-8') as file:
    for i in range(1,len(involve_country)):
        countrystr = involve_country[i].replace(',',';')
        countrystr = countrystr.replace(' ', '')
        file.write('%0 科研立项\n%K '+countrystr+'\n%W CNKI\n\n')
        print(i)
import pymysql
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='canada', charset='utf8')
# cursor = conn.cursor()
# cursor.execute("select involve_country from file")
# row = cursor.fetchall()

# with open(r"C:\Users\hjn\Desktop\大创项目\Canada\预处理数据-Canada.txt", "w", encoding='utf-8') as file:
#     for i in range(len(row)):
#         if (row[i][0] !='')&(row[i][0] !=None):
#             countrystr = row[i][0].replace(',', ';')
#             countrystr = countrystr.replace(' ', '')
#             file.write('%0 科研立项\n%K ' + countrystr + '\n%W CNKI\n\n')
#             print(i)