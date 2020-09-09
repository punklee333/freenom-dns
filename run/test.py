# -*- coding: utf-8 -*-
from freenom_dns import Freenom

if __name__ == '__main__':
    your_username = 'your username'
    your_password = 'your password'
    your_domain = 'your domain'
    freenom = Freenom(your_username, your_password)

    """
    Get Public IP Address
    —————————————————————
    """
    # pub_ip = freenom.pub_ip
    # pub_ip = freenom.get_pub_ip()

    """
    Domains(GET) >>> Return or Show
    ———————————————————————————————
    """
    # domains = freenom.domains()
    # freenom.show_domains()

    """
    Records(GET) >>> Return or Show
    ———————————————————————————————
    """
    # records = freenom.records(your_domain)
    # freenom.show_records(your_domain)

    """
    Record(POST) >>> Add or Modify or Set
    —————————————————————————————————————
    """
    "Add One Record"
    # freenom.add_record(your_domain)  # default: public ip
    # freenom.add_record(your_domain, 'www')  # default: public ip
    # freenom.add_record(your_domain, 'www', '192.168.1.1')
    # freenom.add_record(your_domain, '_dnsauth', type='txt', ttl='3000', target='33333333')
    "Modify One Record: (if the record exists then modify)"
    # freenom.modify_record(your_domain)  # default: public ip
    # freenom.modify_record(your_domain, 'www')  # default: public ip
    # freenom.modify_record(your_domain, 'www', '192.168.2.2')
    # freenom.modify_record(your_domain, '_dnsauth', ttl='2800', target='88888888')
    "Set One Record: (Add or Modify)"
    # freenom.set_record(your_domain, 'my')
    # freenom.set_record(your_domain, 'my', '0.0.0.0')
    "Set Record List: (Beta)"
    # record_list:
    # {name}: *required!!!
    # {type}: default: A
    # {ttl}: default: 3600
    # {target}: default: your Public IP
    record_list = [
        {'name': ''},  # default: public ip
        {'name': 'www', 'target': '100.100.100.100'},
        {'name': '_dnsauth', 'type': 'txt', 'ttl': '2800', 'target': '22222222'}]
    # freenom.set_record_list(your_domain, record_list)

    """
    Record(GET) >>> Delete
    ——————————————————————
    """
    "Delete One Record"
    # freenom.del_record(your_domain, 'www')
    "Clear All Record (Beta ???DANGER!!!)"
    # freenom.clear_record(your_domain)
