import json
import logging
from collections import namedtuple

import requests
from lxml import html

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M')


def xpath(response, requests):
    return html.fromstring(response.text).xpath(requests)


def get_with_cookies(url):
    json_file = open(NAME_FILE_JSON)
    json_str = json_file.read()
    json_data = json.loads(json_str)

    cookies = dict()
    for e in json_data:
        cookies[e['name']] = e['value']

    s = requests.Session()
    return s.get(url, cookies=cookies)


def post_with_cookies(url, data):
    json_file = open(NAME_FILE_JSON)
    json_str = json_file.read()
    json_data = json.loads(json_str)

    cookies = dict()
    for e in json_data:
        cookies[e['name']] = e['value']

    s = requests.Session()
    return s.post(url, cookies=cookies, data=data)


def get_list_projects(response):
    names = []
    for name in xpath(response, '//a[contains(concat(" ",normalize-space(@class)," ")," visitable ")]'):
        names.append(name.text)

    links = []
    for link in xpath(response, '//a[contains(concat(" ",normalize-space(@class)," ")," visitable ")]/@href'):
        links.append(link)

    i = 0
    projects = []
    while(i < len(names)):
        projects.append({
            'name': names[i],
            'link': links[i],
        })
        i += 1
    return projects


def send_position(url, amount, comment):
    try:
        r = get_with_cookies(url)
        data = {
            '_qf__addbid': '',
            'qf:token': xpath(r, '//*[@id="qf:token-0"]/@value')[0],
            'amount': amount,
            'currency_code': 'UAH',
            'safe_type': 'split',
            'days_to_deliver': '1',
            'comment': comment,
            'add': ''
        }
    except:
        logging.error('Problem this project..')
        data = {}
    return post_with_cookies(url, data)


def main():
    global NAME_FILE_JSON
    NAME_FILE_JSON = 'data.json'
    for i in range(1, 20):
        link = f'https://freelancehunt.com/projects?page={i}'
        print('Page:', link)  # TODO: remove
        r = get_with_cookies(link)
        projects = get_list_projects(r)

        # Print all projects
        for el in projects:
            print('Link: ', el['link'])  # TODO: remove
            r = send_position(el['link'], 2000,
                              'Добрый вечер! С радостью выполню ваш заказ, имею огромный опыт веб разработки (4 года). Постоянно на связи - обращайтесь!')
            print(r)


if __name__ == "__main__":
    main()
