import requests

key = input('Введите Global API ключ: ')
email = input('Введите почту от аккаунта Cloudflare: ')

headers = {
    "Content-Type": "application/json",
    "X-Auth-Key": key,
    "X-Auth-Email": email
}
url = "https://api.cloudflare.com/client/v4/zones"
response = requests.request("GET", url, headers=headers)
zones = response.json()['result']
for page in range(2, response.json()['result_info']['total_pages'] + 1):
    url = f"https://api.cloudflare.com/client/v4/zones?page={page}"
    response = requests.request("GET", url, headers=headers)
    zones += response.json()['result']

print('Всего  зон: ', len(zones))

data = {"id":"ech","value":"off"}
i = 0
for zone in zones:
    r = requests.patch(f'https://api.cloudflare.com/client/v4/zones/{zone["id"]}/settings/ech', headers=headers, json=data)
    i += 1
    if r.json()['success']:
        print('Status: ' + str(r.json()['success']) + ", num " + str(i))
    else:
        print('Status: False, Error: ' + str(r.json()) + ', zone name: ' + zone['name'])
