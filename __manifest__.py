# -*- coding: utf-8 -*-
{
    'name': "gse_custo",

    'summary': """
        Customizations pour Goshop Energy""",

    'description': """
        
    """,

    'author': "Sébastien Bühl",
    'website': "http://www.buhl.be",

    'category': 'Customizations',
    'version': '0.1.7.2',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'crm', 'purchase', 'sale', 'sale_management', 'project', 'sale_project', 'purchase_requisition', 'stock'],

    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'report/header_footer.xml',
        'report/sale_report_template.xml',
        'report/sale_report.xml',
        'report/payment_report_template.xml',
        'report/payment_report.xml',
        # 'report/stock_report.xml',
        # 'report/stock_report_template.xml',
        'views/views.xml',
        'views/recouvrement.xml',
        'views/crm_lead_view.xml',
        'views/purchase_view.xml',
        'views/project_task.xml',
        'views/product.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'gse_custo/static/scss/gse_custo.scss',
        ]
    },
}