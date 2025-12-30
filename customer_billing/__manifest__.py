# -*- coding: utf-8 -*-
{
    'name': "Billing Software",
    'summary': """
        """,
    'description': """

    """,
    'author': "Shiny Jenifer Lara",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_skills', 'sale', 'spreadsheet_dashboard', 'account', 'sale_management', 'product',
                'sale_pdf_quote_builder', 'purchase', 'phone_validation', 'l10n_tr_nilvera_einvoice'],
    'data': [

        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'security/ir_sequence.xml',
        # 'security/security.xml',
        'views/cust_details.xml',
        'views/financial_yr.xml',
        'views/exp_amt.xml',
        'views/menu_hide.xml',
        'views/sale_inv.xml',
        'views/purchase_inv.xml',
        'wizard/qr_scanner_xml.xml',
        'data/dashboard.xml',


    ],
    'qweb': [
        'static/src/xml/SwitchFinancialYearMenu.xml'
    ],

    # 'assets': {
    #         'web.assets_backend': [
    #             'customer_billing/static/src/js/SwitchFinancialYearMenu.js',
    #         ],
    #     },

    'installable': True,
    'application': True,
    'auto_install': False,
}