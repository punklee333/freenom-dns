# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:datetime: 2020/8/3 15:18
:url: https://punk_lee.gitee.io/
:copyright: ©2020 Punk Lee <punklee333@gmail.com>
"""
import requests, re

NUM = 50

def print_dev(text, sym='-', align='<', num=NUM):
    print(f'{f"{text}":{sym}{align}{num}}')

def print_info(text, num=NUM):
    print(f'{f"{text}":-^{num}}')

def print_warn(text, num=NUM):
    print(f'{f"{text}":#^{num}}')


def get_public_ip(url=None, timeout=12):
    """
    Get Public IP Address
    :param url: public ip api address
    :type url: str
    :return: ip address
    """
    resp = requests.get(url, timeout=timeout).text
    return match_ip_address(resp)


def match_ip_address(ip):
    pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
    result = pattern.search(ip)
    return result.group() if result else ''


def counter(array):
    data = dict()
    for key in array:
        data[key] = data.get(key, 0) + 1

    return data
