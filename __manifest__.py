# -*- coding: utf-8 -*-
{
    'name': "gse_custo",

    'summary': """
        Ensemble de petites customizations pour la db Goshop Energy""",

    'description': """
        - Remove the read only on the purchase and sale name
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
    'depends': ['base', 'crm', 'purchase', 'sale', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/header_footer.xml',
        'report/sale_report.xml',
        'views/views.xml',
        'views/crm_lead_view.xml'
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}