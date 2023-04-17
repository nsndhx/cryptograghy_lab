import json
import requests
import hashlib
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
a=2

u=u+p
m=hashlib.sha224()
m.update(u.encode('utf-8'))
m.digest()
u=m.hexdigest()
print('u:\t',u)
h=int(u,16)
print("H^a:\t",h)
#TODO:将u进行盲化处理
#H=h**b
#取u前两个字节作为表名存储盲化后的用户名H
#table_name=u.encode('utf-8')

table_name=u[:4]
table_name="bucket_"+table_name
#table_name=table_name.decode('utf-8', errors='ignore')
print("table_name:\t",table_name)

result=request(table_name,h)

end = datetime.datetime.now()
print("using time:\t",end-start)
##server
