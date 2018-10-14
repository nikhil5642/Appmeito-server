import database_info
import psycopg2

conn = psycopg2.connect(database=database_info.database, user = database_info.user, 
                    password = database_info.password, host = database_info.host,
                     port =database_info.port)
cursor=conn.cursor()
                     
def user_data_table():
    cursor.execute("create table users(adid varchar primary key,macid varchar,appid varchar,installation_status varchar,user_category varchar, activity json, device_info json, last_modified timestamp default current_timestamp)")    
    conn.commit()

def client_data_table():
    cursor.execute("create table clients(appid varchar primary key,app_secret varchar,creation_timestamp timestamp,modification_timestamp timestamp)")    
    conn.commit()

def event_data_table(app_id,arr_columns):
    command="create table "+app_id+"_events( id serial primary key, adid varchar, macid varchar,appid varchar, lattitude varchar, longitude varchar, pincode varchar"
    for x in arr_columns:
        command=command+","+x+" varchar"
    command=command+",last_modified timestamp)"
    cursor.execute(command)
    conn.commit()

def drop_event_data_table(app_id):
    cursor.execute("drop table "+app_id+"_events")
    conn.commit()
   
#client_data_table()
#user_data_table()
#event_data_table("appmeito",['page'])
        
    
