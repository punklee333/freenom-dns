# -*- coding: utf-8 -*-
"""
:author: Punk Lee
:datetime: 2020/4/21 22:02
:url: https://punk_lee.gitee.io/
:copyright: ©2020 Punk Lee <punklee333@gmail.com>
"""
from sys import exit
from time import sleep
from random import random
from datetime import datetime
import os, stat, pickle, atexit

from retrying import retry
from requests.utils import cookiejar_from_dict
from requests import Session, ConnectTimeout, ReadTimeout, HTTPError

from . import url
from . import parse
from .utils import print_info, print_warn, get_public_ip, match_ip_address

RETRY_COUNT = 1
RETRY_TIMES = 0


def _retry_on_exception(e):
    global RETRY_COUNT
    _retry = isinstance(e, (ConnectTimeout, ReadTimeout, HTTPError))
    if RETRY_COUNT > RETRY_TIMES:
        print_warn(f'Retry Count > {RETRY_COUNT - 1} Times. Request Aborted.')
        exit()
    elif not _retry:
        print_warn(e)
        exit()
    RETRY_COUNT += 1
    print_warn('Retry + 1')

    return _retry


RETRY_ARGS = {
    'stop_max_attempt_number': 3,
    'wait_random_min': 1000,
    'wait_random_max': 6000,
    'retry_on_exception': _retry_on_exception
}

REQUEST_LAYER_COUNT = 0


def request_handler(func):
    def decorator(self, *args, **kwargs):
        """Request Handler"""
        global RETRY_COUNT
        global REQUEST_LAYER_COUNT
        request_method = args[0]
        request_url = args[1]
        print_prefix = f'│{REQUEST_LAYER_COUNT * 3 * " " + "│" if REQUEST_LAYER_COUNT else ""}'

        # {DEV}
        if self.dev:
            # print_dev(print_prefix, '↓')  # {DEV}
            print(f'{print_prefix}Method:{request_method}')
            print(f'{print_prefix}URL:{request_url}')
            print(f'{print_prefix}Form Data:{kwargs["data"]}') if request_method == 'POST' else None
            print(print_prefix)

        REQUEST_LAYER_COUNT += 1
        """Before the request"""
        # Interval time
        sleep(RETRY_COUNT * random())
        """CORE"""
        resp = func(self, *args, **kwargs)
        """After the request"""
        # {RESET} retry count
        RETRY_COUNT = 1
        # {SAVE} html file
        self.response = resp
        # {UPDATE} token
        self.token = parse.token(resp)
        # {CHECK} logged in
        self.check_login_status(resp)
        # {UPDATE} first get request
        self.first_get_request = True if request_method == 'GET' else self.first_get_request

        REQUEST_LAYER_COUNT = 0
        return resp

    return decorator


