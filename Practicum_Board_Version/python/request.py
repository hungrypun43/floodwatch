import requests

flaskurl = "http://localhost:5555/uppod/"

'''response = requests.get("http://localhost:5555")
print(response.status_code)
print(response.json())
'''

def update(value, publickey, secretkey):
    url = flaskurl + publickey
    print(url)
    print(secretkey)
    print(publickey)
    response = requests.put(url , json = {"secretkey" : secretkey,"height" : value})
    print(response.status_code)
    if response.status_code == 200:
        return(response.text)
    return "0"    
print(update(5, '7a2b463d-b450-432e-a69c-1a14efa7d428', 'toofasttoawake'))