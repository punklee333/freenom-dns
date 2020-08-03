# -*- coding: utf-8 -*-
from freenom_dns import Freenom

if __name__ == '__main__':
    freenom = Freenom('your username', 'your password')
    ###################################################
    pub_ip = freenom.get_public_ip()

    # add or modify a record
    freenom.set_record('your domain', '', 'a', pub_ip)
    freenom.set_record('your domain', 'www', 'a', pub_ip)

    # delete a record
    freenom.del_record('your domain', 'www')

    # show all records with domain
    freenom.show_records('your domain')
