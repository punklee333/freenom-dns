Freenom-dns Script
========================
An unofficial python implementation for managing freenom.com dns records.

## Freenom
Freenom is the world's first and only free domain provider.
## Install
```
# https://pypi.org/simple
pip install freenom-dns
```
## How to use
```python
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
```
## print results
```
There were no changes
Record added successfully
---------------your domain----------------
['', 'A', '3600', 'xxx.xxx.xxx.xxx']
['WWW', 'A', '3600', 'xxx.xxx.xxx.xxx']
```
## License
[MIT](https://github.com/PunkLee2py/freenom-dns/blob/master/LICENSE)