# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:datetime: 2020/8/3 15:18
:url: https://punk_lee.gitee.io/
:copyright: ©2020 Punk Lee <punklee333@gmail.com>
"""
import os

PUB_IPS = ['https://api.ipify.org', 'http://ipinfo.io/ip', 'https://ipecho.net/plain']

HEADERS = {}
HEADERS['Host'] = os.getenv('URL_HOST', 'my.freenom_dns.com')
HEADERS['referer'] = os.getenv('URL_REFERER', 'https://my.freenom.com/clientarea.php')
HEADERS['User-Agent'] = os.getenv('URL_USER_AGENT',
                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36')

HOME = os.getenv('URL_HOME', 'https://www.freenom.com')
PREFIX = os.getenv('URL_PREFIX', 'https://my.freenom.com/')
DO_LOGIN = os.getenv('URL_DO_LOGIN', PREFIX + 'dologin.php')
DOMAINS = os.getenv('URL_DOMAINS', PREFIX + 'clientarea.php?action=domains')
RECORDS = os.getenv('URL_DOMAIN_DNS', PREFIX + 'clientarea.php?managedns=%s&domainid=%s')
RECORDS_DEL = os.getenv('URL_DOMAIN_DNS', PREFIX + 'clientarea.php?dnsaction=delete&managedns=%s&name=%s&records=%s&ttl=%s&value=%s&domainid=%s')