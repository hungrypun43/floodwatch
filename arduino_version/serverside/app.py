from flask import Flask, request
import pymongo
import uuid

app = Flask(__name__)

def addpods(data):
    myclient = pymongo.MongoClient("mongodb+srv://root:password32124@try1.xqhda.mongodb.net/test") #My test server link that will change when you install in another server 
    mydb = myclient["floodwatch"]
    mycol = mydb["pods"]
    newpod = {
        "podname": data["podname"],
        "podkey" : str(uuid.uuid4())
    }
    x = mycol.insert_one(newpod)

    print(x)
    return newpod

@app.route("/")
def greeting():
    return "hello"
@app.route("/addpods", methods=["POST"])
def showreq():
    data = request.json
    n = addpods(data)
    print(n)
    return "gotit"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5555', debug=True)
