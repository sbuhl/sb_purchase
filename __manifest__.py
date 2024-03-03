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
    'version': '17.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'account',
        'base',
        'base_automation',
        'crm',
        'hr',
        'industry_fsm_report',
        'mrp',
        'partner_commission',
        'project',  # recurrence
        'sale_project',
        'stock',  # qty_available
        'website_sale',  # public_categ_ids
        'purchase'
    ],

    'data': [
        'security/security.xml',
        'report/account.xml',
        'report/header_footer.xml',
        'report/sale_report_template.xml',
        'report/sale_report.xml',
        'report/payment_report_template.xml',
        'report/payment_report.xml',
        'report/mrporder.xml',
        'report/purchase.xml',
        'views/account_bank_statement.xml',
        'views/recouvrement.xml',
        'views/crm_lead_view.xml',
        'views/purchase_view.xml',
        'views/project_task.xml',
        'views/product.xml',
        'views/res_partner.xml',
        'views/sales_view.xml',
        'data/automated_actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gse_custo/static/scss/gse_custo.scss',
        ]
    },
}
