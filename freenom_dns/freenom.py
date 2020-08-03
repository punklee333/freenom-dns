# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:datetime: 2020/4/21 22:02
:url: https://punk_lee.gitee.io/
:copyright: ©2020 Punk Lee <punklee333@gmail.com>
"""
import requests, os, json
from retrying import retry
from datetime import datetime
from freenom_dns.utils import is_loggedIn, get_token, get_login_msg
from freenom_dns.utils import get_domains_data, get_records_list, show_result
from freenom_dns.url import *


def _retry_on_exception(e):
    _retry = isinstance(e, (requests.ConnectTimeout,
                            requests.ReadTimeout))
    if not _retry:
        print(e)
        exit()
    return _retry


dkw = {
    'stop_max_attempt_number': 3,
    'wait_random_min': 2000,
    'wait_random_max': 6000,
    'retry_on_exception': _retry_on_exception
}


class Freenom:
    def __init__(self, username, password, dev=False):
        self.username = username
        self.password = password

        self.__path = os.getcwd()
        self.__cookies = os.path.join(os.getcwd(), 'cookies')
        self.__freenomdata = os.path.join(os.getcwd(), 'freenomdata')

        self.session = requests.session()
        self.session.headers = HEADERS
        self.token = ''

        self.dev = dev

    def __save_html(self, html_text, filename='response'):
        if self.dev:
            with open(f'{self.__path}/{filename}.html', 'w', encoding='utf-8') as f:
                time = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                f.write(f'<!--{time}-->\n')
                f.write(html_text)

    @retry(**dkw)
    def __request(self, req, url, **kwargs):
        # send request
        html = req(url, **kwargs).content.decode('utf-8')
        # is loggedIn?
        if not is_loggedIn(html):
            self.do_login()
            raise requests.ConnectTimeout
        # found token
        self.token = get_token(html)

        # save html --dev
        self.__save_html(html)

        return html

    def __get_data(self):
        """get local domain data"""
        data = {}
        try:
            if not os.path.isfile(self.__freenomdata):
                html = self.__request(self.session.get, URLS['domains'])
                # parse html text
                domains_data = get_domains_data(html)
                # save as local file
                f = open(self.__freenomdata, 'w', encoding='utf-8')
                f.write(json.dumps(domains_data))
                f.close()
            with open(self.__freenomdata, encoding='utf-8') as f:
                data = json.loads(f.read())
        except Exception as e:
            print(e)
            exit()

        return data

    def __get_records(self, domain, domain_id):
        url = URLS['domain_dns'] % (domain, domain_id)
        html = self.__request(self.session.get, url)
        return get_records_list(html)

    @retry(**dkw)
    def get_public_ip(self, url=PubIP_URL):
        res = requests.get(url)
        pub_ip = res.content.decode()
        return pub_ip

    def do_login(self):
        html = self.session.get(URLS['login']).content.decode('utf-8')
        token = get_token(html)
        form_data = {
            'token': token,
            'username': self.username,
            'password': self.password
        }

        response = self.session.post(ACTIONS['do_login'], data=form_data)
        if response.url.find('incorrect=true') != -1:
            print(get_login_msg(response.text))
            exit()

    def show_records(self, domain):
        data = self.__get_data()
        if not domain in data:
            print('No data found for this domain')
            exit()
        records = self.__get_records(domain, data.get(domain, ''))
        if records:
            print(f'{domain:-^38}')
            for record in records:
                print(record)
        else:
            print(f'{"No records to display":-^38}')

    def __is_add_record(self, records, name):
        # no records
        if not records:
            return True
        # no name in records
        for record in records:
            if name == record[0]:
                return False

        return True

    def set_record(self, domain, name, type, target, ttl='3600'):
        """add or modify record"""
        data = self.__get_data()
        if not domain in data:
            print('No data found for this domain')
            exit()
        records = self.__get_records(domain, data.get(domain, ''))

        # init params
        url = URLS['domain_dns'] % (domain, data.get(domain, ''))
        name = name.upper()
        type = type.upper()
        ttl = str(ttl)
        target = str(target)
        # add or modify?
        form_data = {}
        form_data['token'] = self.token
        if self.__is_add_record(records, name):
            form_data['dnsaction'] = 'add'
            form_data['addrecord[0][name]'] = name
            form_data['addrecord[0][type]'] = type
            form_data['addrecord[0][ttl]'] = ttl
            form_data['addrecord[0][value]'] = target
        else:
            form_data['dnsaction'] = 'modify'
            for i in range(len(records)):
                if type == records[i][1]:
                    if name == records[i][0]:
                        records[i][3] = target
                form_data[f'records[{i}][name]'] = records[i][0]
                form_data[f'records[{i}][type]'] = records[i][1]
                form_data[f'records[{i}][ttl]'] = records[i][2]
                form_data[f'records[{i}][value]'] = records[i][3]

        # send request
        html = self.__request(self.session.post, url, data=form_data)
        # show result
        show_result(html)

    def del_record(self, domain, name, type='', target='', ttl='3600'):
        """delete record"""
        data = self.__get_data()
        if not domain in data:
            print('No data found for this domain')
            exit()
        records = self.__get_records(domain, data.get(domain, ''))

        # init params
        url = 'https://my.freenom.com/clientarea.php?' \
              'managedns={}&' \
              'records={}&' \
              'dnsaction=delete&' \
              'name={}&' \
              'value={}&' \
              'ttl={}&' \
              'domainid={}'
        name = name.upper()
        type = type.upper()
        ttl = str(ttl)
        target = str(target)
        domain_id = data.get(domain, '')
        if records:
            for record in records:
                if name == record[0]:
                    type = record[1]
                    ttl = record[2]
                    target = record[3]

            # send request
            html = self.__request(self.session.get, url.format(domain, type, name, target, ttl, domain_id))
            # show dns result
            show_result(html)
        else:
            print('no records to delete')
