import json
import logging
from collections import namedtuple

import requests
from lxml import etree, html

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M')


def get_with_cookies(url, json_file=None):
    '''Функция возвращает html-разметку у запрашиваемого сайта, используя cookies'''
    cookies = dict()
    if(json_file == None):
        json_file = open(json_file)
        json_str = json_file.read()
        json_data = json.loads(json_str)

        for e in json_data:
            cookies[e['name']] = e['value']

    s = requests.Session()
    return s.get(url, cookies=cookies)


def get_list_projects(response):
    '''Функция возвращает список проектов из предоставленой html-разметки'''
    tree = html.fromstring(response.text)

    names = []
    for name in tree.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," visitable ")]'):
        names.append(name.text)

    links = []
    for link in tree.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," visitable ")]/@href'):
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
    namefile_json = 'data'
    response = get_with_cookies(
        'https://freelancehunt.com/projects?skills%5B%5D=124', namefile_json)
    projects = get_list_projects(response)

    for el in projects:
        print(el['link'])

if __name__ == "__main__":
    main()
