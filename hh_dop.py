import json
import re

import requests
import fake_headers
from bs4 import BeautifulSoup


def web_page_quality(url):
    link_html = requests.get(url,
                             headers=headers.generate()
                             ).text
    return link_html


def main_link(html):
    main_soup = BeautifulSoup(html, features="lxml")

    main_list = main_soup.find("main", "vacancy-serp-content")
    div_tags = main_list.find("div")
    parsed_date = []
    for tag in div_tags:
        t = tag.find("div")
        if t != None:
            tag_a = t.find("a")
            if tag_a != None:
                link = tag_a["href"]
                tag_name = tag_a.span.span.text
                parsed_date.append({
                    "Название": tag_name,
                    "ссылка": link,
                })
    return parsed_date


def description(soup):
    description_list = soup.find("div", [
        "vacancy-description",
        "tmpl_hh_content",
        "vacancy-branded-user-content",
        "g-user-content"
    ]).text
    # job_description = div_list.text
    return description_list


def value_wages(soup):
    wages_div = soup.find('div',
                          'vacancy-title')
    h1 = wages_div.find('h1')
    wages = wages_div.text.replace(h1.text, '')
    return wages


def sity_name(soup):
    del_el = soup.find('div', 'employer-cards-slider--XmyCTYuS7L682S5FDgpM')
    if del_el == None:
        sity = soup.find(['div'],
                         'vacancy-company-redesigned').text.replace(name_comany, '')
    else:
        sity_ = soup.find(['div'],
                          'vacancy-company-redesigned').text.replace(name_comany, '')
        sity = sity_.replace(del_el.text, '')
    if ',' in sity:
        sity = sity[0:sity.find(',')]
    return sity


def salary_in_dollars(wages):
    if '$' in wages:
        print('зарплата в $')
        return True
    else:
        print('зарплата в РУБЛЯХ')
        return False


headers = fake_headers.Headers(browser="chrome", os="win")
main_html = web_page_quality(url="https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")
parsed_date = main_link(main_html)

json_data = {}
for element in parsed_date:
    vacancy_html = web_page_quality(url=element['ссылка'])
    print(element['ссылка'])
    soup = BeautifulSoup(vacancy_html, features="lxml")
    job_description = description(soup)
    wages = value_wages(soup)
    if salary_in_dollars(wages):
        name_comany = soup.find('div', 'vacancy-company-details').text
        sity = sity_name(soup)
        json_data[element['Название']] = {
            'ссылка': element['ссылка'],
            'заработная плата': wages,
            'название компании': name_comany,
            'город': sity
        }

with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)
