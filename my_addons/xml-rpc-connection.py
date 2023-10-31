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
property_ids = models.execute_kw(db, user_id, password, 'real.property', 'search', [[]])
print(f'search function ==> {property_ids}')  # search function ==> [1, 2, 3, 4, 5]

# count function
count_property_ids = models.execute_kw(db, user_id, password, 'real.property', 'search_count', [[]])
print(f'count function ==> {count_property_ids}')  # count function ==> 5

