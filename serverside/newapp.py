from flask import Flask, request, jsonify, make_response
import pymongo
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_cors import CORS, cross_origin
from flask import Flask, request, abort

#linebot
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

Channel_secret = 'a5c7b8e489524fba5ba15b3c9439ee23'
Channel_access_token = '4N3RnBeTGC+Oxrh22LlmEXSx9IWh2/Tbzz1tMatqPsZ8XYnOGmtZ5RkOIlWLwgr7QQ2me54tw6y48gB2i0UaYoLHKzpsxOF3u/JnbSwRt9rzCgKXhUnnbMC7n129+KVzA8/XrjKuUiXZHXUfApKDjQdB04t89/1O/w1cDnyilFU='
basic_id = '@374bcfrv'

line_bot_api = LineBotApi('4N3RnBeTGC+Oxrh22LlmEXSx9IWh2/Tbzz1tMatqPsZ8XYnOGmtZ5RkOIlWLwgr7QQ2me54tw6y48gB2i0UaYoLHKzpsxOF3u/JnbSwRt9rzCgKXhUnnbMC7n129+KVzA8/XrjKuUiXZHXUfApKDjQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a5c7b8e489524fba5ba15b3c9439ee23')
##############################################################################################

app = Flask(__name__)
app.config["SECRET_KEY"] = 'my super secret key'.encode('utf8')
CORS(app, support_credentials=True)

def connect():
    myclient = pymongo.MongoClient("mongodb+srv://root:password32124@try1.xqhda.mongodb.net/test") #My test server link that will change when you install in another server 
    mydb = myclient["floodwatch"]
    return mydb

def addpods(data):
    mydb = connect()
    mycol = mydb["pods"]
    key = str(uuid.uuid4())
    newpod = {
        "podkey" : key,
        "secretkey" : generate_password_hash(data["podpassword"], method='sha256')
    }
    myfeed = mydb["feed"]
    newfeed = {
        "podname": data["podname"],
        "podkey" : key,
        "podstatus": 0,
        "height": 0,
        "setuph": data["sheight"],
        "latitude": data["latitude"],
        "longtitude": data["longtitude"],
        "aware": data["aware"],
        "harm": data["harm"]
    }
    mycol.insert_one(newpod)
    myfeed.insert_one(newfeed)
    return newpod

def findpod_bykey(key):
    mydb = connect()
    mycol = mydb["pods"]
    u = mycol.find_one({'podkey': str(key)})
    print(u)
    return u

def findpoddata_bykey(key):
    mydb = connect()
    mycol = mydb["feed"]
    u = mycol.find_one({'podkey': str(key)})
    print(u)
    return u
    

def p_update(pointer, what, value):
    mydb = connect()
    mycol = mydb["feed"]
    mycol.find_one_and_update({'podkey': pointer},{'$set': {what:value}})
    print("updated")
    mydata = findpoddata_bykey(pointer)
    if what == "height":
        if value < (mydata["aware"]/mydata["setuph"]*100):
            mycol.find_one_and_update({'podkey': pointer},{'$set': {"podstatus":1}})
        elif value < (mydata["harm"]/mydata["setuph"]*100):
            mycol.find_one_and_update({'podkey': pointer},{'$set': {"podstatus":2}})
        else:
            mycol.find_one_and_update({'podkey': pointer},{'$set': {"podstatus":3}})
    findpoddata_bykey(pointer)

#line_bot_api

def broadcast_message(message):
    line_bot_api.broadcast(TextSendMessage(
        text=message))

    return 'Notified Janitors'

def status(postition, status_number):
    if status_number == 2:
        return postition + "มีน้ำท่วมในระดับที่ไม่เหมาะกับการเดินเท้า"
    elif status_number == 3:
        return postition + "มีน้ำท่วมสูงไม่เหมาะกับการนำรถยนต์ขนาดเล็กผ่าน"

################################################################

