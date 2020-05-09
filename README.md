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
    pub_ip = freenom.getPublicIP()

    # add or modify a record
    freenom.setRecord('your domain', '', 'a', pub_ip)
    freenom.setRecord('your domain', 'www', 'a', pub_ip)
    freenom.setRecord('your domain', 'test', 'a', pub_ip)

    # delete a record
    freenom.delRecord('your domain', 'test')

    # show all records with domain
    freenom.showRecords('your domain')
```
## print results
```
doLogin: Login successfully.
PublicIP: xxx.xxx.xxx.xxx
setRecord: There were no changes
setRecord: There were no changes
setRecord: Record added successfully
delRecord: Record deleted successfully
--------------your domain--------------
['', 'A', '3600', 'xxx.xxx.xxx.xxx']
['WWW', 'A', '3600', 'xxx.xxx.xxx.xxx']
```
## License
[MIT](https://github.com/PunkLee2py/freenom-dns/blob/master/LICENSE)