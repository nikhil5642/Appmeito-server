from flask import Flask,jsonify,request
import database_info
import psycopg2
import insert
import update

conn = psycopg2.connect(database=database_info.database, user = database_info.user, 
                    password = database_info.password, host = database_info.host,
                     port =database_info.port)
cursor=conn.cursor()

def check_auth(request):
    try:
        app_id=request.headers['app_id']
        app_secret=request.headers['app_secret']
        cursor.execute("select * from clients where appid='%s' and app_secret='%s'"%(app_id,app_secret))
        if(cursor.rowcount!=0):
            return True
        else:
            return False        
    except:
            return False
    

app=Flask(__name__)
@app.route("/test")
def test():
    return jsonify(success=False,message="Invalid Authentication")
@app.route("/event_data",methods=['POST'])
def event_data():
    if(check_auth(request)==False):
        return jsonify(success=False,message="Invalid Authentication")
    try: 
        data=request.get_json(force=True)
        adid=data['adid']
        macid=data['macid']
        appid=data['appid']
        event_json=data['event_json']
        for event in event_json:
            lattitude=event['lattitude']
            longitude=event['longitude']
            zipcode=event['code']
            event_now=event['event']
            timestamp=event['timestamp']
            insert.new_event_data(adid,macid,appid,lattitude,longitude,zipcode,event_now,timestamp)
        return jsonify(success=True,message=None)
    except:
        return jsonify(success=False,message="Invalid body")

@app.route("/user_installation",methods=['POST'])
def user_installation():
    if(check_auth(request)==False):
        return jsonify(success=False,message="Invalid Authentication")
    try:
        data=request.get_json(force=True)
        adid=data['adid']
        macid=data['macid']
        appid=data['appid']
        installation_status='installed'
        user_category=None
        activity=data['activity']
        device_info=data['device_info']
        cursor.execute("select * from users where adid='%s' and appid='%s'"%(adid,appid))
        if(cursor.rowcount!=0):
            update.user_activity(adid,appid,activity)
        else:
            insert.new_user(adid,macid,appid,installation_status,user_category,activity,device_info)
        return jsonify(success=True,message=None)
    except:
        return jsonify(success=False,message="Invalid body")

@app.route("/user_uninstallation",methods=['POST'])
def user_uninstallation():
    if(check_auth(request)==False):
        return jsonify(success=False,message="Invalid Authentication")
    try:
        data=request.get_json(force=True)
        adid=data['adid']
        macid=data['macid']
        appid=data['appid']
        installation_status='uninstalled'
        user_category=None
        activity=data['activity']
        device_info=data['device_info']
        update.user_activity(adid,appid,activity)
        return jsonify(success=True,message=None)
    except:
        return jsonify(success=False,message="Invalid body")

