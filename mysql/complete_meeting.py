import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab', db='parliamentdata1', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接
cursor.execute("select speech_id,meeting_id from meeting_speech")
row = cursor.fetchall()
meeting_speech_dict = {}
for i in range(len(row)):
   if row[i][1] in meeting_speech_dict.keys():
       speech_id_str = meeting_speech_dict[row[i][1]] + ';'+row[i][0]
       meeting_speech_dict[row[i][1]] = speech_id_str
   else:
       meeting_speech_dict[row[i][1]] = row[i][0]
temp_m_id = ''
temp_s_id = ''
one_meeting_country = ''
one_speech_country = ''
meeting_country_dict = {}

for meeting_id,speech_id in meeting_speech_dict.items():
    speech_id_list = speech_id.split(';')
    para_id_list = []
    country_list = []
    for i in range(len(speech_id_list)):
        cursor.execute("select para_id from speech_para where speech_id = \'"+speech_id_list[i]+'\'')
        row = cursor.fetchall()
        if len(row)!=0:

            for t in range(len(row)):
                para_id_list.append(row[t][0])
            for j in range(len(para_id_list)):
                cursor.execute("select para_involve_country from paragraph where para_id = \'" + para_id_list[j] + '\'')
                row = cursor.fetchall()
                for z in range(len(row)):
                    country_list.append(row[z][0])
    country_list = set(country_list)
    country_str = ''.join(country_list)
    print(country_str)
    row = cursor.execute(
        "update meeting set involve_country = \'"+country_str+"\' where meeting_id = \'"+meeting_id+"\'")
    conn.commit()















    # if temp_m_id=='':
    #     temp_m_id = meeting_id[0]
    #     temp_s_id = speech_id[0]
    #     cursor.execute("select para_id from speech_para where speech_id="+temp_s_id)
    #     row = cursor.fetchall()
    #     para_id = row[0]
    #
    #     for t in range(len(para_id)):
    #         cursor.execute("select para_involve_country from paragraph where para_id="+para_id[t])
    #         row = cursor.fetchall()
    #         temp = row[0]
    #         one_speech_country = one_speech_country+temp
    #     one_meeting_country = one_speech_country
    #     one_speech_country = ''
    #
    # if temp_m_id==meeting_id[i]:
    #     temp_s_id = speech_id[i]
    #     cursor.execute("select para_id from speech_para where speech_id="+temp_s_id)
    #     row = cursor.fetchall()
    #     para_id = row[0]
    #
    #     for t in range(len(para_id)):
    #         cursor.execute("select para_involve_country from paragraph where para_id=" + para_id[t])
    #         row = cursor.fetchall()
    #         temp = row[0]
    #         one_speech_country = one_speech_country + ';' + temp
    #     one_meeting_country = one_meeting_country+one_speech_country
    #     one_speech_country = ''
    #
    #
    # if temp_m_id!=meeting_id[i]:
    #     row = cursor.execute(
    #         "insert into meeting(involve_country)values(%s) where meeting_id="+temp_m_id,
    #         (one_meeting_country))
    #     conn.commit()
    #     print(temp_m_id+'处理完毕')
    #     one_meeting_country = ''
    #     temp_m_id = meeting_id[i]
    #     temp_s_id = speech_id[i]
    #     cursor.execute("select para_id from speech_para where speech_id=" + temp_s_id)
    #     row = cursor.fetchall()
    #     para_id = row[0]
    #
    #     for t in range(len(para_id)):
    #         cursor.execute("select para_involve_country from paragraph where para_id=" + para_id[t])
    #         row = cursor.fetchall()
    #         temp = row[0]
    #         one_speech_country = one_speech_country + ';' + temp
    #     one_meeting_country = one_meeting_country + one_speech_country
    #     one_speech_country = ''





