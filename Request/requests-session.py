import requests

url = 'http://google.com/'

r = requests.get(url)

print(r.status_code)
print(r.text)
print(r.history)