def token_required(function):
    @wraps(function)
    def decorated(*args,**kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            currentpod = data['public_id']
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        
        return function(currentpod, *args, **kwargs)
    return decorated

@app.route("/")
def greeting():
    mydb = connect()
    mycol = mydb["feed"]
    data = mycol.find()
    resd = []
    print(resd)
    for i in data:
        resd.append({
        "podname": i["podname"],
        "podkey" : i["podkey"],
        "podstatus": i["podstatus"],
        "podlatitude": i["latitude"],
        "podlongtitude": i["longtitude"]})
    res = {"data" : resd}
    return res

@app.route("/auth")
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response({"message": "Not found"}, 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'} )
    user = findpod_bykey(auth.username)
    if not user:
        return make_response({"message": "Not found"}, 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'} )
    if check_password_hash(user["secretkey"], auth.password):
        token = jwt.encode({'public_id' : user["podkey"], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response({"message": "Not found"}, 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'} )

@app.route("/addpods", methods=["POST"])
def create():
    data = request.get_json()
    n = addpods(data)
    print(n)
    res = {
        "podname": data["podname"],
        "podkey": n["podkey"],
        "secretkey": data["podpassword"]
    }
    return res

@app.route("/getpoddata/<keys>", methods=["GET"])
def show(keys):
    #return '%s' % keys
    podauth = findpod_bykey(keys)
    poddata = findpoddata_bykey(keys)
    print(podauth)
    print(poddata)
    #return "ok"
    res = {
        "podname": poddata["podname"],
        "podkey" : podauth["podkey"],
        "podsetupheight": poddata["setuph"],
        "podlatitude": poddata["latitude"],
        "podlongtitude": poddata["longtitude"],
        "podheight": poddata["height"],
        "podstatus" : poddata["podstatus"]
    }
    return res

@app.route("/mydata", methods=["GET"])
@token_required
def showme(currentpod):
    #return '%s' % keys
    podauth = findpod_bykey(currentpod)
    poddata = findpoddata_bykey(currentpod)
    print(podauth)
    print(poddata)
    #return "ok"
    res = {
        "podname": poddata["podname"],
        "podkey": podauth["podkey"],
        "podsetupheight": poddata["setuph"],
        "podlatitude": poddata["latitude"],
        "podlongtitude": poddata["longtitude"],
        "podaware": poddata["aware"],
        "podharm" : poddata["harm"]
    }

    return res
@app.route("/mydata", methods=["PUT"])
@token_required
def editPod(currentpod):
    data = request.get_json()
    p_update(currentpod, "podname", data["podname"])
    p_update(currentpod, "setuph", data["setuph"])
    p_update(currentpod, "latitude", data["latitude"])
    p_update(currentpod, "longtitude", data["longtitude"])
    p_update(currentpod, "aware", data["aware"])
    p_update(currentpod, "harm", data["harm"])
    poddata = findpoddata_bykey(currentpod)
    res = {
        "podname": poddata["podname"],
        "podsetupheight": poddata["setuph"],
        "podlatitude": poddata["latitude"],
        "podlongtitude": poddata["longtitude"],
        "podaware": poddata["aware"],
        "podharm" : poddata["harm"]
    }

    return res

@app.route("/uppod/<keys>", methods=["PUT"])
def uppod(keys):
    data = request.get_json()
    mydata = findpoddata_bykey(keys)
    authdata = findpod_bykey(keys)
    print(authdata["secretkey"])
    secretk = data["secretkey"]
    if check_password_hash(authdata["secretkey"], secretk):
        h = mydata["setuph"] - data["height"]
        p_update(keys, 'height', h)
        mydata = findpoddata_bykey(keys)
        if(mydata["podstatus"]>1):
            broadcast_message(status(mydata["podname"], mydata["podstatus"]))
        res = {
            "message" : "updated",
            "status" : mydata["podstatus"]
        }
        #return res
        return str(mydata["podstatus"])
    res = {
        "message" : "failed"
    }
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5555', debug=True)
