#!/usr/bin/env python
from __future__ import print_function
import click

import click_odoo


@click.command()
@click_odoo.env_options(default_log_level='error')
@click.option('--say-hello', is_flag=True)
def main(env, say_hello):
    if say_hello:
        click.echo("Hello!")
    for u in env['res.users'].search([]):
        print(u.login, u.name)


if __name__ == '__main__':
    main()