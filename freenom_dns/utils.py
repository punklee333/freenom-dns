# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:datetime: 2020/8/3 15:18
:url: https://punk_lee.gitee.io/
:copyright: ©2020 Punk Lee <punklee333@gmail.com>
"""
from lxml.html import etree


def parse_html(html, xpath):
    element = etree.HTML(html)
    return element.xpath(xpath)


def is_loggedIn(html):
    return 'loggedIn' in parse_html(html, '//body/@class')[0]


def get_token(html):
    return parse_html(html, '//input[@name="token"]/@value')[0]


def get_login_msg(html):
    return parse_html(html, '//div[contains(@class,"error-message")]/p/text()')[0]


def get_domains_data(html):
    data = {}
    domains = parse_html(html, '//td[@class="second"]//text()')
    domain_hrefs = parse_html(html, '//td[@class="seventh"]//a/@href')
    if domains and domain_hrefs:
        domains = [i.strip() for i in domains[:] if i.strip()]
        id = [i.split('=')[-1] for i in domain_hrefs[:]]
        data = dict(zip(domains, id))
    return data


def get_records_list(html):
    data = []
    records_list = parse_html(html, '//*[@id="recordslistform"]/table/tbody/tr')
    if records_list:
        for record in records_list:
            tmp_list = []
            name = record.xpath('./td[@class="name_column"]//input[@type="text"]/@value')[0]
            type = record.xpath('./td[@class="type_column"]//text()')[0]
            ttl = record.xpath('./td[@class="ttl_column"]//input[@type="text"]/@value')[0]
            target = record.xpath('./td[@class="value_column"]//input[@type="text"]/@value')[0]
            tmp_list.append(name)
            tmp_list.append(type)
            tmp_list.append(ttl)
            tmp_list.append(target)
            data.append(tmp_list)

    return data


def show_result(html):
    xpath_list = ['//div[@class="recordslist"]/ul/li/text()', '//section[@class="domainContent"]//p/text()']
    # show dns result
    for xpath in xpath_list:
        dns_res = parse_html(html, xpath)
        if dns_res:
            print(dns_res[0])
            return
    print('cannot find dns result')
    return
