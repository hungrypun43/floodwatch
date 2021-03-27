from flask import Flask, request
import pymongo
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = 'my super secret key'.encode('utf8')

def connect():
    myclient = pymongo.MongoClient("mongodb+srv://root:password32124@try1.xqhda.mongodb.net/test") #My test server link that will change when you install in another server 
    mydb = myclient["floodwatch"]
    return mydb

def addpods(data):
    #myclient = pymongo.MongoClient("mongodb+srv://root:password32124@try1.xqhda.mongodb.net/test") #My test server link that will change when you install in another server 
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
        "setuph": data["sheight"]
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

@app.route("/")
def greeting():
    return "hello"

@app.route("/auth")
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return "Not found"
    user = findpod_bykey(auth.username)
    if not user:
        return "Not found"
    if check_password_hash(user["secretkey"], auth.password):
        return "welcome" + user["podname"]
    return "fail"

@app.route("/addpods", methods=["POST"])
def create():
    data = request.get_json()
    n = addpods(data)
    print(n)
    return "gotit"

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
        "podseckey": podauth["secretkey"],
        "podsetupheight": poddata["setuph"]
    }
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5555', debug=True)
