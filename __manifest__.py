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
    'version': '0.1.7.9',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'base_automation', 'account', 'crm', 'sale_project', 'hr',
        'stock',  # qty_available
        'website_sale',  # public_categ_ids
        'partner_commission'],

    'data': [
        'security/security.xml',
        'report/account.xml',
        'report/header_footer.xml',
        'report/sale_report_template.xml',
        'report/sale_report.xml',
        'report/payment_report_template.xml',
        'report/payment_report.xml',
        'report/mrporder.xml',
        'views/recouvrement.xml',
        'views/crm_lead_view.xml',
        'views/purchase_view.xml',
        'views/project_task.xml',
        'views/product.xml',
        'data/automated_actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gse_custo/static/scss/gse_custo.scss',
        ]
    },
}
