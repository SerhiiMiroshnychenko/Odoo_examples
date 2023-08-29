# Copyright © 2022 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import fields, models


class DemoWidget(models.Model):
    _name = "demo.widget"
    _description = 'Odoo Widgets Demo'

    name = fields.Char(
        string='Name',
    )
    calculator_int = fields.Integer(
        string='Calculator',
        help='The widget "calculator" allows to calculate digit values using '
             'a string representing as a simple formula.'
             'Supported arithmetic operations: + - * / ^ ( )',
    )
    calculator_float = fields.Float(
        string='Calculator',
        help='The widget "calculator" allows to calculate digit values using '
             'a string representing as a simple formula.'
             'Supported arithmetic operations: + - * / ^ ( )',
    )
    color_code = fields.Char(
        string="Color",
        help="Here you can set a specific HTML color index (e.g. #ff0000).",
    )
    code_python = fields.Text(
        string='Python Code',
        default="""
from datetime import datetime, timedelta

def get_product_name(product):
    return product.name
        """,
    )
    code_xml = fields.Text(
        string='XML Code',
        default="""<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="menu_demo_widget_root" model="ir.ui.menu">
        <field name="name">Widget Demo</field>
        <field name="web_icon">module,static/description/icon.png</field>
        <field name="sequence" eval="10"/>
    </record>
</odoo>    
        """,
    )
