import odoorpc

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)

# Check available databases
print(odoo.db.list())

# Login
odoo.login('edu-data', 'veprzlisu@gmail.com', 'odoo16')

# Current user
user = odoo.env.user
print(user.name)             # name of the user connected
print(user.company_id.name)  # the name of its company

# Simple 'raw' query
user_data = odoo.execute('res.users', 'read', [user.id])
print(user_data)

# Use all methods of a model
if 'sale.order' in odoo.env:
    Order = odoo.env['sale.order']
    order_ids = Order.search([])
    for order in Order.browse(order_ids):
        print(order.name)
        products = [line.product_id.name for line in order.order_line]
        print(products)

# Update data through a record
user1 = odoo.env['res.users'].browse(875)
print(f'{user1.name = }')
user1.name = "Brian Jones"
print(f'{user1.name = }')
