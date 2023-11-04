import json
import urllib.request
from random import randint

odoo_url = 'http://localhost:8069'
username = 'veprzlisu@gmail.com'
password = 'odoo16'
db = 'edu-data'


def json_rpc(url, method, params):
    data = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': randint(0, 1000000000),
    }
    headers = {
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

    if response.get('error'):
        raise Exception(response['error'])

    return response['result']


def call(url, service, method, *args):
    return json_rpc(f'{url}/jsonrpc', 'call', {'service': service, 'method': method, 'args': args})


user_id = call(odoo_url, 'common', 'login', db, username, password)
print(f'{user_id = }')

vals = {'name': 'Test JSON RPC Property', 'sales_id': 875}

try:
    create_property = call(
        odoo_url,
        'object',
        'execute',
        db,
        user_id,
        password,
        'real.property',
        'create',
        vals
    )
    print(f'{create_property = }')
except Exception as e:
    print(e.__class__, e)

create_property = call(
        odoo_url,
        'object',
        'execute',
        db,
        user_id,
        password,
        'real.property',
        'read',
        [10]
    )
print(f'{create_property = }')
