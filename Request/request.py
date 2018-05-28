import requests

domain = 'http://10.17.2.175'
token = ''

# post: get auth token
'''
post: 支持的参数
url=string
# data/json/files不能混用
data=dict()
json=json.dumps()
files=dict()
'''

url = domain + ':8882/api/authorizations'
body = {
    'login_name': '2R33302X323B'
}

r = requests.post(url, data=body)
if r.status_code == 201:
    token = 'Bearer ' + r.json()['content']['token']
else:
    exit('request error...')


'''
# ================================================
# post: files
# note: 这里的token要保证是在同一台服务器上生成的token
#       上面生成的端口应改为8889
url = domain + ':8887/api/picture'
headers = {
    'Authorization': token,
    'AppId': '1'
}
files = {
    'picture': open(r'C:\Koala.jpg', 'rb')
}

picture = requests.post(url, headers=headers, files=files)

print(picture.json())

# ================================================
'''


# get:
url = domain + ':8883/api/resellers'
params = {
    'page': 1,
    'per_page': 10
}
headers = {
    'Authorization': token
}
data = requests.get(url, params=params, headers=headers)

print(data.json())
