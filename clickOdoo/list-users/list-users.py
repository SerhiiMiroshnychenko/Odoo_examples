# pip install click-odoo

#!/usr/bin/env python
from __future__ import print_function

for u in env['res.users'].search([]):
    print(u.login, u.name)
