import json
import requests
import hashlib
from hashToCurve import hashToCurve,powMod,ep
import datetime

def request(tablename,H):
    url = "http://localhost:5000/api/requests"
    headers = {'content-type': 'application/json'}
    requestData = {"table_name": tablename, "H": H}
    ret = requests.post(url, json=requestData, headers=headers)
    if ret.status_code == 200:
        text = json.loads(ret.text)
        print(text)
    return text

print("please input username:")
u=input()
print("please input password:")
p=input()

start = datetime.datetime.now()

##client
b=10

u=u+p
m=hashlib.sha224()
m.update(u.encode('utf-8'))
m.digest()
u=m.hexdigest()
#print('u:\t',u)
h=int(u,16)
H=hashToCurve(h)
print("H:\t",H)
#取u前两个字节作为表名存储盲化后的用户名H
#table_name=u.encode('utf-8')
table_name=u[:2]
table_name="bucket_"+table_name
#TODO:将u进行盲化处理
u=powMod(H,b,ep.p)
#table_name=table_name.decode('utf-8', errors='ignore')
print("table_name:\t",table_name)
print("username:\t",u)

result=request(table_name,u)

end = datetime.datetime.now()
print("using time:\t",end-start)
##server
