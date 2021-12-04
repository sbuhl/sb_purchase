# -*- coding: utf-8 -*-
{
    'name': "sb_purchase",

    'summary': """
        Remove the read only on the purchase and sale name""",

    'description': """
        Remove the read only on the purchase and sale name
    """,

    'author': "Sébastien Bühl",
    'website': "http://www.buhl.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
