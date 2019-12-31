import json
import logging
from collections import namedtuple

import requests
from lxml import etree, html

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


def main():
    global NAME_FILE_JSON
    NAME_FILE_JSON = 'data.json'

    r = get_with_cookies(
        'https://freelancehunt.com/projects?skills%5B%5D=124')
    projects = get_list_projects(r)

    # for el in projects:
    #     r2 = get_with_cookies(el['link'])
    #     tree = html.fromstring(r2.text)
    #     title = tree.xpath('//title')[0].text
    #     print(title)

    print(projects[0]['link'])
    r = get_with_cookies(projects[0]['link'])

    tree = html.fromstring(r.text)
    data = {
        '_qf__addbid': '',
        'qf:token': tree.xpath('//*[@id="qf:token-0"]/@value')[0],
        'amount': '1234',
        'currency_code': 'UAH',
        'safe_type': 'split',
        'days_to_deliver': '1',
        'comment': 'Здравствуйте. Давайте обсудим в личных сообщениях все моменты) А в целом, сделаю в лучщем виде :)',
        'add': ''
    }
    # r2 = post_with_cookies(projects[0]['link'], data)
    # print(r2.text)


if __name__ == "__main__":
    main()
