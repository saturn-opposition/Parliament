import csv
with open(r"C:\Users\hjn\Desktop\大创项目准备\提取国家\commons_2009-2018.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    country = [row[6] for row in reader]
country_num = []
for i in range(len(country)):
    temp = country[i].split(';')
    country_num.append(len(temp))
heading = ['num']
with open("C:\\Users\\hjn\\Desktop\\大创项目准备\\提取国家\\数量.csv", "w", encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(heading)
    csvwriter.writerows(zip(country_num))
csvfile.close()
