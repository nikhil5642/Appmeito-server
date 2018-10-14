from datetime import datetime
import database_info
import psycopg2
import json

conn = psycopg2.connect(database=database_info.database, user = database_info.user, 
                    password = database_info.password, host = database_info.host,
                     port =database_info.port)
cursor=conn.cursor()

def new_client(app_id,app_secret):
    dt=datetime.now() 
    cursor.execute("insert into clients(appid,app_secret,creation_timestamp,modification_timestamp) values(%s,%s,%s,%s)",(app_id,app_secret,dt,dt))
    conn.commit()
    
def new_user(adid,macid,appid,installation_status,user_category,activity,device_info):
    cursor.execute("insert into users(adid,macid,appid,installation_status,user_category, activity, device_info) values(%s,%s,%s,%s,%s,%s,%s)",(adid,macid,appid,installation_status,user_category,json.dumps([activity]),json.dumps(device_info)))
    conn.commit()

def new_event_data(adid,macid,appid,lattitude,longitude,zipcode,event_json,time):
    col_arr=event_json.keys()
    command="insert into "+appid+"_events(adid , macid, appid, lattitude, longitude, pincode"
    for i in col_arr:
        command=command+","+i
    command=command+",last_modified) values('%s','%s','%s','%s','%s','%s'"%(adid,macid,appid,lattitude,longitude,zipcode)   
    for i in col_arr:
        command=command+(",'%s'"%(event_json[i]))
    command=command+",'%s')"%datetime.fromtimestamp(time/1000.0)
    cursor.execute(command)
    conn.commit()

#new_client('appmeito','appmeito_test')