class Freenom(Session):
    def __init__(self, username, password, root_path=None, headers=url.HEADERS, dev=False, retry_times=3):
        """
        The Script for managing Freenom.com dns records.
        :param username: your username
        :param password: your password
        :param root_path: cache file path of the program
        :param headers: Freenom.com request headers
        :param retry_times: retry times of per request
        :param dev: debugging mode
        """
        super(Freenom, self).__init__()

        self.root_path = root_path if root_path else os.getcwd()
        self.__locallydata_path = os.path.join(self.root_path, '.freenomdata')
        self.__dev_path = os.path.join(self.root_path, 'dev')
        self.dev = dev
        self.first_get_request = False
        global RETRY_TIMES
        RETRY_TIMES = retry_times

        self.username = username
        self.password = password
        self.get_locally_data()
        self.__response = None
        self.__pub_ip = None
        self.__token = ''
        # Save the file before the end of the program
        atexit.register(self.save_locally_data)

        self.headers = headers
        self.cookies = self.locally_cookies

    def get_locally_data(self):
        try:
            f = open(f'{self.__locallydata_path}', 'rb')
            self.__locally_data = pickle.load(f)
            f.close()
        except Exception:
            # create new freenom_dns cache data file
            self.__locally_data = {
                'cookies': cookiejar_from_dict({}),
                'domains': []
            }
            self.save_locally_data()

        return self.__locally_data

    def save_locally_data(self):
        f = open(f'{self.__locallydata_path}', 'wb')
        # {CACHE} Cookies
        self.__locally_data['cookies'] = self.cookies
        pickle.dump(self.__locally_data, f)
        f.close()

    @property
    def locally_cookies(self):
        return self.__locally_data['cookies']

    @locally_cookies.setter
    def locally_cookies(self, cookies):
        self.__locally_data['cookies'] = cookies

    @property
    def locally_domains(self):
        if not self.__locally_data['domains']:
            self.__locally_data['domains'] = self.domains()
        return self.__locally_data['domains']

    @locally_domains.setter
    def locally_domains(self, domains):
        self.__locally_data['domains'] = domains

    def locally_records(self, domain):
        try:
            return self.__locally_data[domain]
        except Exception:
            self.__locally_data[domain] = self.records(domain)
            return self.__locally_data[domain]

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, resp):
        if self.dev:
            html_text = resp.content.decode(parse.DECODE)
            # create dev folder
            if not os.path.exists(self.__dev_path):
                os.mkdir(self.__dev_path)
                os.chmod(self.__dev_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)
            filename = datetime.now().strftime("%H_%M_%S")
            with open(f'{self.__dev_path}/{filename}.html', 'w', encoding='utf-8') as f:
                f.write(f'<!-- {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->\n')
                f.write(f'<!-- {html_text if html_text else "This request has no response data available."} -->\n')
        self.__response = resp

    @property
    def pub_ip(self):
        if not self.__pub_ip:
            self.__pub_ip = self.get_pub_ip()
        return self.__pub_ip

    @pub_ip.setter
    def pub_ip(self, ip):
        self.__pub_ip = ip

    @property
    def token(self):
        if not self.__token and self.response:
            self.__token = parse.token(self.response)
        return self.__token

    @token.setter
    def token(self, data):
        self.__token = data

    def check_login_status(self, resp):
        # wrong username or password
        if resp.url.find('incorrect=true') != -1:
            print_warn(parse.login_msg(resp))
            exit()
        # do login request
        None if parse.loggedIn(resp) else self.do_login()

    @request_handler
    @retry(**RETRY_ARGS)
    def request(self, *args, **kwargs):
        return super(Freenom, self).request(timeout=RETRY_COUNT * 10, *args, **kwargs)

    @retry(**RETRY_ARGS)
    def get_pub_ip(self, pub_ip_url=''):
        global RETRY_COUNT
        pub_ip_url = pub_ip_url if pub_ip_url else url.PUB_IPS[RETRY_COUNT - 1]
        self.pub_ip = get_public_ip(pub_ip_url, timeout=RETRY_COUNT * 10)
        # {RESET} retry count
        RETRY_COUNT = 1
        return self.pub_ip

    def do_login(self):
        """Do Login..."""
        run = (True if input('Do you want to do login(y/n):').lower().count('y') else False) if self.dev else True
        FORM_DATA = {
            'token': self.token,
            'username': self.username,
            'password': self.password
        }
        # # clear old {COOKIES}
        # self.cookies = cookiejar_from_dict({})
        if run:
            # Send a request to {LOGIN}.
            self.post(url.DO_LOGIN, data=FORM_DATA)
            # # {CACHE} new Cookies
            # self.locally_cookies = self.cookies

    def domains(self):
        """{Request} and {Update} and {Return} All Domain Data"""
        self.get(url.DOMAINS)
        # {CACHE} domains data
        self.locally_domains = data = parse.domains_tbody_data(self.response)
        return data

    def show_domains(self):
        """Show All Domain"""
        tbody = self.domains()
        thead = parse.domains_thead_info(self.response)
        if thead and tbody:
            for domain in tbody:
                print(f'{thead[0]} >>> {domain["domain"]}')
                print(f'{thead[1]} >>> {domain["reg_date"]}')
                print(f'{thead[2]} >>> {domain["exp_date"]}')
                print(f'{thead[3]} >>> {domain["status"]}')
                print(f'{thead[4]} >>> {domain["type"]}')
                print_info('', num=32)
        else:
            print_info('NOTHING')

    def __url_records(self, domain):
        domains_data = self.locally_domains
        domains = [i['domain'] for i in domains_data]
        if not domain in domains:
            print_warn('NO DATA FOUND FOR THIS DOMAIN')
            exit()
        domains_id = [i['id'] for i in domains_data]
        domiansdns_data = dict(zip(domains, domains_id))
        return url.RECORDS % (domain, domiansdns_data[domain])

    def records(self, domain):
        """{Request} and {Return} All Record Data With Domain"""
        self.get(self.__url_records(domain))
        # {CACHE} domain records data
        self.__locally_data[domain] = data = parse.records_tbody_data(self.response)
        return data

    def show_records(self, domain):
        """Show All Record"""
        tbody = self.records(domain)
        thead = parse.records_thead_info(self.response)
        if thead and tbody:
            for record in tbody:
                print(f'{thead[0]} >>> {record["name"]}')
                print(f'{thead[1]} >>> {record["type"]}')
                print(f'{thead[2]} >>> {record["ttl"]}')
                print(f'{thead[3]} >>> {record["target"]}')
                print_info('', 32)
        else:
            print_info('NOTHING')

    def __data_from_records(self, action, record_list):
        FORM_DATA = {}
        FORM_DATA['token'] = self.token
        FORM_DATA['dnsaction'] = action
        action_prefix = 'addrecord' if action == 'add' else 'records'
        for i in range(len(record_list)):
            FORM_DATA[action_prefix + f'[{i}][name]'] = record_list[i]['name']
            FORM_DATA[action_prefix + f'[{i}][type]'] = record_list[i]['type']
            FORM_DATA[action_prefix + f'[{i}][ttl]'] = record_list[i]['ttl']
            FORM_DATA[action_prefix + f'[{i}][value]'] = record_list[i]['target']
        return FORM_DATA

    def __request_record(self, domain, action, record_list):
        request_url = self.__url_records(domain)
        # {Request} GET first
        if not self.first_get_request: self.get(request_url)
        # {Request} POST
        self.post(request_url, data=self.__data_from_records(action, record_list))
        # {PRINT} error|success info
        for msg in parse.record_msg(self.response, all=True):
            print_info(msg)
        # {CACHE} domain records data
        self.__locally_data[domain] = data = parse.records_tbody_data(self.response)
        return data

    def add_record(self, domain, name='', target='', type='', ttl=''):
        """{Request} and {Add} Record Data"""
        record_list = [{
            'name': name.upper(),
            'type': type.upper() if type else 'A',
            'ttl': ttl if ttl else '3600',
            'target': target if target else self.pub_ip
        }]
        return self.__request_record(domain, 'add', record_list)

    def modify_record(self, domain, name='', target='', ttl=''):
        """{Request} and {Modify} Record Data"""
        record_list = []
        for item in self.locally_records(domain):
            modify = True if item['name'] == name.upper() else False
            record_list.append({
                'name': item['name'],
                'type': item['type'],
                'ttl': ttl if modify and ttl else item['ttl'],
                'target': (target or self.pub_ip) if modify else item['target']})
        return self.__request_record(domain, 'modify', record_list)

    def set_record(self, domain, name, *args, **kwargs):
        """{Request} and {Add|Modify} Record Data"""
        return self.modify_record(domain, name, *args, **kwargs) \
            if [i for i in self.locally_records(domain) if i['name'] == name.upper()] \
            else self.add_record(domain, name, *args, **kwargs)

    def set_record_list(self, domain, record_list):
        """{Request} and {Modify} a list Record Data"""
        add_record_list = []
        modify_record_list = []
        total_record_list = [add_record_list, modify_record_list]
        for record in record_list[:]:
            name = record.get('name')
            if name is None: continue
            name = name.upper()
            _record = {
                'name': name,
                'type': record.get('type', 'A').upper(),
                'ttl': record.get('ttl', '3600'),
                'target': record['target'] if record.get('target') else self.pub_ip
            }
            if not name in [i['name'] for i in self.locally_records(domain)]:
                add_record_list.append(_record)
            modify_record_list.append(_record)
        for i in range(len(total_record_list)):
            record_list = total_record_list[i]
            record_list = ([] if add_record_list == total_record_list[i] else record_list) if i else record_list
            if record_list: self.__request_record(domain, 'modify' if i else 'add', record_list)

    def del_record(self, domain, name, target=None, type=None, ttl=None):
        """{Request} and {Delete} Domain Record Data"""
        target = match_ip_address(target) if target else None
        type = type.upper() if type else None
        name = name.upper()

        records_data = self.locally_records(domain)
        record = {}
        for item in records_data:
            if item['name'] == name and item['target'] == target:
                record = item
                break
            elif item['name'] == name and item['type'] == type:
                record = item
                break
            elif item['name'] == name and item['ttl'] == ttl:
                record = item
                break
            elif item['name'] == name:
                record = item
        # if not record:
        #     print_warn(f'{name.lower()}.{domain} NOT FOUND')
        #     exit()
        # {Request}
        if record:
            self.get(url.PREFIX + record['delete'])
        else:
            print_info(f'{name.lower()}.{domain} NOT FOUND')
        # print error|success info
        print_info(parse.record_msg(self.response))
        # {CACHE} domain records data
        self.__locally_data[domain] = data = parse.records_tbody_data(self.response)
        return data

    def clear_record(self, domain):
        """{Request} and {Clear} All Domain Record Data (USE CAUTION!!!)"""
        records_data = self.locally_records(domain)
        for item in records_data:
            # {Request}
            self.get(url.PREFIX + item['delete'])
        # {CACHE} domain records data
        self.__locally_data[domain] = data = parse.records_tbody_data(self.response)
        if self.locally_records(domain):
            print_info('Not cleared successfully')
        else:
            print_info('All cleared successfully')
        return data
