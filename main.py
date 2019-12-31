import requests, json

url = 'https://freelancehunt.com/my'

json_file = open('data.json')
json_str = json_file.read()
json_data = json.loads(json_str)
cookies = dict()
for e in json_data:
    cookies[e['name']] = e['value']

s = requests.Session()
r = s.get(url, cookies=cookies)
print(r.text[:200])