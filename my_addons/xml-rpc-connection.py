import xmlrpc.client

url = 'http://localhost:8069'
username = 'veprzlisu@gmail.com'
password = 'odoo16'
db = 'edu-data'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
print(common.version())
# {
# 'server_version': '16.0',
# 'server_version_info': [16, 0, 0, 'final', 0, ''],
# 'server_serie': '16.0', 'protocol_version': 1
# }

user_id = common.authenticate(db, username, password, {})
print(f'{user_id = }')  # user_id = 2

# 'xmlrpc/2/object' 'execute_kw'
# 'db, uid, password, model_name, method_name, [], {}'


models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# search function
property_ids = models.execute_kw(db, user_id, password, 'real.property', 'search', [[]], {'offset': 2, 'limit': 3})
print(f'search function ==> {property_ids}')  # search function ==> [1, 2, 3, 4, 5]

# count function
count_property_ids = models.execute_kw(db, user_id, password, 'real.property', 'search_count', [[]])
print(f'count function ==> {count_property_ids}')  # count function ==> 5

# read function
read_property_ids = models.execute_kw(
    db,
    user_id,
    password,
    'real.property',
    'read',
    [property_ids],
    {'fields': ['id', 'name']}
)
print(f'read function ==> {read_property_ids}')
# read function ==> [
# {'id': 1, 'name': 'New House'},
# {'id': 2, 'name': 'New Villa😎'},
# {'id': 3, 'name': 'New Tower'},
# {'id': 4, 'name': 'New Test House'},
# {'id': 5, 'name': 'New Test Cabin'}
# ]


# search and read function
search_and_read_property_ids = models.execute_kw(
    db,
    user_id,
    password,
    'real.property',
    'search_read',
    [[]],
    {'fields': ['name', 'sales_id'], 'limit': 2}
)
print(f'search and read function ==> {search_and_read_property_ids}')
# search and read function ==> [
# {'id': 1, 'name': 'New House', 'sales_id': [2, 'Mitchell Admin']},
# {'id': 2, 'name': 'New Villa😎', 'sales_id': [6, 'Marc Demo']}
# ]


# create function
try:
    create_property_id = models.execute_kw(
        db, user_id, password,
        'real.property',
        'create',
        [{'name': 'Property from RPC', 'sales_id': 2}],
        {'context': {'lang': 'en_US'}}
    )
    print(f'create property ==> {create_property_id}')
except Exception as e:
    print(e.__class__, e)


# write function
try:
    write_property_id = models.execute_kw(
        db, user_id, password,
        'real.property',
        'write',
        [[8], {'name': 'Property from RPC Updated'}],
    )
    print(f'write property ==> {write_property_id}')
except Exception as e:
    print(e.__class__, e)

try:
    read_name_get = models.execute_kw(
        db, user_id, password,
        'real.property',
        'name_get',
        [[8]],
    )
    print(f'read_name_get ==> {read_name_get}')
except Exception as e:
    print(e.__class__, e)

# unlink function
try:
    unlink_property_id = models.execute_kw(
        db, user_id, password,
        'real.property',
        'unlink',
        [[8]],
    )
    print(f'unlink property ==> {unlink_property_id}')
except Exception as e:
    print(e.__class__, e)