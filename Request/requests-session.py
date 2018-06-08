import requests

url = 'http://171.221.172.13:8888/lottery/accept/searchDetails'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cookie': 'JSESSIONID=1FBEC40FD1D9FA75D4576171DC78D905; route=bdec837c7e1c29abc7e4a1324bbfe784',
    'Upgrade-Insecure-Requests': '1'
}

r = requests.get(url, headers=headers)

print(r.status_code)
print(r.text)
print(r.history)
