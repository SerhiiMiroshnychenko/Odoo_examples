# pip install odoo-runner

import sys
from odoo_runner import OdooRunner


def start(env):
    return env['res.partner'].search_count([])


if __name__ == "__main__":
    args = sys.argv[1:]
    runner = OdooRunner(args, start)
    partner_count = runner.run()
    print("Number of partners:", partner_count)

    sys.exit(0)