# -*- coding: utf-8 -*-
{
    "name": "Library Management",

    "summary": "Manage library catalog and book lending.",
    "sequence": -100,

    "author": "Serhii Miroshnychenko",
    "license": "AGPL-3",
    "website": "https://github.com/SerhiiMiroshnychenko/Odoo_examples/tree/main/my_addons/library_app",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Services/Library",
    "version": "16.0.1.0.0",

    # any module necessary for this one to work correctly
    "depends": ["base"],

    # always loaded
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "views/book_view.xml",
        "views/library_menu.xml",
        "views/book_list_template.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "data/res.partner.csv",
        "data/library.book.csv",
        "data/book_demo.xml",
    ],

    "application": True,
}
