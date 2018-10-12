import database_info
import psycopg2
import json
conn = psycopg2.connect(database=database_info.database, user = database_info.user, 
                    password = database_info.password, host = database_info.host,
                     port =database_info.port)
cursor=conn.cursor()

def user_activity(adid,appid,activity):
    cursor.execute("select activity from users where appid='%s' and adid='%s'"%(appid,adid))
    data=cursor.fetchall()[0][0]
    data.append(activity)
    cursor.execute("update users set activity='%s' where adid='%s' and appid='%s'"%(json.dumps(data),adid,appid))
    conn.commit()

