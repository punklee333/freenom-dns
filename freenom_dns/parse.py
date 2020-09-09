# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:datetime: 2020/9/3 21:13
:url: https://punk_lee.gitee.io/
:copyright: ©2020 Punk Lee <punklee333@gmail.com>
"""
from lxml import etree
from lxml.html import parse as lxml_parse
import re

DECODE = 'utf-8'

def parse(resp, xpath):
    if not resp:
        return []
    text = resp.content.decode(DECODE)
    html = etree.HTML(text)
    return html.xpath(xpath)

def parse_file(path, xpath):
    """dev use"""
    html = lxml_parse(path)
    return html.xpath(xpath)

def token(resp):
    token = parse(resp, '//input[@name="token"]/@value')
    return token.pop() if token else ''

def login_msg(resp):
    msg = parse(resp, '//div[contains(@class,"error-message")]/p/text()')
    return msg.pop() if msg else ''

def record_msg(resp, all=False):
    msg = parse(resp, '//div[@class="recordslist"]//li/text()')
    if not all:
        msg = msg.pop() if msg else ''
    return msg

def loggedIn(resp):
    return 'loggedIn' in ''.join(parse(resp, '//body/@class'))

def domains_thead_info(resp):
    thead = parse(resp, '//*[@id="bulkactionform"]//thead//th//text()')
    thead = [i for i in thead if i.strip()]

    return thead

def domains_tbody_data(resp):
    domains_data = []
    tbody = parse(resp, '//*[@id="bulkactionform"]//tbody//tr')
    for tr in tbody:
        json_data = {}
        json_data['domain'] = ''.join(tr.xpath('.//td[1]/a/text()')).strip()
        json_data['reg_date'] = ''.join(tr.xpath('.//td[2]/text()')).strip()
        json_data['exp_date'] = ''.join(tr.xpath('.//td[3]/text()')).strip()
        json_data['status'] = ''.join(tr.xpath('.//td[4]/span/text()')).strip()
        json_data['type'] = ''.join(tr.xpath('.//td[5]/text()')).strip()
        json_data['href'] = ''.join(tr.xpath('.//td[6]//a/@href')).strip()
        result = re.search(r'id=(.*)', json_data['href'])
        json_data['id'] = result.group(1) if result else ''
        domains_data.append(json_data)

    return domains_data

def records_thead_info(resp):
    thead = parse(resp, '//*[@id="recordslistform"]//thead//th//text()')
    thead = [i for i in thead if i.strip()]

    return thead

def records_tbody_data(resp):
    records_data = []
    tbody = parse(resp, '//*[@id="recordslistform"]//tbody/tr')
    for tr in tbody:
        json_data = {}
        json_data['name'] = ''.join(tr.xpath('./td[@class="name_column"]//input[@type="text"]/@value')).strip()
        json_data['type'] = ''.join(tr.xpath('./td[@class="type_column"]//text()')).strip()
        json_data['ttl'] = ''.join(tr.xpath('./td[@class="ttl_column"]//input[@type="text"]/@value')).strip()
        json_data['target'] = ''.join(tr.xpath('./td[@class="value_column"]//input[@type="text"]/@value')).strip()
        del_href = ''.join(tr.xpath('./td[@class="delete_column"]//button[@type="button"]/@onclick'))
        del_href = re.search(r"href='(.*)'", del_href)
        json_data['delete'] = del_href.group(1) if del_href else ''
        records_data.append(json_data)

    return records_data