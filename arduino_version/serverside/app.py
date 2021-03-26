from flask import Flask, request
import pymongo
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = 'my super secret key'.encode('utf8')

def addpods(data):
    myclient = pymongo.MongoClient("mongodb+srv://root:password32124@try1.xqhda.mongodb.net/test")
    mydb = myclient["floodwatch"]
    mycol = mydb["pods"]
    newpod = {
        "podname": data["podname"],
        "podkey" : str(uuid.uuid4()),
        "secretkey" : generate_password_hash(data["podpassword"], method='sha256')
    }
    x = mycol.insert_one(newpod)

    print(x)
    return newpod
def findpod_bykey(key):
    myclient = pymongo.MongoClient("mongodb+srv://root:password32124@try1.xqhda.mongodb.net/test")
    mydb = myclient["floodwatch"]
    mycol = mydb["pods"]
    u = mycol.find_one({'podkey': key})
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
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5555', debug=True)